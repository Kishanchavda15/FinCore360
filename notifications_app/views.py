# notifications_app/views.py

"""
notifications_app/views.py
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

# Import the dispatch function from tasks
from notifications_app.tasks import _dispatch

# Catch any broker-level connection failure
BROKER_ERRORS = (RedisConnectionError, CeleryOperationalError, KombuOperationalError, RuntimeError)


class NotificationListAPI(ListAPIView):
    """GET /notifications/"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrOwnerStaff]

    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.select_related("client", "policy").order_by("-reminder_date")
        if user.role == "admin":
            return qs
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
    Sends notification IMMEDIATELY (synchronously)
    """
    permission_classes = [IsAdminOrOwnerStaff]

    def _get_notification_or_error(self, pk, user):
        try:
            notification = Notification.objects.select_related("client", "policy__client").get(pk=pk)
        except Notification.DoesNotExist:
            raise ValidationError({"detail": "Notification not found."})

        if user.role == "staff":
            if notification.policy.client.assigned_staff_id != user.id:
                raise PermissionDenied("You can only manage notifications of your assigned clients.")
        return notification

    def post(self, request, pk, *args, **kwargs):
        notification = self._get_notification_or_error(pk, request.user)

        # Check if already sent
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

        # ✅ Send IMMEDIATELY (synchronously) - No Celery required!
        try:
            # Mark as manual send mode
            if notification.send_mode != "manual":
                notification.send_mode = "manual"
                notification.save(update_fields=["send_mode"])

            # Call dispatch directly (synchronous)
            _dispatch(notification)

            return Response(
                {
                    "detail": "Notification sent successfully!",
                    "notification_id": notification.pk,
                    "status": notification.status,
                    "sent_at": notification.sent_at,
                    "channel": notification.channel,
                },
                status=200,
            )
        except Exception as exc:
            return Response(
                {
                    "detail": f"Failed to send notification: {str(exc)}",
                    "notification_id": notification.pk,
                    "status": notification.status,
                },
                status=500,
            )


class UrgentSendNotificationAPI(ManualSendNotificationAPI):
    """POST /notifications/<pk>/send-urgent/ - Same as manual send"""
    pass