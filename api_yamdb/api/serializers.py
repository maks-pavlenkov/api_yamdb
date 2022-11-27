from datetime import date

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(read_only=True, many=True)
    category = serializers.StringRelatedField(read_only=True)
    description = serializers.StringRelatedField(required=False)

    class Meta:
        fields = '__all__'
        model = Title

    # def validate(self):
    #     title_year = int(self.context['year'])
    #     current_year = date.today().year
    #     if title_year > current_year:
    #         raise serializers.ValidationError(
    #             'Нельзя добавлять произведения, которые еще не вышли!'
    #         )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)
