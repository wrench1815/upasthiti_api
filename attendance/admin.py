from django.contrib import admin

from .models import AttendanceModel


@admin.register(AttendanceModel)
class AttendanceModelAdmin(admin.ModelAdmin):
    '''Admin View for AttendanceModel'''

    list_display = [
        'student',
        'date',
        'is_present',
        'is_absent',
        'is_late',
    ]

    ordering = [
        'date',
    ]
