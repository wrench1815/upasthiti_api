from django.contrib import admin

from .models import StudentModel


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    '''Admin View for StudentModel'''

    list_display = [
        'student_name',
        'class_rollno',
        'created_on',
    ]

    search_fields = [
        'student_first_name',
        'student_last_name',
        'class_rollno',
    ]

    def student_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
