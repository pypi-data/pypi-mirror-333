import logging
from abc import abstractmethod
from typing import TypeVar, Generic, Self, Any, Callable

from pydantic import BaseModel, ValidationError

from promy.utils.http_requests import HTTPClient
from promy.utils.models import BaseModel as DjangoBaseModel

ModelType = TypeVar("ModelType", bound=DjangoBaseModel)

logger = logging.getLogger(__name__)


class SkipUpdate(Exception):
    ...


class Updater:
    @abstractmethod
    def update(self):
        ...


class ModelUpdater(BaseModel, Generic[ModelType], Updater):
    @abstractmethod
    def update(self) -> ModelType:
        ...


class UpdaterHandler:
    def __init__(
        self,
        default_object_name: str | None = None,
        client: HTTPClient | None = None,
    ) -> None:
        self.handlers: dict[
            str, tuple[type[Updater], tuple[Callable[[Any], None], ...]]
        ] = {}
        self.default_object_name = default_object_name

        self.client = client
        if self.client:
            assert self.client.base_url, "base_url is not provided to HTTPClient"

    def add(
        self,
        object_name: str,
        updater_class: type[Updater],
        *callbacks: Callable[[Any], None],
    ) -> Self:
        assert object_name not in self.handlers
        self.handlers[object_name] = updater_class, callbacks
        return self

    def pull(self, name: str, **kwargs) -> list[Any]:
        assert self.client, "client is not provided to UpdaterHandler"
        resp = self.client.get(
            "station/publisher/query",
            params={"name": name, **kwargs},
        )
        resp.raise_for_status()
        resp_body = resp.json()
        results = resp_body["results"]
        instances = []

        for item in results:
            instance = self(item, default_name=name)
            if instance:
                instances.append(instance)

        return instances

    def pull_one(self, name: str, **kwargs) -> Any | None:
        instances = self.pull(name, **kwargs)
        if not instances:
            return None

        assert len(instances) == 1
        return instances[0]

    def __call__(
        self, value, *, raise_exception: bool = False, default_name: str | None = None
    ) -> Any | None:
        if "object_name" in value:
            name = value["object_name"]
            data = value["body"]

        elif default_name or self.default_object_name:
            name = default_name or self.default_object_name
            data = value
        else:
            logger.info("unknown object received")
            return None

        if name not in self.handlers:
            logger.info("unknown object received", extra={"object_name": name})
            return None

        updater_class, callbacks = self.handlers[name]

        try:
            data["updater_handler"] = self
            updater = updater_class(**data)
        except ValidationError as e:
            if raise_exception:
                raise e
            logger.exception("invalid object received")
            return None

        try:
            instance = updater.update()
        except SkipUpdate:
            logger.info("update skipped")
            return None

        if instance is None:
            return None

        if isinstance(instance, DjangoBaseModel):
            logger.info(
                "object persisted",
                extra={
                    "model": instance.__class__.__name__,
                    "key": instance.key,
                    "created_at": instance.created_at,
                    "updated_at": instance.updated_at,
                },
            )
        else:
            logger.info("object persisted", extra={"object_name": name})

        for callback in callbacks:
            try:
                callback(instance)
            except Exception as e:
                if raise_exception:
                    raise e
                logger.exception("callback failed")

        return instance
