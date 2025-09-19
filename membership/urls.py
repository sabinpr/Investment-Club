from django.urls import path
from .views import MembershipRequestViewSet

urlpatterns = [
    # Membership Requests
    path('membership-requests/', MembershipRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='membership-request-list'),
    path('membership-requests/<int:pk>/', MembershipRequestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='membership-request-detail'),
    path('membership-requests/<int:pk>/approve/', MembershipRequestViewSet.as_view({'post': 'approve'}), name='membership-request-approve'),
    path('membership-requests/<int:pk>/reject/', MembershipRequestViewSet.as_view({'post': 'reject'}), name='membership-request-reject'),
]