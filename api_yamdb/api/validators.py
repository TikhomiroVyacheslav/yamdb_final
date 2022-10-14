from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from rest_framework import serializers


def validate_forbidden_username(value):
    """Проверяет, что имя пользователя не является «me»."""
    if 'me' == value.lower():
        msg = f'Нельзя создать пользователя с именем «{value}».'
        raise ValidationError(msg)

    return value


def validate_unique_case_insensitive_username(value):
    """Независимо от регистра проверяет, что имя пользователя уникально."""
    user_model = get_user_model()
    if user_model.objects.filter(username__iexact=value).exists():
        msg = gettext_lazy('A user with that username already exists.')
        raise ValidationError(msg)
    return value


def validate_unique_case_insensitive_email(value):
    """Независимо от регистра проверяет, что email пользователя уникален."""
    user_model = get_user_model()
    if user_model.objects.filter(email__iexact=value).exists():
        msg = 'Пользователь с таким адресом электронной почты уже существует.'
        raise ValidationError(msg)
    return value


def validate_score(value):
    """Проверка оценки пользователя в отзыве."""
    if not 1 <= value <= 10:
        raise serializers.ValidationError(
            'Ваша оценка произведению должна быть в диапазоне 1-10.'
        )
    elif isinstance(value, float):
        raise serializers.ValidationError(
            'Ваша оценка произведению должна быть целым числом.'
        )
    return True
