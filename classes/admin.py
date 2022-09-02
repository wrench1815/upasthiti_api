from django.contrib import admin

from .models import ClassesModel


@admin.register(ClassesModel)
class ClassesModelAdmin(admin.ModelAdmin):
    '''Admin View for ClassesModel'''

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
