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

        client = validated_data["client"]
        policy = validated_data.get("policy")
        document_type = validated_data["document_type"]

        created_docs = []

        for f in files:
            doc = Document.objects.create(client=client, policy=policy, document_type=document_type, file=f)
            created_docs.append(doc)

        # IMPORTANT: return first object (DRF compatible)
        return created_docs[0]

    # ---------------------------
    # VALIDATION
    # ---------------------------
    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        client = attrs.get("client")

        # Staff can only upload for assigned clients
        if user.role == "staff":
            if client.assigned_staff_id != user.id:
                raise serializers.ValidationError(
                    "You can only create documents for your assigned clients.")

        return attrs

    # ---------------------------
    # FIX RESPONSE FOR BULK
    # ---------------------------
    def to_representation(self, instance):
        return super().to_representation(instance)
