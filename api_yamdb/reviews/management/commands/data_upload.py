import csv
import os

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'static/data/users.csv'
        )
        with open(user_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                User.objects.create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
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
        review_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'static/data/review.csv'
        )
        with open(review_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                title = Title.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Review.objects.create(
                    id=row[0],
                    title=title,
                    author=author,
                    text=row[2],
                    score=row[4],
                    pub_date=row[5]
                )
        comments_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'static/data/comments.csv'
        )
        with open(comments_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            for row in data[1:]:
                user = User.objects.get(id=row[3])
                review = Review.objects.get(id=row[1])
                Comment.objects.get_or_create(
                    id=row[0],
                    author=user,
                    review=review,
                    text=row[2],
                    pub_date=row[4]
                )
