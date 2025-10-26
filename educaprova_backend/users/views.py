import secrets
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EmailTokenSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class EmailTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class GuestLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Cria usuário convidado temporário
        User = get_user_model()
        rand = secrets.token_hex(4)
        email = f"guest_{rand}@guest.local"
        username = f"guest_{rand}"
        user = User.objects.create(
            email=email,
            username=username,
            is_guest=True,
            plan=User.Plan.FREE,
            guest_expires_at=timezone.now() + timedelta(days=7),
        )
        # Define uma senha aleatória para cumprir política (não será usada)
        user.set_password(secrets.token_urlsafe(16))
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        })


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = ForgotPasswordSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        email = s.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Não vazar existência do e-mail
            return Response({"detail": "Se o e-mail existir, enviaremos instruções."})

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Em dev, retornamos o token/uid para facilitar
        return Response({"detail": "Instruções enviadas.", "uid": uid, "token": token})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = ResetPasswordSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        uid = s.validated_data["uid"]
        token = s.validated_data["token"]
        new_password = s.validated_data["new_password"]
        try:
            uid_int = int(urlsafe_base64_decode(uid).decode("utf-8"))
            user = User.objects.get(pk=uid_int)
        except Exception:
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Senha redefinida com sucesso."})
