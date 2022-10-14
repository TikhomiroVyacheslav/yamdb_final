import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

models_and_data = (
    (Category, 'static/data/category.csv'),
    (Genre, 'static/data/genre.csv'),
    (Title, 'static/data/titles.csv'),
    (GenreTitle, 'static/data/genre_title.csv'),
    (Review, 'static/data/review.csv'),
    (Comment, 'static/data/comments.csv'),
)


class Command(BaseCommand):
    help = 'Loads csv files in database.'

    def handle(self, *args, **options):
        # Кастомную модель User заполняем отдельно
        with open('static/data/users.csv', encoding='utf-8') as r_file:
            # Создаем объект reader, указываем символ-разделитель ","
            file_reader = csv.reader(r_file, delimiter=',')
            next(file_reader)
            for row in file_reader:
                User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                ).save()
            self.stdout.write(self.style.SUCCESS(
                f'Модель {User.__name__} успешно заполнена тестовыми данными.')
            )
        # Заполняем остальные модели в базе
        for model, path in models_and_data:
            with open(path, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=',')
                next(file_reader)
                for row in file_reader:
                    model(*row).save()
                self.stdout.write(self.style.SUCCESS(
                    (f'Модель {model.__name__} '
                     'успешно заполнена тестовыми данными.'))
                )
