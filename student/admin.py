from django.contrib import admin

from .models import StudentModel


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    '''Admin View for StudentModel'''

    list_display = [
        'university_rollno',
        'first_name',
        'last_name',
        'created_on',
    ]

    search_fields = [
        'university_rollno',
        'first_name',
        'last_name',
        'class_rollno',
    ]

    # def student_name(self, obj):
    #     return '{} {}'.format(obj.first_name, obj.last_name)
