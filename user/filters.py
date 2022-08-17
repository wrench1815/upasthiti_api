from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model

User = get_user_model()


class HODFilter(filters.FilterSet):
    unassigned = filters.BooleanFilter(
        field_name='college',
        lookup_expr='isnull',
        distinct=True,
    )

    #? Exclude college passed from lookup
    exclude_college = filters.NumberFilter(
        field_name='hod_department__college',
        lookup_expr='exact',
        exclude=True,
    )

    class Meta:
        model = User
        fields = ['college']
