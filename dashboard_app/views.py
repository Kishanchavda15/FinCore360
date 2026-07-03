from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts_app.models import User
from clients_app.models import ClientProfile
from documents_app.models import Document
from notifications_app.models import Notification
from policies_app.models import Policy

from .filters import (
    ClientProfileFilter,
    DocumentFilter,
    NotificationFilter,
    PolicyFilter,
    StaffFilter,
)
from .permissions import IsAdmin
from .serializers import (
    ClientProfileSerializer,
    DocumentSerializer,
    NotificationSerializer,
    PolicySerializer,
    StaffSerializer,
)


class StaffViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for staff/admin user accounts.
    Filtering:  ?role=staff&gender=female&is_active=true
    Search:     ?search=john
    Ordering:   ?ordering=-created_at
    """
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = StaffSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StaffFilter
    search_fields = ["full_name", "email", "phone_number"]
    ordering_fields = ["created_at", "full_name", "joining_date"]


class ClientProfileViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for client profiles.
    Filtering:  ?assigned_staff=3&city=Rajkot&gender=female
    Search:     ?search=patel
    Ordering:   ?ordering=-created_at,city
    """
    queryset = ClientProfile.objects.select_related("assigned_staff").order_by("-created_at")
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClientProfileFilter
    search_fields = ["full_name", "email", "phone_number", "city", "occupation"]
    ordering_fields = ["created_at", "full_name", "city", "date_of_birth"]


class PolicyViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for policies.
    Filtering:  ?product_type=loan&status=active&client=5&amount_min=10000
    Search:     ?search=home
    Ordering:   ?ordering=-start_date,amount
    """
    queryset = Policy.objects.select_related("client", "staff").order_by("-created_at")
    serializer_class = PolicySerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PolicyFilter
    search_fields = ["name", "client__full_name", "client__email"]
    ordering_fields = ["created_at", "start_date", "amount", "status"]


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for uploaded documents.
    Filtering:  ?document_type=Identity Document&client=5&policy=2
    Search:     ?search=patel
    Ordering:   ?ordering=-uploaded_at
    """
    queryset = Document.objects.select_related("client", "policy").order_by("-uploaded_at")
    serializer_class = DocumentSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = ["client__full_name", "client__email", "document_type"]
    ordering_fields = ["uploaded_at", "document_type"]


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for notifications.
    Filtering:  ?status=pending&channel=email&client=5
    Search:     ?search=renewal
    Ordering:   ?ordering=reminder_date
    """
    queryset = Notification.objects.select_related("client", "policy").order_by("-created_at_notification")
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NotificationFilter
    search_fields = ["title", "message", "client__full_name"]
    ordering_fields = ["reminder_date", "created_at_notification", "status"]


class DashboardStatsView(APIView):
    """
    Read-only summary counts for the admin dashboard landing page.
    GET /api/dashboard/stats/
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        data = {
            "staff_count": User.objects.filter(role="staff").count(),
            "admin_count": User.objects.filter(role="admin").count(),
            "client_count": ClientProfile.objects.count(),
            "policy_count": Policy.objects.count(),
            "policies_active": Policy.objects.filter(status="active").count(),
            "policies_completed": Policy.objects.filter(status="completed").count(),
            "document_count": Document.objects.count(),
            "notifications_pending": Notification.objects.filter(status="pending").count(),
            "notifications_sent": Notification.objects.filter(status="sent").count(),
            "notifications_failed": Notification.objects.filter(status="failed").count(),
        }
        return Response(data)
