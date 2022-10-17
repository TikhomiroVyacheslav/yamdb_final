from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q
from reviews.validators import validate_title_year

User = get_user_model()


class Category(models.Model):
    """Таблица категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Таблица жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Таблица произведений."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[validate_title_year]

    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
        verbose_name='Жанр'
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='Описание'
    )
    rating = models.IntegerField(
        'Рейтинг',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Таблица отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        'Оценка'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            CheckConstraint(check=Q(score__range=(1, 10)), name='valid_score'),
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review_model'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Отзыв на {self.title.name}'


class Comment(models.Model):
    """Таблица комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.review.pk}, {self.author.username}'


class GenreTitle(models.Model):
    """Вспомогательная таблица жанр/произведение."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
