from rest_framework import serializers
from . import models


class CourseFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display course data
        
    '''

    class Meta:
        model = models.CourseModel
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    '''
        serializer to add and edit data
    '''
    class Meta:
        model = models.CourseModel
        exclude = [
            'pk',
            'created_on',
        ]
    # todo: add validation
    def validate(self, attrs):
        return super().validate(attrs)
