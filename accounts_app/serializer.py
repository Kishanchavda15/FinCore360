from rest_framework import serializers

from accounts_app.models import User, OtpVerification


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "password", "phone_number", "gender", "address", "role","profile_image"]


    def create(self, validated_data):
        validated_data["role"] = "staff"  # FIXED: prevent role abuse
        return User.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User does not exist. "})

        try:
            otp_obj = OtpVerification.objects.get(user=user, otp=otp, is_used=False)
        except OtpVerification.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid OTP or OTP not verified."})  # FIXED

        if otp_obj.is_expired:  # ADDED
            raise serializers.ValidationError({"otp": "OTP expired"})

        attrs["user"] = user
        attrs["otp"] = otp

        return attrs


class UpdateProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "gender", "address", "role", "profile_image",
                 ]
        read_only_fields=["id","email","role"]

