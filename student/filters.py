from django_filters import rest_framework as filters

from .models import StudentModel


class StudentFilter(filters.FilterSet):
    classs = filters.NumberFilter(
        field_name='class_student__id',
        lookup_expr='exact',
        label='Filter Student of given Class',
    )

    class Meta:
        model = StudentModel
        fields = ['college']
