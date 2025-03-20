from promy.station.registry import station_registry
from promy.utils.celery import app
from promy.utils.monitoring import observe


@app.task
@observe("publish_everything", const_labels={"observer_type": "celery_task"})
def publish_everything() -> None:
    for publisher in station_registry.publishers:
        publisher.publish_all()


@app.task
@observe(
    "publish_recently_updated_objects", const_labels={"observer_type": "celery_task"}
)
def publish_recently_updated_objects() -> None:
    for publisher in station_registry.publishers:
        publisher.publish_recently_updated()


@app.task
@observe("update_everything", const_labels={"observer_type": "celery_task"})
def update_everything() -> None:
    if station_registry.periodic_updaters is None:
        return
    station_registry.periodic_updaters.update("all")


@app.task
@observe("update_set", const_labels={"observer_type": "celery_task"})
def update_set(name: str) -> None:
    if station_registry.periodic_updaters is None:
        return
    station_registry.periodic_updaters.update(name)
