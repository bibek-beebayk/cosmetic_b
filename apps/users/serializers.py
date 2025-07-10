from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if not email or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect email or password.")
        attrs["email"] = user.email
        attrs["id"] = user.id
        tokens = get_tokens(user)
        attrs["access_token"] = tokens["access"]
        attrs["refresh_token"] = tokens["refresh"]
        return attrs

    def create(self, validated_data):
        # This method is not used in this context but is required by the serializer
        return validated_data


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=32)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if not (email and password):
            raise serializers.ValidationError("Email and password are required.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages[0])

        return attrs
    
    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone", "full_name")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
