from rest_framework import serializers
from . import models


class DepartmentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display Department Data
    '''

    class Meta:
        model = models.DepartmentModel
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Department Data
    '''

    class Meta:
        model = models.DepartmentModel
        exclude = [
            'created_on',
        ]

    # Todo : janch partal(validation)
    def validate(self, attrs):
        return super().validate(attrs)
