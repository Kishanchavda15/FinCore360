from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from clients_app.pagination import PageList
from documents_app.models import Document
from documents_app.serializer import DocumentSerializer
from policies_app.permissions import IsAdminOrOwnerStaff

from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter

from documents_app.models import Document
from documents_app.serializer import DocumentSerializer
from policies_app.permissions import IsAdminOrOwnerStaff


class DocumentListCreateAPI(ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrOwnerStaff]
    pagination_class = PageList

    filter_backends = [SearchFilter]

    search_fields = [
        "document_type",
        "client__email",
    ]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)

        if role == "admin":
            return Document.objects.all().order_by("-id")

        if role == "staff":
            return Document.objects.filter(
                client__assigned_staff_id=user.id
            ).order_by("-id")

        return Document.objects.none()

class DocumentRetrieveUpdateDeleteAPI(RetrieveUpdateDestroyAPIView):
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
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        document = self.get_object()
        self.check_object_permissions(request, document)
        document.delete()

        return Response(status=204)