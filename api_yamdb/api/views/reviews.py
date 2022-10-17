from api.filters import TitleFilter
from api.mixins import ListPostDeleteViewSet
from api.permissions import (IsAdminOrReadOnlyPermission,
                             IsStaffOrAuthorOrWriteAuthOrReadOnlyPermission)
from api.serializers.reviews import (CategorySerializer, CommentSerializer,
                                     GenreSerializer, ReviewSerializer,
                                     TitleListSerializer, TitleSerializer)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(ListPostDeleteViewSet):
    """Получение/создание/редактирование/удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListPostDeleteViewSet):
    """Получение/создание/редактирование/удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Получение/создание/редактирование/удаление произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def retrieve(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        serializer = TitleListSerializer(title)
        return Response(serializer.data)

    def create(self, request):
        serializer = TitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        serializer = TitleSerializer(title, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение/создание/редактирование/удаление отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrWriteAuthOrReadOnlyPermission,)

    def calculate_rating(self, title):
        """Пересчет рейтинга при создании/редактировании/удалении отзыва."""
        title.rating = round(
            title.reviews.aggregate(Avg('score')).get('score__avg')
        )
        title.save()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )

        self.calculate_rating(title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )

        self.calculate_rating(title=title)

    def perform_destroy(self, request):
        pk = self.kwargs.get('pk')
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        self.calculate_rating(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение/создание/редактирование/удаление комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrWriteAuthOrReadOnlyPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )
