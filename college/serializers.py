from rest_framework import serializers
from . import models


class CollegeFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add College
    '''

    class Meta:
        model = models.CollegeModel
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    '''
        Serializer to Create and Edit College
    '''
    class Meta:
        model = models.CollegeModel
        exclude = [
            'pk',
            'created_on',
        ]
    # todo: add validation
    def validate(self, attrs):
        return super().validate(attrs)
