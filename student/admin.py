from django.contrib import admin

from .models import StudentModel, CollegeRollNo, UniversityRollNo


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
    '''Admin View for StudentModel'''

    list_display = [
        # 'university',
        'first_name',
        'last_name',
        'created_on',
    ]

    search_fields = [
        # 'university',
        'first_name',
        'last_name',
        'class_rollno',
    ]


    # def student_name(self, obj):
    #     return '{} {}'.format(obj.first_name, obj.last_name)
@admin.register(UniversityRollNo)
class UniversityRollNoAdmin(admin.ModelAdmin):
    '''Admin View for UniversityRollNo'''

    list_display = [
        'university_roll_no',
    ]

    search_fields = [
        'university_roll_no',
    ]


@admin.register(CollegeRollNo)
class CollegeRollNoAdmin(admin.ModelAdmin):
    '''Admin View for CollegeRollNo'''

    list_display = [
        'class_roll_no',
    ]

    search_fields = [
        'class_roll_no',
    ]
