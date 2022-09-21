from rest_framework import serializers
from . import models


class StudentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display Student Data
    '''

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

    # Todo: janch partal(valaidation)
    def validate(self, attrs):
        return super().validate(attrs)
