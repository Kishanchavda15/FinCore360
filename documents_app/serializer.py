from rest_framework import serializers
from documents_app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = Document
        fields = ["id", "client", "policy", "document_type", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def create(self, validated_data):
        files = validated_data.pop("file")

        docs = []
        for f in files:
            docs.append(
                Document.objects.create(**validated_data, file=f)
            )
        return docs

    def validate(self, attrs):

        request = self.context.get("request")  # FIXED (safe access)
        user = request.user

        client = attrs.get("client")

        # IMPORTANT: staff restriction
        if user.role == "staff":
            if client.assigned_staff_id != user.id:
                raise serializers.ValidationError(
                    "You can only upload documents for your assigned clients."
                )

        return attrs

    def to_representation(self, instance):
        return super().to_representation(instance)
