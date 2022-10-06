from django_filters import rest_framework as filters

from .models import AttendanceModel


class AttendanceFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = AttendanceModel
        fields = [
            'date',
            'is_present',
            'is_late',
            'is_absent',
        ]
