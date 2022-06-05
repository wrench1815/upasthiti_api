from django.contrib import admin

from .models import TeacherModel


@admin.register(TeacherModel)
class TeacherModelAdmin(admin.ModelAdmin):
    '''Admin View for TeacherModel'''

    list_display = [
        'teacher_name',
        'teacher_department',
    ]

    search_fields = [
        'teacher_name',
    ]
