from api.validators import validate_score
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        many=True,
        required=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор отдельно для списка произведений."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',
                  'rating'
                  )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        user = self.context.get('request').user
        score = data.get('score')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = title.reviews.all()
        if validate_score(score):
            if self.context.get('request').method == 'POST':
                if reviews.filter(author=user).exists():
                    raise serializers.ValidationError(
                        'Вы можете оставлять только 1 отзыв к произведению.'
                    )
                return data
            return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
