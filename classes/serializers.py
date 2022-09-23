from rest_framework import serializers
from . import models


class ClassFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display class data
    '''

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

    # Todo: validation
    def validate(self, attrs):
        return super().validate(attrs)
