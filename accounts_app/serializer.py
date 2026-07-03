from rest_framework import serializers
from accounts_app.models import User, OtpVerification, PendingRegistration


# -------------------------
# EXISTING SERIALIZERS (KEEP ALL YOUR OLD ONES)
# -------------------------

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "full_name", "email", "password",
            "phone_number", "gender", "address",
            "role", "profile_image"
        ]

    def create(self, validated_data):
        validated_data["role"] = "staff"
        return User.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "full_name", "email",
            "phone_number", "gender", "address",
            "role", "profile_image", "joining_date"
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if not obj.profile_image:
            return None
        return request.build_absolute_uri(obj.profile_image.url) if request else obj.profile_image.url


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "gender", "address", "role", "profile_image"]
        read_only_fields = ["id", "email", "role"]


# ======================================================
# NEW SERIALIZER (PENDING REGISTRATION)
# ======================================================
class PendingRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingRegistration
        fields = [
            "full_name",
            "email",
            "phone_number",
            "gender",
            "address",
            "password"
        ]