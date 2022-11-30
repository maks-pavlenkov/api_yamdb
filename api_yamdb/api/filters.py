import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genres = django_filters.CharFilter(
        name='genres__name',
        lookup_type='contains',
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')