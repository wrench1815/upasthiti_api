from rest_framework import serializers
from . import models


class AttendanceFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display Attendance Data   
    '''

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
            'pk',
            'created_on',
        ]
    
    # todo: janch partal(validation)
    def validate(self, attrs):
        return super().validate(attrs)
