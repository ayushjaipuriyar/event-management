from django.urls import path
from .views import UserSignUpView, UserAuthenticationView, UserRegistrationsView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-register'),
    path('signin/', UserAuthenticationView.as_view(), name='user-login'),
    path('registrations/', UserRegistrationsView.as_view(),
         name='user-registrations'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(),
         name='admin-user-detail'),
]
