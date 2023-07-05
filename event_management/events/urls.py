from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    RegisterView,
    RegistrationListView,
    RegistrationDetailView,
#     RegistrationApprovalView,
)

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:event_pk>/registrations/',
         RegistrationListView.as_view(), name='registration-list'),
    path('<int:event_pk>/register/', RegisterView.as_view(),
         name='registration-create'),
    path('<int:event_pk>/registrations/<int:pk>/',
         RegistrationDetailView.as_view(), name='registration-detail'),
#     path('<int:event_pk>/registrations/<int:pk>/approval/',
#          RegistrationApprovalView.as_view(), name='registration-approval'),
]
