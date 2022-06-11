from django.contrib import admin

from .models import CourseModel


@admin.register(CourseModel)
class CourseModelAdmin(admin.ModelAdmin):
    '''Admin View for CourseModel'''

    list_display = [
        'course_name',
        'course_code',
        'is_practical',
    ]

    search_fields = [
        'course_name',
        'course_code',
    ]
