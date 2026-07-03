import random

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_202_ACCEPTED

from accounts_app.models import User, OtpVerification, PendingRegistration
from accounts_app.serializer import RegisterUserSerializer, LoginUserSerializer, ResetPasswordSerializer, \
    ForgetPasswordSerializer, UpdateProfileSerializer, UserSerializer, PendingRegisterSerializer
from accounts_app.utils import generate_secret_key
from fincore import settings


# Create your views here.
#
#
# class RegisterUser(ListCreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = RegisterUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class LoginUser(ListCreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = LoginUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = LoginUserSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#
#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]
#
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, HTTP_404_NOT_FOUND)
#         if not user.check_password(password):
#             return Response({"error": "Invalid password"}, status=HTTP_400_BAD_REQUEST)
#
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {"Message": "Login successfully .",
#              "status": True,
#              "user": UserSerializer(
#                  user,
#                  context={"request": request}
#              ).data,
#              "token": {
#                  "refresh": str(refresh),
#                  "access": str(refresh.access_token)
#              }
#              }, status=HTTP_200_OK)
#
#
# class SendOtp(GenericAPIView):
#     queryset = OtpVerification.objects.all()
#     serializer_class = ForgetPasswordSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = ForgetPasswordSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#
#         email = serializer.validated_data["email"]
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"message": "user not exist"}, HTTP_400_BAD_REQUEST)
#
#         otp_code = str(random.randint(1000, 9999))
#
#         OtpVerification.objects.create(user=user, otp=otp_code,
#                                        expires_at=timezone.now() + timezone.timedelta(minutes=2))
#
#         return Response({
#             "status": True,
#             "message": "otp sent successfully",
#             "otp-code": otp_code}, status=HTTP_200_OK)
#
#
# class ForgotPassword(GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = ResetPasswordSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.validated_data["user"]
#         otp = serializer.validated_data["otp"]
#         new_password = serializer.validated_data["new_password"]
#
#         user.set_password(new_password)
#         user.save()
#
#         otp.is_used = True
#         otp.save()
#
#         return Response({"message": "Password reset successfully"}, status=HTTP_200_OK)
#
#
# class UpdateProfile(RetrieveUpdateAPIView):
#     serializer_class = UpdateProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):  # FIXED (clean way)
#         return self.request.user
#
#     def retrieve(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.serializer_class(user)
#         return Response({"status": True, "message": "Profile fetch successfully", "data": serializer.data},
#                         status=HTTP_202_ACCEPTED)
#
#     def patch(self, request, *args, **kwargs):
#         user = request.user
#
#         serializer = self.serializer_class(
#             user,
#             data=request.data,
#             partial=True
#         )
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(
#             {
#                 "status": True,
#                 "message": "Profile updated successfully",
#                 "user": UserSerializer(
#                     user,
#                     context={"request": request}
#                 ).data
#             },
#             status=HTTP_200_OK
#         )



# ======================================================
# 1. PENDING REGISTER API
# ======================================================
class RegisterPendingUser(CreateAPIView):
    queryset = PendingRegistration.objects.all()
    serializer_class = PendingRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        secret_key = generate_secret_key(8)

        pending = serializer.save(secret_key=secret_key)

        send_mail(
            subject="New Registration Request",
            message=f"""
New User Registration:

Email: {pending.email}
Secret Key: {secret_key}

Share this key with user to approve registration.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@gmail.com"]
        )

        return Response({
            "status": True,
            "message": "Registration submitted. Waiting for approval."
        }, status=HTTP_200_OK)


# ======================================================
# 2. VERIFY SECRET KEY + CREATE USER
# ======================================================
class VerifySecretKey(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        secret_key = request.data.get("secret_key")

        try:
            pending = PendingRegistration.objects.get(
                email=email,
                secret_key=secret_key,
            )
        except PendingRegistration.DoesNotExist:
            return Response({"error": "Invalid email or secret key"}, status=HTTP_400_BAD_REQUEST)

        # create real user
        user = User.objects.create_user(
            email=pending.email,
            full_name=pending.full_name,
            phone_number=pending.phone_number,
            gender=pending.gender,
            address=pending.address,
            password=pending.password
        )

        pending.delete()

        return Response({
            "status": True,
            "message": "User created successfully"
        }, status=HTTP_200_OK)


# ======================================================
# 3. LOGIN API (UNCHANGED)
# ======================================================
class LoginUser(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            "status": True,
            "user": UserSerializer(user, context={"request": request}).data,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=HTTP_200_OK)


# ======================================================
# 4. OTP SEND API (UNCHANGED)
# ======================================================
class SendOtp(GenericAPIView):
    queryset = OtpVerification.objects.all()
    serializer_class = ForgetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "user not exist"}, status=HTTP_400_BAD_REQUEST)

        otp_code = str(random.randint(1000, 9999))

        OtpVerification.objects.create(
            user=user,
            otp=otp_code,
            expires_at=timezone.now() + timezone.timedelta(minutes=2)
        )

        return Response({
            "status": True,
            "message": "otp sent successfully",
            "otp-code": otp_code
        }, status=HTTP_200_OK)


# ======================================================
# 5. FORGOT PASSWORD (UNCHANGED)
# ======================================================
class ForgotPassword(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        otp.is_used = True
        otp.save()

        return Response({"message": "Password reset successfully"}, status=HTTP_200_OK)


# ======================================================
# 6. PROFILE API (UNCHANGED)
# ======================================================
class UpdateProfile(RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "Profile updated",
            "user": UserSerializer(user, context={"request": request}).data
        }, status=HTTP_200_OK)