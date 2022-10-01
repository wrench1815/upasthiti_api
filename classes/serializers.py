from rest_framework import serializers

from django.contrib.auth import get_user_model

from . import models
from college.models import CollegeModel
from college import serializers as college_serializers
from department.models import DepartmentModel
from course.models import CourseModel

User = get_user_model()

##############################################################################################
# Start:Nested Serialisers
##############################################################################################


class NestedCollegeSerializer(serializers.ModelSerializer):
    '''
        Nested College Serializer for Class
    '''

    principal = college_serializers.CollegePrincipalSerializer()

    class Meta:
        model = CollegeModel
        exclude = [
            'hod',
            'teacher',
        ]


class NestedDepartmentSerializer(serializers.ModelSerializer):
    '''
        Nested Department Serializer for Class
    '''

    name = serializers.CharField(source='name.department_name')

    class Meta:
        model = DepartmentModel
        fields = '__all__'


class NestedCourseSerializer(serializers.ModelSerializer):
    '''
        Nested Course Serializer for Class
    '''

    # name = serializers.CharField(source='name.department_name')

    class Meta:
        model = CourseModel
        fields = '__all__'


class NestedTeacherSerializer(serializers.ModelSerializer):
    '''
        Nested Teacher Serializer for Class
    '''

    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    class Meta:
        model = User
        fields = [
            'id',
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'full_name',
            'short_name',
            'email',
            'mobile',
            'address',
            'district',
            'gender',
            'date_added',
            'is_active',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
        ]


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class ClassFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display class data
    '''

    college = NestedCollegeSerializer()
    department = NestedDepartmentSerializer()
    course = NestedCourseSerializer()
    teacher = NestedTeacherSerializer()

    class Meta:
        model = models.ClassModel
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and edit class data
    '''

    class Meta:
        model = models.ClassModel
        exclude = [
            'created_on',
        ]
