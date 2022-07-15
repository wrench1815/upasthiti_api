from rest_framework import serializers

from .models import UniversityModel


class UniversitySerializer(serializers.ModelSerializer):
    '''
        Serializer for LIsting University Data
    '''

    class Meta:
        model = UniversityModel
        fields = '__all__'


class UniversityCreateSerializer(serializers.ModelSerializer):
    '''
        Serializer for Editing and creating a new University
    '''

    class Meta:
        model = UniversityModel
        fields = [
            'name',
            'address',
            'alias',
            'email',
            'phone_number',
            'logo',
            'logo_public_id',
            'vice_chancelor',
        ]
