import django_filters
from olx_website import models
from django_filters import DateFilter, NumberFilter, CharFilter
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderFilters(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label='Description')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    class Meta:
        model = models.Item
        fields = '__all__'
        exclude = ['image', 'is_sold', 'created_by', 'created_at', 'price']
