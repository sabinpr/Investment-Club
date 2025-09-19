from django.urls import path
from api.views import (
    RegisterView, LogoutView,
    ContributionListCreateView, ContributionCSVExportView,
    AssetInvestmentListCreateView, InvestmentListCreateView, ManualUpdateInvestmentView, OwnershipShareView,
    ProposalListCreateView, ProposalVoteView, ExpiredProposalsView,
    MeetingListCreateView, EducationalResourcesView, PasswordResetRequestView,
    PasswordResetConfirmView, DashboardView, ChangePasswordView, NotificationViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Contributions
    path('contributions/', ContributionListCreateView.as_view(), name='contribution-list-create'),
    path('contributions/download/', ContributionCSVExportView.as_view(), name='contribution-download'),

    # Portfolio
    path('portfolio/investments/', InvestmentListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolio/assets/', AssetInvestmentListCreateView.as_view(), name='portfolio-assets-list-create'),
    path('portfolio/assets/manual-update/', ManualUpdateInvestmentView.as_view(), name='portfolio-assets-manual-update'),
    path('portfolio/ownership/', OwnershipShareView.as_view(), name='portfolio-ownership'),

    # Proposals
    path('proposals/', ProposalListCreateView.as_view(), name='proposal-list-create'),
    path('proposals/<int:pk>/vote/', ProposalVoteView.as_view(), name='proposal-vote'),
    path('proposals/expired/', ExpiredProposalsView.as_view(), name='proposal-expired'),

    # Meetings
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    
    #Resources
    path('resources/', EducationalResourcesView.as_view(), name='educational-resources'),
    
    #Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    
    # Notifications
    path('notifications/', NotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='notification-detail'),
    path('notifications/unread/', NotificationViewSet.as_view({'get': 'unread'}), name='notification-unread'),
    path('notifications/<int:pk>/mark-as-read/', NotificationViewSet.as_view({'post': 'mark_as_read'}), name='notification-mark-as-read'),
    path('notifications/mark-all-as-read/', NotificationViewSet.as_view({'post': 'mark_all_as_read'}), name='notification-mark-all-as-read'),
    path('notifications/count-unread/', NotificationViewSet.as_view({'get': 'count_unread'}), name='notification-count-unread'),

]
