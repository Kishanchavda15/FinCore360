from rest_framework import serializers
from documents_app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)

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

        client = attrs.get("client")

        if client is None and self.instance:
            client = self.instance.client

        if client is None:
            raise serializers.ValidationError({"client": "Client is required."})

        if user.role == "staff" and client.assigned_staff_id != user.id:
            raise serializers.ValidationError(
                "You can only manage documents for your assigned clients."
            )

        return attrs

    def validate_client(self, client):
        request = self.context["request"]
        user = request.user

        if user.role == "staff" and client.assigned_staff_id != user.id:
            raise serializers.ValidationError(
                "You cannot assign this client."
            )

        return client

    def update(self, instance, validated_data):
        # FIX: proper file handling
        file = validated_data.get("file", None)
        if file:
            instance.file = file

        instance.document_type = validated_data.get(
            "document_type",
            instance.document_type
        )

        instance.client = validated_data.get(
            "client",
            instance.client
        )

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.file:
            data["file"] = instance.file.url
        return data