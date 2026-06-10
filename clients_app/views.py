from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import *

from clients_app.models import ClientProfile
from clients_app.permissions import IsAdminOrStaff
from clients_app.serializer import ClientSerializer, ClientUpdateSerializer


class ClientCreateApi(ListCreateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrStaff]

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}  # FIXED
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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