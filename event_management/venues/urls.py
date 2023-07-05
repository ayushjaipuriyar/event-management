from django.urls import path
from .views import (
    VenueListView,
    VenueCreateView,
    VenueDetailView,
    VenueUpdateView,
    VenueDeleteView,
)

urlpatterns = [
    path('', VenueListView.as_view(), name='venue-list'),
    path('create/', VenueCreateView.as_view(), name='venue-create'),
    path('<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    path('<int:pk>/update/', VenueUpdateView.as_view(), name='venue-update'),
    path('<int:pk>/delete/', VenueDeleteView.as_view(), name='venue-delete'),
]
