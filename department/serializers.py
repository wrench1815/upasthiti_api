from rest_framework import serializers

from . import models
from college import serializers as college_serializers
from college.models import CollegeModel

DEPARTMENT_FIELDS = [
    'id',
    'name',
    'hod',
    'teacher',
    'course',
    'college',
    'created_on',
]

##############################################################################################
# Start:Nested Serialisers
##############################################################################################


class DeptCollegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollegeModel
        exclude = [
            'university',
            'principal',
            'hod',
        ]


DeptHODSerializer = college_serializers.CollegeHODSerializer


class DeptNameRelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DepartmentTypeModel
        fields = '__all__'


##############################################################################################
# End:Nested Serialisers
##############################################################################################


##############################################################################################
# Department Serializers
class DepartmentFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display Department Data
    '''
    name = serializers.CharField(source='name.department_name')
    name_rel = DeptNameRelSerializer(source='name')
    hod = DeptHODSerializer()
    college = DeptCollegeSerializer()

    class Meta:
        model = models.DepartmentModel
        fields = DEPARTMENT_FIELDS + [
            'name_rel',
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    '''
        Serializer to Add and Edit Department Data
    '''

    class Meta:
        model = models.DepartmentModel
        exclude = [
            'created_on',
        ]


##############################################################################################
# Department Type Serializers


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
