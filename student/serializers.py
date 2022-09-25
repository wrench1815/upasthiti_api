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

    class Meta:
        model = models.CollegeModel
        # fields = '__all__'
        exclude = [
            'hod',
            'teacher',
        ]


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class UniversityRollNoSerializer(serializers.Serializer):
    '''
        Nested Serializer for University Roll no
    '''

    university = UniversitySerializer()
    university_roll_no = serializers.CharField()
    created_on = serializers.DateTimeField()

    class Mets:
        model = models.UniversityRollNo
        fields = '__all__'


class CollegeRollNoSerializer(serializers.Serializer):
    '''
        Nested Serializer for College Roll no
    '''

    college = CollegeSerializer()
    class_roll_no = serializers.CharField()
    created_on = serializers.DateTimeField()

    class Mets:
        model = models.CollegeRollNo
        fields = '__all__'


class StudentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display Student Data
    '''

    college = CollegeRollNoSerializer(many=True)
    university = UniversityRollNoSerializer(many=True)

    class Meta:
        model = models.StudentModel
        fields = '__all__'


class StudentBulkSerializer(serializers.ListSerializer):
    '''
        Parent Serializer for studentSerializer 
        Used for Bulk Posting objects
    '''

    def create(self, validated_data):

        studentlist = [models.StudentModel(**item) for item in validated_data]
        return models.StudentModel.objects.bulk_create(studentlist)


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
