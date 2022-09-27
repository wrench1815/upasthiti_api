from rest_framework import serializers

from . import models
from university.models import UniversityModel
from college.models import CollegeModel

##############################################################################################
# Start:Nested Serialisers
##############################################################################################


class UniversitySerializer(serializers.ModelSerializer):
    '''
        Serializer for LIsting University Data
    '''

    class Meta:
        model = UniversityModel
        fields = [
            'id',
            'name',
            'address',
            'alias',
            'district',
            'email',
            'phone_number',
            'website',
            'logo',
            'logo_public_id',
            'vice_chancelor',
            'date_added',
        ]


class CollegeSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display College Data
    '''
    university = UniversitySerializer()

    class Meta:
        model = CollegeModel
        exclude = [
            'hod',
            'teacher',
        ]


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class StudentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display Student Data
    '''

    college = CollegeSerializer()

    class Meta:
        model = models.StudentModel
        fields = '__all__'


class StudentCreateUpdateSerializerFull(serializers.ModelSerializer):
    '''
        Serializer to create and edit Student
    '''

    class Meta:
        model = models.StudentModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobile',
            'address',
            'district',
            'profile_image',
            'profile_image_public_id',
            'gender',
            'college',
            'class_roll_no',
            'university_roll_no',
        ]


#TODO: implement if possible
class StudentBulkSerializer(serializers.ListSerializer):
    '''
        Parent Serializer for studentSerializer 
        Used for Bulk Posting objects
    '''

    def create(self, validated_data):

        studentlist = [models.StudentModel(**item) for item in validated_data]
        return models.StudentModel.objects.bulk_create(studentlist)


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    '''
        Serializer to create and edit Student
    '''

    class Meta:
        model = models.StudentModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobile',
            'address',
            'district',
            'profile_image',
            'profile_image_public_id',
            'gender',
        ]


class StudentSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Student Data
    '''

    class Meta:
        #? Nesting Serializer
        list_serializer_class = StudentBulkSerializer
        model = models.StudentModel
        exclude = [
            'created_on',
        ]
        optional_fields = [
            'courses',
            'department',
            'classes',
            'attendance ',
        ]
