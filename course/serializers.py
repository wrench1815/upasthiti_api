from rest_framework import serializers
from . import models


class CourseFullSerializer(serializers.ModelSerializer):
    '''
        
    '''

    class Meta:
        model = models.CourseModel
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CourseModel
        fields = '__all__'
