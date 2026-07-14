from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from clients_app.models import ClientProfile
from clients_app.pagination import PageList
from notifications_app.utility import update_policy_reminders
from policies_app.permissions import IsAdminOrOwnerStaff
from policies_app.models import Policy
from policies_app.serializer import PolicySerializer, PolicyUpdateSerializer


class PolicyCreateAPI(ListCreateAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAdminOrOwnerStaff]
    pagination_class = PageList

    filter_backends = [SearchFilter, DjangoFilterBackend]

    search_fields = [
        "name",
        "product_type__name",        # Updated to use foreign key
        "product_subtype__name",     # Updated to use foreign key
        "status",
        "installment_frequency",
        "client__email",
    ]

    filterset_fields = [
        "status",
        "product_type",
        "product_subtype",
        "installment_frequency",
        "client",
        "staff",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Policy.objects.all().order_by("-id")
        return Policy.objects.filter(staff=user).order_by("-id")

    def perform_create(self, serializer):
        client_id = self.request.data.get("client")
        if not ClientProfile.objects.filter(id=client_id).exists():
            raise ValueError("Client not found")
        print("=" * 60)
        print("POLICY CREATE API CALLED")
        print("Time:", timezone.now())
        print("User:", self.request.user)
        print("Data:", self.request.data)
        print("=" * 60)
        serializer.save(staff=self.request.user)


class PolicyRetrieveUpdateDeleteAPI(RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    permission_classes = [IsAdminOrOwnerStaff]
    serializer_class = PolicyUpdateSerializer

    def patch(self, request, *args, **kwargs):
        policy = self.get_object()
        self.check_object_permissions(request, policy)
        serializer = self.get_serializer(policy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_policy_reminders(policy)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        policy = self.get_object()
        self.check_object_permissions(request, policy)
        policy.delete()
        return Response({"message": "Policy deleted successfully"}, status=200)