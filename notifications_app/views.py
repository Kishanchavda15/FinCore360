"""
notifications_app/views.py

GET  /notifications/                  → list  (admin: all, staff: own clients)
GET  /notifications/<pk>/            → retrieve one
POST /notifications/<pk>/send/       → manual send  (pending or failed)
POST /notifications/<pk>/send-urgent/ → urgent send  (alias, same logic)
"""

from celery.exceptions import OperationalError as CeleryOperationalError
from kombu.exceptions import OperationalError as KombuOperationalError
from redis.exceptions import ConnectionError as RedisConnectionError

from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications_app.models import Notification
from notifications_app.serializers import NotificationSerializer
from notifications_app.tasks import send_single_notification
from policies_app.permissions import IsAdminOrOwnerStaff

# Catch any broker-level connection failure
BROKER_ERRORS = (RedisConnectionError, CeleryOperationalError, KombuOperationalError, RuntimeError)


class NotificationListAPI(ListAPIView):
    """
    GET /notifications/
    Admin  → all notifications
    Staff  → only their assigned clients' notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Notification.objects
            .select_related("client", "policy")
            .order_by("-reminder_date")
        )
        if user.role == "admin":
            return qs
        # staff sees only their assigned clients
        return qs.filter(policy__client__assigned_staff=user)


class NotificationDetailAPI(RetrieveAPIView):
    """GET /notifications/<pk>/"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.select_related("client", "policy")
        if user.role == "admin":
            return qs
        return qs.filter(policy__client__assigned_staff=user)


class ManualSendNotificationAPI(APIView):
    """
    POST /notifications/<pk>/send/

    Queues the notification for immediate dispatch via Celery.
    Works for status="pending" or status="failed".
    Returns 409 if already sent.
    """
    permission_classes = [IsAdminOrOwnerStaff]

    def _get_notification_or_error(self, pk, user):
        try:
            notification = (
                Notification.objects
                .select_related("client", "policy__client")
                .get(pk=pk)
            )
        except Notification.DoesNotExist:
            raise ValidationError({"detail": "Notification not found."})

        # object-level permission
        if user.role == "staff":
            if notification.policy.client.assigned_staff_id != user.id:
                raise PermissionDenied(
                    "You can only manage notifications of your assigned clients."
                )
        return notification

    def post(self, request, pk, *args, **kwargs):
        notification = self._get_notification_or_error(pk, request.user)

        if notification.status == "sent":
            return Response(
                {
                    "detail": "Notification already sent.",
                    "notification_id": notification.pk,
                    "status": notification.status,
                    "sent_at": notification.sent_at,
                },
                status=409,
            )

        # Queue immediately in Celery
        try:
            task = send_single_notification.delay(notification.pk)
        except BROKER_ERRORS as exc:
            return Response(
                {
                    "detail": "Celery broker (Redis) is not reachable. "
                              "Please start Redis and the Celery worker, then try again.",
                    "error": str(exc),
                },
                status=503,
            )

        return Response(
            {
                "detail": "Notification queued for immediate sending.",
                "notification_id": notification.pk,
                "task_id": task.id,
                "current_status": notification.status,
                "channel": notification.channel,
            },
            status=202,
        )


class UrgentSendNotificationAPI(ManualSendNotificationAPI):
    """POST /notifications/<pk>/send-urgent/ — identical to manual send."""
    pass