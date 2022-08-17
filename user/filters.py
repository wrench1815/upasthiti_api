from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model

User = get_user_model()


class HODFilter(filters.FilterSet):
    unassigned = filters.BooleanFilter(
        field_name='college',
        lookup_expr='isnull',
    )

    class Meta:
        model = User
        fields = ['college']
