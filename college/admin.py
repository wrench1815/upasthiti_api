from django.contrib import admin

from .models import CollegeModel


@admin.register(CollegeModel)
class CollegeModelAdmin(admin.ModelAdmin):
    '''Admin View for CollegeModel'''

    list_display = [
        'name',
        'alias_name',
        'principal',
    ]

    search_fields = [
        'name',
    ]
