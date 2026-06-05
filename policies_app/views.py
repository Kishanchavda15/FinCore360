from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients_app.models import ClientProfile
from clients_app.permissions import IsAdminOrStaff
from policies_app.models import Policy
from policies_app.serializer import PolicySerializer


# Create your views here.

class PolicyGet(ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class PolicyCreateAPI(ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request, *args, **kwargs):
        client_id = request.data.get("client")

        try:
            client = ClientProfile.objects.get(id=client_id)
        except ClientProfile.DoesNotExist:
            raise PermissionDenied("Client not found")

        # ownership check
        if request.user.role != "admin" and client.created_by != request.user:
            raise PermissionDenied("You cannot create policy for this client")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(staff=request.user)

        return Response(serializer.data, status=201)