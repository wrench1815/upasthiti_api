from rest_framework import serializers

from . import models
from user.serializers import UserSerializer


class CollegeFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display College Data
    '''
    hod = UserSerializer(many=True)

    class Meta:
        model = models.CollegeModel
        fields = '__all__'
        depth = 1


class CollegeSerializer(serializers.ModelSerializer):
    '''
        Serializer to Create and Edit College
    '''

    class Meta:
        model = models.CollegeModel
        exclude = [
            'created_on',
        ]

    # todo: add validation
    def validate(self, attrs):
        return super().validate(attrs)
