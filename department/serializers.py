from rest_framework import serializers
from . import models


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DepartmentModel
        fields = '__all__'
