from rest_framework import serializers

from . import models
from student.serializers import StudentFullSerializer
from classes.serializers import ClassFullSerializer


class AttendanceFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display Attendance Data   
    '''

    student = StudentFullSerializer()
    for_class = ClassFullSerializer()

    class Meta:
        model = models.AttendanceModel
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Attendance Data   
    '''

    class Meta:
        model = models.AttendanceModel
        exclude = [
            'created_on',
        ]


class AttendanceListSerializer(serializers.ListSerializer):
    '''
        Child List Serializer to create a list of Attendances.
        To be used to create Attendances in Bulk.
    '''

    def create(self, validated_data):
        attendance_list = [
            models.AttendanceModel(**item) for item in validated_data
        ]
        return models.AttendanceModel.objects.bulk_create(attendance_list)


class AttendanceBulkSerializer(serializers.ModelSerializer):
    '''
        Serializer to create Attendances in Bulk. 
    '''

    class Meta:
        #? Nesting Serializer
        list_serializer_class = AttendanceListSerializer
        model = models.AttendanceModel
        exclude = [
            'created_on',
        ]
