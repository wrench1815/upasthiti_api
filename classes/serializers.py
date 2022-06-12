from rest_framework import serializers
from . import models


class ClassesFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display classes data
    '''

    class Meta:
        model = models.ClassesModel
        fields = '__all__'


class ClassesSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and edit classes data
    '''

    class Meta:
        model = models.ClassesModel
        exclude = [
            
            'created_on',
        ]

    # Todo: validation
    def validate(self, attrs):
        return super().validate(attrs)