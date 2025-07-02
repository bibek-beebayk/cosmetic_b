from rest_framework import serializers
from django.contrib.auth import get_user_model
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
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")