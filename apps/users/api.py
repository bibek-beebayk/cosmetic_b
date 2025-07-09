from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.order.serializers import OrderSerializer
from apps.users.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserSerializer,
)

User = get_user_model()


class AuthenticationViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # import ipdb; ipdb.set_trace()
        if serializer.validated_data.get("error"):
            return Response(
                {"detail": serializer.validated_data.get("error")}, status=400
            )
        return Response(serializer.validated_data)

    @action(methods=["post"], detail=False)
    def refresh(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=400)
        try:
            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)
            return Response({"access_token": access, "refresh_token": refresh_token})
        except Exception as e:
            return Response({"detail": "Invalid refresh token"}, status=401)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "orders":
            return OrderSerializer
        return super().get_serializer_class()

    @action(methods=["get", "put", "patch"], detail=False)
    def me(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        # Handle PUT/PATCH
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )  # Use partial=True for PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, url_path="change-password")
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(old_password):
            return Response(
                {"detail": "Incorrect existing password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response(
                {"detail": e.messages[0]}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully."}, status=status.HTTP_200_OK
        )
    
    @action(detail=False)
    def orders(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        user = request.user
        orders = user.orders.order_by("-created_at")[:20]
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
        
