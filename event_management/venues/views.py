# venues/views.py
from rest_framework import generics, permissions, response
from .models import Venue
from .serializers import VenueSerializer
from rest_framework import generics, permissions
from django.conf import settings
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from events.models import Event
from events.serializers import EventSerializer
import jwt


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the access token is present in the request cookies
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return False
        try:
            # Decode the access token and extract the user ID
            decoded_token = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms='HS256')
            user_id = decoded_token.get('user_id')
        except jwt.ExpiredSignatureError:
            return False

        # Look up the user based on the user ID from the access token
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False

        # Check if the user is authenticated and has the 'admin' role
        return user.role.lower() == 'admin'


class VenueListView(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AdminPermission]


class VenueCreateView(generics.CreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AdminPermission]


class VenueDetailView(generics.RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        venue = self.get_object()
        events = Event.objects.filter(venue=venue)
        event_serializer = EventSerializer(events, many=True)
        venue_serializer = self.get_serializer(venue)
        data = {
            'venue': venue_serializer.data,
            'events': event_serializer.data
        }
        return response.Response(data)


class VenueUpdateView(generics.UpdateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AdminPermission]


class VenueDeleteView(generics.DestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AdminPermission]
