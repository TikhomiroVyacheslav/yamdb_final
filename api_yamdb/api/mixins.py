from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnlyPermission


class ListPostDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnlyPermission,)
    lookup_field = 'slug'
