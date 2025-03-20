from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    CREATED_AT = False
    UPDATED_AT = False

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True

    def get_fields(self):
        fields = super().get_fields()

        if "archived_at" in fields:
            fields.pop("archived_at")

        if not self.CREATED_AT and "created_at" in fields:
            fields.pop("created_at")

        if not self.UPDATED_AT and "updated_at" in fields:
            fields.pop("updated_at")

        return fields


class UserIdSerializerMixin:
    def validate(self, attrs):
        attrs["user_id"] = self.context.get("user_id", None)
        return attrs

    def add_user_id(self, user_id):
        self.context["user_id"] = user_id
