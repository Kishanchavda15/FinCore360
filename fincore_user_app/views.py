from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from fincore_user_app.models import User
from fincore_user_app.serializer import RegisterUserSerializer, LoginUserSerializer


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
        serializer =LoginUserSerializer(data=data)
        serializer.is_valid()

        email =serializer.validated_data["email"]
        password =serializer.validated_data["password"]

        try:
            user = User.objects.filter(email=-email).frist()
        except User.DoseNotExist:
            return Response({"error":"User not found."},HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"Error":"Password not exist."},HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response (
            {"Message":"Login successfully .",
             "status":True,
            "token":{
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            }
        },status=HTTP_200_OK)

