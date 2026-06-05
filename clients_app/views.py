from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_200_OK

from clients_app.models import ClientProfile
from clients_app.permissions import IsAdminOrStaff
from clients_app.serializer import ClientSerializer, ClientUpdateSerializer


# Create your views here.

class ClientCreateApi(ListCreateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrStaff]

    def post(self, request, *args, **kwargs):
        user = request.user.email
        serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():
            serializer.save(assigned_staff=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ClientUpdateApi(RetrieveUpdateAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({"status": True, "message": "Profile fetch successfully", "data": serializer.data},
                        status=HTTP_202_ACCEPTED)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user,data=request.data,partial=True)

        if not serializer.is_valid():
            return Response({"status": False,
                             "message": "update failed",
                             "errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {"status": True,
             "message": "Profile update successfully."}, status=HTTP_200_OK)
