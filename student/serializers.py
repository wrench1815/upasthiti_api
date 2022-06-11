from rest_framework import serializers
from . import models


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentModel
        fields = '__all__'
