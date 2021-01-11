import django_filters
from robot import models


class CSVCollectionFilter(django_filters.FilterSet):
    class Meta:
        model = models.CSVCollection
        fields = {'name': ['exact']}
