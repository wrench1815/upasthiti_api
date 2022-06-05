from django.contrib import admin

from .models import DepartmentModel


@admin.register(DepartmentModel)
class DepartmentModelAdmin(admin.ModelAdmin):
    '''Admin View for DepartmentModel'''

    list_display = [
        'department_code',
        'department_name',
        'programmes_offered',
    ]

    search_fields = [
        'department_name',
        'department_code',
    ]
