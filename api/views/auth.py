from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.serializers import RegisterSerializer, LogoutSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, ChangePasswordSerializer
from api.permissions import IsAdminOrSuperAdmin

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{request.get_host()}/api/password-reset-confirm/{uid}/{token}/"

            message = _("Hi {username},\n\nWelcome! Click the link below to set your password:\n{link}").format(
                username=user.username, link=reset_link
            )
            try:
                send_mail(
                    subject=_("Set Your Equity Everest Password"),
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
            except Exception:
                return Response({"detail": _("User created, but failed to send email.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": _("User registered successfully! Password setup link sent to email."),
                "new_user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": _("Refresh token required.")}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": _("Logged out successfully")}, status=status.HTTP_205_RESET_CONTENT)

        except Exception:
            raise AuthenticationFailed(_("Invalid refresh token"))


class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        
        if not email:
            return Response({'error': _('Email is required')}, status=400)

        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{request.get_host()}/api/password-reset-confirm/{uid}/{token}/"

            send_mail(
                subject=_("Password Reset Request"),
                message=_("Hi {username},\n\nClick the link below to reset your password:\n{link}").format(
                    username=user.username, link=reset_link
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
        return Response({'message': _('If that email exists, a reset link has been sent.')}, status=200)


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  # validates new_password and re_new_password

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': _('Invalid user or UID')}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': _('Invalid or expired token')}, status=400)

        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return Response({'message': _('Password has been reset successfully')}, status=200)
    

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

