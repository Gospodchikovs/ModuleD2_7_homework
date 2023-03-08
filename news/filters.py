from django_filters import FilterSet,  DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


class PostFilter(FilterSet):
    date_create = DateFilter(field_name='time_create', lookup_expr='date__gt', input_formats=['%d-%m-%Y', '%d/%m/%Y'])

    class Meta:
        model = Post
        fields = {'heading': ['icontains'], 'author': ['in']}
