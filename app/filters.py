import django_filters
from .models import Tracetoplantation


class TracetoplantationFilter(django_filters.FilterSet):
    mill_eq_id = django_filters.CharFilter(field_name='mill_eq_id')

    class Meta:
        model = Tracetoplantation
        fields = ['mill_eq_id', ]
