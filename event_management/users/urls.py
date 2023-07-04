from django.urls import path
from .views import UserRegistrationView, UserAuthenticationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserAuthenticationView.as_view(), name='user-login'),
]
