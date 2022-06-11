from django.contrib import admin

from .models import StudentModel


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    '''Admin View for StudentModel'''

    list_display = [
        'student_name',
        'class_rollno',
        'batch',
    ]

    search_fields = [
        'student_name',
        'class_rollno',
    ]
