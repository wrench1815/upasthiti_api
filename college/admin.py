from django.contrib import admin

from .models import CollegeModel


@admin.register(CollegeModel)
class CollegeModelAdmin(admin.ModelAdmin):
    '''Admin View for CollegeModel'''

    list_display = [
        'institute_name',
        'institute_alias_name',
        'institute_type',
        'institute_principal',
    ]

    search_fields = [
        'institute_name',
    ]
