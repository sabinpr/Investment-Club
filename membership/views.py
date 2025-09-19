from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from .permissions import IsAdminOrSuperAdmin
from .models import MembershipRequest
from .serializers import MembershipRequestSerializer, MembershipRequestCreateSerializer

User = get_user_model()


class MembershipRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling membership requests.
    - Anyone can create a request
    - Admins/Superadmins can view, approve, or reject requests
    """
    queryset = MembershipRequest.objects.all()
    
    def get_permissions(self):
        # Allow public access to create membership requests
        # Restrict list/retrieve/approve/reject to admin or superadmin
        if self.action in ['create']:
            return [AllowAny()]
        elif self.action in ['list', 'retrieve', 'approve', 'reject']:
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        # Use a different serializer for creation (simplified input)
        if self.action in ['create']:
            return MembershipRequestCreateSerializer
        return MembershipRequestSerializer
    
    def perform_create(self, serializer):
        # Automatically set status to 'pending' when a request is submitted
        serializer.save(status='pending')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Custom action to approve a pending membership request.
        - Creates a new user account with 'member' role
        - Sends password setup email to the user
        """
        membership_request = self.get_object()
        
        # Allow approval only if the request is still pending
        if membership_request.status != 'pending':
            return Response({'detail': 'Request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prevent duplicate users
        if User.objects.filter(email=membership_request.email).exists():
            return Response({'detail': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user account
        user = User.objects.create(
            username=membership_request.email.split('@')[0],
            email=membership_request.email,
            role='member',
            is_active=True
        )
        
        # Generate password reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{request.scheme}://{request.get_host()}/api/password-reset-confirm/{uid}/{token}/"

        # Send email with password setup link
        send_mail(
            subject="Set Your Equity Everest Password",
            message=(
                "Hi {username},\n\nWelcome to Everest Equity Club!\n\n"
                "Please set your account password using the link below:\n\n{link}\n\n"
                "This link will expire soon for security reasons.\n\n"
                "Thank you!"
            ).format(username=user.username, link=reset_link),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        # Update membership request status
        membership_request.status = 'approved'
        membership_request.responded_at = timezone.now()
        membership_request.save()
        
        return Response({
            "message": "Membership approved and user created. Password setup link sent.",
            "user_email": user.email
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Custom action to reject a pending membership request.
        """
        membership_request = self.get_object()
        
        if membership_request.status != 'pending':
            return Response({'detail': 'Request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as rejected and log response time
        membership_request.status = 'rejected'
        membership_request.responded_at = timezone.now()
        membership_request.save()
        
        return Response(MembershipRequestSerializer(membership_request).data, status=status.HTTP_200_OK)
