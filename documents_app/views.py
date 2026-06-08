from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from documents_app.models import Document
from documents_app.serializer import DocumentSerializer
from policies_app.permissions import IsAdminOrOwnerStaff


class DocumentListCreateAPI(ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    # ---------------------------
    # CREATE (MULTIPLE FILES)
    # ---------------------------
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(self.get_serializer(instance).data, status=201)


class DocumentRetrieveUpdateDeleteAPI(RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    # ---------------------------
    # PATCH UPDATE
    # ---------------------------
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()

        # object-level permission check
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # ---------------------------
    # DELETE
    # ---------------------------
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        obj.delete()

        return Response(status=204)
