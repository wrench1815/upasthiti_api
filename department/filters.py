from django_filters import rest_framework as filters

from .models import DepartmentTypeModel


class DepartmentTypeFilter(filters.FilterSet):

    #? Exclude college passed from lookup
    exclude_college = filters.NumberFilter(
        field_name='department__college',
        lookup_expr='exact',
        exclude=True,
    )

    class Meta:
        model = DepartmentTypeModel
        fields = []
