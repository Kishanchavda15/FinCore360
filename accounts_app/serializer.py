from rest_framework import serializers

from accounts_app.models import User, OtpVerification


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "password", "phone_number", "gender", "address", "role"]

    def create(self, validated_data):
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
            otp = OtpVerification.objects.get(user=user, otp=otp, is_used=False)
        except OtpVerification.DoesNotExist:
            raise serializers.ValidationError({"otp", "Invalid OTP or OTP not verified."})

        attrs["user"] = user
        attrs["otp"] = otp

        return attrs


