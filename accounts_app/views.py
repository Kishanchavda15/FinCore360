import random
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from accounts_app.models import User, OtpVerification
from accounts_app.serializer import RegisterUserSerializer, LoginUserSerializer, ResetPasswordSerializer, \
    ForgetPasswordSerializer


# Create your views here.

class RegisterUser(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoginUser(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginUserSerializer(data=data)
        serializer.is_valid()

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({"Error": "Password not exist."}, HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {"Message": "Login successfully .",
             "status": True,
             "token": {
                 "refresh": str(refresh),
                 "access": str(refresh.access_token)
             }
             }, status=HTTP_200_OK)


class SendOtp(GenericAPIView):
    queryset = OtpVerification.objects.all()
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ForgetPasswordSerializer(data=data)
        serializer.is_valid()

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "user not exist"}, HTTP_400_BAD_REQUEST)

        otp_code = str(random.randint(1000, 9999))

        OtpVerification.objects.create(user=user, otp=otp_code,
                                       expires_at=timezone.now() + timezone.timedelta(minutes=2))

        return Response({
            "status": True,
            "message": "otp sent successfully",
            "otp-code": otp_code}, status=HTTP_200_OK)


class ForgotPassword(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]


        user.set_password(new_password)
        user.save()

        otp.is_used = True
        otp.save()

        return Response({"message":"Password reset successfully"},status=HTTP_200_OK)

