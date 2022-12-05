import os

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import data_validation


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'static/data/users.csv'
        )
        required_fields_users = [
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        ]
        data = data_validation(user_path, required_fields_users)
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
        required_fields_genres = [
            'id',
            'name',
            'slug'
        ]
        data = data_validation(genres_path, required_fields_genres)
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
        required_fields_categories = [
            'id',
            'name',
            'slug'
        ]
        data = data_validation(categories_path, required_fields_categories)
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
        required_fields_titles = [
            'id',
            'name',
            'year',
            'category'
        ]
        data = data_validation(titles_path, required_fields_titles)
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
        required_fields_genre_title = [
            'id',
            'title_id',
            'genre_id'
        ]
        data = data_validation(genre_title_path, required_fields_genre_title)
        for row in data[1:]:
            title = Title.objects.get(id=row[1])
            genre = Genre.objects.get(id=row[2])
            title.genre.add(genre)
        review_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'static/data/review.csv'
        )
        required_fields_review = [
            'id',
            'title_id',
            'text',
            'author',
            'score',
            'pub_date'
        ]
        data = data_validation(review_path, required_fields_review)
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
        required_fields_comments = [
            'id',
            'review_id',
            'text',
            'author',
            'pub_date'
        ]
        data = data_validation(comments_path, required_fields_comments)
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
