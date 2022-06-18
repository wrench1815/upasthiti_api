from rest_framework import serializers
from . import models


class DepartmentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display Department Data
    '''
    department_name = serializers.CharField(
        source='department_name.department_name')

    class Meta:
        model = models.DepartmentModel
        fields = '__all__'
        depth = 1


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


class DepartmentTypeSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Department Type Data
    '''

    class Meta:
        model = models.DepartmentTypeModel
        exclude = [
            'created_on',
        ]


class DepartmentTypeFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add, Edit and List Department Type Data
    '''

    class Meta:
        model = models.DepartmentTypeModel
        fields = '__all__'
