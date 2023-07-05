from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer
import jwt
from django.conf import settings
from events.serializers import RegistrationSerializer
from events.models import Registration
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10


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


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = make_password(serializer.validated_data['password'])
        fullname = serializer.validated_data['fullname']
        role = serializer.validated_data['role']

        User.objects.create(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            role=role
        )

        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)


class UserAuthenticationView(generics.CreateAPIView):
    serializer_class = UserAuthenticationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens with expiry dates
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        # Set the token as a secure HTTPS-only cookie
        response = Response({
            'user': UserRegistrationSerializer(user).data,
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        })
        response.set_cookie('access_token', access_token, max_age=60 *
                            60 * 24, secure=True, httponly=True, samesite='Strict')
        response.set_cookie('refresh_token', refresh_token, max_age=7*60 *
                            60 * 24, secure=True, httponly=True, samesite='Strict')
        response['Authorization'] = 'Bearer {}'.format(access_token)

        return response


class UserRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [ParticipantPermission]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        participant = ParticipantPermission()
        user_id = participant.get_user_id(self.request, self)
        return Registration.objects.filter(user_id=user_id)
