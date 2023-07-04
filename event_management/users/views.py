from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = make_password(serializer.validated_data['password'])
        fullname = serializer.validated_data['fullname']
        role = serializer.validated_data['role']

        User.objects.create(
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

        return response
