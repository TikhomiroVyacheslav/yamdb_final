import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from api.validators import (validate_forbidden_username,
                            validate_unique_case_insensitive_email,
                            validate_unique_case_insensitive_username)
from api_yamdb.settings import DEFAULT_FROM_EMAIL


class User(AbstractUser):
    _USER = 'user'
    _MODERATOR = 'moderator'
    _ADMIN = 'admin'

    ROLE_CHOICES = (
        (_USER, 'Пользователь'),
        (_MODERATOR, 'Модератор'),
        (_ADMIN, 'Администратор'),
    )

    # Переопределяем стандартные поля модели AbstractUser
    # Оставляем gettext_lazy для переводов

    # Добавляем валидаторы
    username = models.CharField(
        gettext_lazy('username'),
        max_length=150,
        unique=True,
        help_text=gettext_lazy('Required. 150 characters or fewer. '
                               'Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(),
                    validate_forbidden_username,
                    validate_unique_case_insensitive_username],
        error_messages={
            'unique':
                gettext_lazy('A user with that username already exists.'),
        },
    )

    # Делаем поле уникальным и обязательным
    email = models.EmailField(
        gettext_lazy('email address'),
        blank=False, null=False, unique=True,
        validators=[validate_unique_case_insensitive_email],
        error_messages={
            'unique':
                'Пользователь с таким адресом электронной почты '
                'уже существует.'
        }
    )

    # Максимальный размер поля в django 2.2 = 30, меняем на 150
    first_name = models.CharField(gettext_lazy('first name'), max_length=150,
                                  blank=True)

    # Новые поля
    bio = models.TextField('О себе', blank=True)
    role = models.CharField('Роль', choices=ROLE_CHOICES, max_length=9,
                            default=_USER)
    confirmation_code = models.CharField('Код подтверждения', max_length=128,
                                         null=True, blank=True)

    @property
    def is_user(self):
        return self.role == self._USER

    @property
    def is_moderator(self):
        return self.role == self._MODERATOR

    @property
    def is_admin(self):
        return self.role == self._ADMIN

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self._ADMIN
        super().save(*args, **kwargs)

    def send_mail_with_confirmation_code(self):
        """Отправить пользователю письмо с кодом подтверждения."""
        confirmation_code = self.generate_confirmation_code()
        msg_plain = render_to_string(
            'users/email/confirmation_code_when_signup.txt',
            {'username': self.username,
             'confirmation_code': confirmation_code})
        msg_html = render_to_string(
            'users/email/confirmation_code_when_signup.html',
            {'username': self.username,
             'confirmation_code': confirmation_code})
        send_mail('Добро пожаловать!',
                  msg_plain,
                  DEFAULT_FROM_EMAIL,
                  (self.email,),
                  html_message=msg_html,
                  fail_silently=False, )

    def generate_confirmation_code(self):
        """Генерируем случайный код для получения токена по API V1."""
        confirmation_code = uuid.uuid4()
        self.confirmation_code = make_password(confirmation_code)
        self.save()
        return confirmation_code

    def get_token(self):
        """Обновляем токен авторизации по API V1 для пользователя."""
        return str(RefreshToken.for_user(self).access_token)
