from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class AuthenticationViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = None

    @action(methods=["post"], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("error"):
            return Response(
                {"detail": serializer.validated_data.get("error")}, status=400
            )
        return Response(serializer.validated_data.get("login_info"))
    

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
