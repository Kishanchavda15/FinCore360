from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from clients_app.models import ClientProfile
from clients_app.permissions import IsAdminOrStaff
from clients_app.serializer import ClientSerializer, ClientUpdateSerializer


class ClientCreateApi(ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrStaff]
    queryset = ClientProfile.objects.all()
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    ordering = ["-id"]

    search_fields = [
        "full_name",
        "email",
        "phone_number",
        "city",
    ]

    def get_queryset(self):
        user = self.request.user

        # Admin sees all clients
        if user.role == "admin":
            return ClientProfile.objects.all().order_by("-id")

        # Staff sees only assigned clients
        return ClientProfile.objects.filter(
            assigned_staff=user
        ).order_by("-id")

    def perform_create(self, serializer):
        # Auto-assign staff if user is staff
        if self.request.user.role == 'staff':
            serializer.save(assigned_staff=self.request.user)
        else:
            serializer.save()


class ClientUpdateApi(RetrieveUpdateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientUpdateSerializer
    permission_classes = [IsAdminOrStaff]

    def retrieve(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.get_serializer(client)

        return Response({
            "status": True,
            "message": "Client fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.get_serializer(
            client,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "Client updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)