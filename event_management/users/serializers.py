from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'fullname', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
            role=validated_data['role']
        )
        return user


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    fullname = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'role')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        instance.user.fullname = user_data.get(
            'fullname', instance.user.fullname)
        instance.user.role = user_data.get('role', instance.user.role)
        instance.user.save()
        return instance

    def __init__(self, *args, **kwargs):
        is_admin = kwargs['context'].get('is_admin', False)
        super().__init__(*args, **kwargs)

        if is_admin:
            self.fields['id'].read_only = True
            self.fields['username'].read_only = True
            self.fields['email'].read_only = True
