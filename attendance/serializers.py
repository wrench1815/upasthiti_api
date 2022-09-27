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
