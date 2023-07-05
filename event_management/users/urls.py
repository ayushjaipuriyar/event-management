from django.urls import path
from .views import UserSignUpView, UserAuthenticationView, UserRegistrationsView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-register'),
    path('signin/', UserAuthenticationView.as_view(), name='user-login'),
    path('registrations/', UserRegistrationsView.as_view(),
         name='user-registrations'),
]
