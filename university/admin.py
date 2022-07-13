from django.contrib import admin

from .models import UniversityModel


@admin.register(UniversityModel)
class UniversityModelAdmin(admin.ModelAdmin):
    '''Admin View for UniversityModel'''

    list_display = [
        'name',
        'address',
        'alias',
    ]
