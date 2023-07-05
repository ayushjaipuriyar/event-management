from rest_framework import generics, permissions, status, response
from .models import Event, Registration
from venues.models import Venue
from .serializers import EventSerializer, RegistrationSerializer
import datetime
from django.conf import settings
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
import django_filters.rest_framework as filters
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

    def get_username(self, request, view):
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
        return user.username


class ParticipantPermission(permissions.BasePermission):
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

        # Check if the user is authenticated and is not an admin
        return user.role.lower() == 'participant'

    def get_username(self, request, view):
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

        # Check if the user is authenticated and is not an admin
        return user.username

    def get_user_id(self, request, view):
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

        return user_id


class EventFilter(filters.FilterSet):
    venue = filters.CharFilter(
        field_name='venue__name', lookup_expr='icontains')
    categories = filters.CharFilter(
        field_name='categories', lookup_expr='icontains')
    tags = filters.CharFilter(field_name='tags', lookup_expr='icontains')
    start_date = filters.DateFilter(
        field_name='start_time', lookup_expr='date')


class EventListView(generics.ListAPIView):
    queryset = Event.objects.filter(start_time__gte=datetime.datetime.now())
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = EventFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        queryset = Event.objects.filter(
            start_time__gte=datetime.datetime.now())
        venue = self.request.query_params.get('venue')
        categories = self.request.query_params.get('categories')
        tags = self.request.query_params.get('tags')
        start_date = self.request.query_params.get('start_date')

        if venue:
            queryset = queryset.filter(venue__name=venue)

        if categories:
            queryset = queryset.filter(categories__icontains=categories)

        if tags:
            queryset = queryset.filter(tags__icontains=tags)

        if start_date:
            queryset = queryset.filter(start_time__date=start_date)

        return queryset


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AdminPermission]

    def perform_create(self, serializer):
        admin_permission = AdminPermission()
        creator = admin_permission.get_username(self.request, self)
        serializer.save(creator=creator)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [ParticipantPermission]

    def post(self, request, *args, **kwargs):
        participant = ParticipantPermission()
        event_id = kwargs['event_pk']
        event = Event.objects.get(pk=event_id)

        user_id = participant.get_user_id(self.request, self)
        user = User.objects.get(pk=user_id)

        if Registration.objects.filter(event=event, user=user).exists():
            return response.Response({'error': 'You are already registered for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        registration = Registration(event=event, user=user, status='Pending')
        registration.save()

        return response.Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)


class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AdminPermission]

    def get_queryset(self):
        event_pk = self.kwargs['event_pk']
        permission = AdminPermission()
        username = permission.get_username(self.request, self)

        event = Event.objects.filter(pk=event_pk, creator=username).first()
        if not event:
            return Registration.objects.none()

        return Registration.objects.filter(event_id=event_pk)



class RegistrationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        permission = AdminPermission()
        instance = self.get_object()
        username = permission.get_username(self.request, self)
        if instance.event.creator != username:
            return response.Response({'error': 'You are not authorized to view this registration.'}, status=status.HTTP_403_FORBIDDEN)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        permission = AdminPermission()
        instance = self.get_object()
        username = permission.get_username(self.request, self)
        if instance.event.creator != username:
            return response.Response({'error': 'You are not authorized to approve or decline this registration.'}, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        permission = AdminPermission()
        context['is_admin'] = permission.has_permission(self.request, self)
        return context
