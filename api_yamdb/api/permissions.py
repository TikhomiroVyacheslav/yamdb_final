from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnlyPermission(BasePermission):
    """
    Читать можно всем, остальное только админу.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsStaffOrAuthorOrWriteAuthOrReadOnlyPermission(BasePermission):
    """
    Читать можно всем, добавлять авторизованным,
    остальное автору/модератору/админу.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user or request.user.is_admin
                or request.user.is_moderator)


class IsAdminOnlyPermission(BasePermission):
    """
    Доступ только администратору.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
