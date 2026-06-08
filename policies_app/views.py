from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients_app.models import ClientProfile
from policies_app.permissions import IsAdminOrOwnerStaff
from policies_app.models import Policy
from policies_app.serializer import PolicySerializer, PolicyUpdateSerializer


# Create your views here.



class PolicyCreateAPI(ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def post(self, request, *args, **kwargs):
        client_id = request.data.get("client")

        try:
            ClientProfile.objects.get(id=client_id)
        except ClientProfile.DoesNotExist:
            raise PermissionDenied("Client not found")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(staff=request.user)

        return Response(serializer.data, status=201)

class PolicyRetrieveUpdateDeleteAPI(RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    permission_classes = [IsAdminOrOwnerStaff]
    serializer_class = PolicyUpdateSerializer

    def patch(self, request, *args, **kwargs):
        policy = self.get_object()
        self.check_object_permissions(request, policy)
        serializer = self.get_serializer(
            policy,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        policy = self.get_object()
        self.check_object_permissions(request, policy)
        policy.delete()

        return Response(
            {"message": "Policy deleted successfully"},
            status=200
        )