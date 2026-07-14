from django.contrib.auth.hashers import make_password
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
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist"})

        # Check if OTP exists and is valid
        try:
            otp_record = OtpVerification.objects.get(
                user=user,
                otp=otp,
                is_used=False,
                is_verify=False
            )
        except OtpVerification.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid OTP code"})

        # Check if OTP is expired
        if otp_record.is_expired:
            raise serializers.ValidationError({"otp": "OTP has expired"})

        data['user'] = user
        data['otp_record'] = otp_record

        return data

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "gender", "address", "role", "profile_image"]
        read_only_fields = ["id", "email", "role"]


# ======================================================
# NEW SERIALIZER (PENDING REGISTRATION)
# ======================================================
class PendingRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PendingRegistration
        fields = [
            "full_name",
            "email",
            "phone_number",
            "gender",
            "address",
            "password",
            "confirm_password"
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if email already exists in User model
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})

        # Check if email already exists in PendingRegistration
        if PendingRegistration.objects.filter(email=data.get('email'), is_verified=False).exists():
            raise serializers.ValidationError({"email": "Registration already pending for this email."})

        # Check if password and confirm_password match
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        # Remove confirm_password if it exists
        validated_data.pop('confirm_password', None)

        # ✅ DON'T HASH HERE - store plain password
        # The password will be hashed when creating the actual user

        # Create the pending registration
        pending = PendingRegistration.objects.create(**validated_data)
        return pending

# Add at the end of the file

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user