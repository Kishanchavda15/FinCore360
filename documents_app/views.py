from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from documents_app.models import Document
from documents_app.serializer import DocumentSerializer
from policies_app.permissions import IsAdminOrOwnerStaff


class DocumentListCreateAPI(ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save()


class DocumentRetrieveUpdateDeleteAPI(
    RetrieveUpdateDestroyAPIView
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def get_serializer_context(self):
        return {"request": self.request}

    def patch(self, request, *args, **kwargs):
        document = self.get_object()

        self.check_object_permissions(request, document)

        serializer = self.get_serializer(
            document,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        document = self.get_object()

        self.check_object_permissions(request, document)

        document.delete()

        return Response(status=204)