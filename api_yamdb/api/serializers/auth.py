from api.validators import (validate_forbidden_username,
                            validate_unique_case_insensitive_email,
                            validate_unique_case_insensitive_username)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import exceptions, serializers

User = get_user_model()


class UserSignUpSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=None)
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        try:
            self.user = User.objects.get(
                username=username, email=email)
        except User.DoesNotExist:
            validate_forbidden_username(username)
            validate_unique_case_insensitive_username(username)
            validate_unique_case_insensitive_email(email)
        return data

    def create(self, validated_data):
        if not validated_data.get('user'):
            validated_data['user'] = User.objects.create(
                username=validated_data.get('username'),
                email=validated_data.get('email'))
        return validated_data.get('user')


class UserTokenSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=None)
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        try:
            self.user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            msg = 'Пользователь не найден'
            raise exceptions.NotFound({'username': msg})
        if not check_password(data['confirmation_code'],
                              self.user.confirmation_code):
            msg = 'Предоставлены неверные учетные данные'
            raise exceptions.ValidationError({'token': msg})
        return data
