from dataclasses import fields
from rest_framework import serializers

from .models import UniversityModel


class UniversitySerializer(serializers.Serializer):
    '''
        Serializer for LIsting University Data
    '''

    class Meta:
        model = UniversityModel
        fields = '__all__'


class UniversityCreateSerializer(serializers.Serializer):
    '''
        Serializer for LIsting University Data
    '''

    class Meta:
        model = UniversityModel
        fields = [
            'name',
            'address',
            'alias',
        ]
