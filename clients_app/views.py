from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import *

from clients_app.models import ClientProfile
from clients_app.permissions import IsAdminOrStaff
from clients_app.serializer import ClientSerializer, ClientUpdateSerializer


class ClientCreateApi(ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):

        user = self.request.user

        # Admin sees all clients
        if user.role == "admin":
            return ClientProfile.objects.all().order_by("-id")

        # Staff sees only assigned clients
        return ClientProfile.objects.filter(
            assigned_staff=user
        ).order_by("-id")

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        client = serializer.save()

        return Response(
            ClientSerializer(client).data,
            status=201
        )


class ClientUpdateApi(RetrieveUpdateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.serializer_class(client)

        return Response({
            "status": True,
            "message": "Client fetched successfully",
            "data": serializer.data
        }, status=HTTP_200_OK)

    def patch(self, request, *args, **kwargs):

        client = self.get_object()  # FIXED (important)

        serializer = self.serializer_class(
            client,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "Client updated successfully"
        }, status=HTTP_200_OK)