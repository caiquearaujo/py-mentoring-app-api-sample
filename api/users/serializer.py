from rest_framework import serializers
from . import services


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    location = serializers.CharField()
    employer = serializers.CharField()
    title = serializers.CharField()
    status = serializers.CharField()
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    location = serializers.CharField(allow_null=True, default=None, max_length=150)
    employer = serializers.CharField(allow_null=True, default=None, max_length=150)
    title = serializers.CharField(allow_null=True, default=None, max_length=150)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)


class UserSignUpSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)
    location = serializers.CharField(allow_null=True, default=None, max_length=150)
    employer = serializers.CharField(allow_null=True, default=None, max_length=150)
    title = serializers.CharField(allow_null=True, default=None, max_length=150)
    password = serializers.CharField(write_only=True, max_length=255)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, max_length=255)
