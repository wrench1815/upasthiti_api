from rest_framework import serializers
from . import models


class StudentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display Student Data
    '''

    class Meta:
        model = models.StudentModel
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Student Data
    '''

    class Meta:
        model = models.StudentModel
        exclude = [
            'created_on',
        ]

    # Todo: janch partal(valaidation)
    def validate(self, attrs):
        return super().validate(attrs)
