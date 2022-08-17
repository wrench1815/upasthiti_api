from django_filters import rest_framework as filters

from .models import DepartmentTypeModel


class DepartmentTypeFilter(filters.FilterSet):
    unassigned = filters.BooleanFilter(field_name='department',
                                       lookup_expr='isnull')

    class Meta:
        model = DepartmentTypeModel
        fields = []
