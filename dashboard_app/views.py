from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from dashboard_app.serializers import DashboardSummarySerializer
from dashboard_app.services import DashboardService


class DashboardAPIView(APIView):
    """
    Dashboard API

    Admin  -> Company Dashboard
    Staff  -> Staff Dashboard
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # ===========================
        # ADMIN DASHBOARD
        # ===========================
        if user.role == "admin":

            data = DashboardService.get_admin_dashboard()

            serializer = DashboardSummarySerializer(data)

            return Response(
                {
                    "status": True,
                    "role": "admin",
                    "message": "Admin dashboard fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        # ===========================
        # STAFF DASHBOARD
        # ===========================
        elif user.role == "staff":

            data = DashboardService.get_staff_dashboard(user)

            serializer = DashboardSummarySerializer(data)

            return Response(
                {
                    "status": True,
                    "role": "staff",
                    "message": "Staff dashboard fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        # ===========================
        # INVALID ROLE
        # ===========================
        return Response(
            {
                "status": False,
                "message": "Invalid user role.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )