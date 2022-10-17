from api.permissions import IsAdminOnlyPermission
from api.serializers.users import UserMeSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnlyPermission,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(methods=('GET', 'PATCH'), detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = UserMeSerializer(request.user, data=request.data,
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
