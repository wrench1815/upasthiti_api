from django.contrib import admin

from .models import ClassModel


@admin.register(ClassModel)
class ClassModelAdmin(admin.ModelAdmin):
    '''Admin View for ClassModel'''

    list_display = [
        'name',
        'code',
        'session_start',
        'session_end',
    ]
    list_filter = [
        'code',
        'session_start',
    ]

    search_fields = [
        'name',
        'code',
    ]
    ordering = [
        '-created_on',
    ]
