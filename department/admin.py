from django.contrib import admin

from .models import DepartmentModel


@admin.register(DepartmentModel)
class DepartmentModelAdmin(admin.ModelAdmin):
    '''Admin View for DepartmentModel'''

    list_display = [
        'department_name',
        'created_on',
    ]

    search_fields = [
        'department_name',
    ]
