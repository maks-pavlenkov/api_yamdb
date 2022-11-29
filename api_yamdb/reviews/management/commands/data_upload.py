import csv
import os

from django.core.management import BaseCommand
from reviews.models import Category, Genre, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        genres_path = os.path.join(
                                os.path.abspath(os.path.dirname('manage.py')),
                                'static/data/genre.csv'
                                )
        with open(genres_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                Genre.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        categories_path = os.path.join(
                                os.path.abspath(os.path.dirname('manage.py')),
                                'static/data/category.csv'
                                )
        with open(categories_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                Category.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        titles_path = os.path.join(
                                os.path.abspath(os.path.dirname('manage.py')),
                                'static/data/titles.csv'
                                )
        with open(titles_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3]
                )
        genre_title_path = os.path.join(
                                os.path.abspath(os.path.dirname('manage.py')),
                                'static/data/genre_title.csv'
                                )
        with open(genre_title_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                title = Title.objects.get(id=row[1])
                genre = Genre.objects.get(id=row[2])
                title.genre.add(genre)
