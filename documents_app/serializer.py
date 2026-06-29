from rest_framework import serializers
from documents_app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Document
        fields = [
            "id",
            "client",
            "policy",
            "document_type",
            "file",
            "uploaded_at",
        ]
        read_only_fields = ["id", "uploaded_at"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        # Use existing client during PATCH if not supplied
        client = attrs.get("client")

        if client is None and self.instance:
            client = self.instance.client

        if client is None:
            raise serializers.ValidationError(
                {"client": "Client is required."}
            )

        if (
            user.role == "staff"
            and client.assigned_staff_id != user.id
        ):
            raise serializers.ValidationError(
                "You can only manage documents for your assigned clients."
            )

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.file:
            data["file"] = instance.file.url

        return data