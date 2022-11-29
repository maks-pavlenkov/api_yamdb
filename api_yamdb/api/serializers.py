from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Genre, GenreTitle, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleGetSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        print(genres)
        for genre in genres:
            genre_obj = get_object_or_404(Genre, slug=genre['slug'])
            GenreTitle.objects.create(genre=genre_obj, title=title)
        category_obj = get_object_or_404(Category, slug=category['slug'])
        title = Title.objects.create(
            genre=GenreTitle.genre,
            category=category_obj,
            **validated_data
        )
        return title


class TitlePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate(self, data):
        title_year = data['year']
        current_year = date.today().year
        if title_year > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return data
