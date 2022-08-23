from rest_framework import serializers

from . import models

from university import models as uni_models

##############################################################################################
# Start:Nested Serialisers
##############################################################################################


class CourseUniSerializer(serializers.ModelSerializer):
    '''
        Nested University Serializer for Course
    '''

    class Meta:
        model = uni_models.UniversityModel
        fields = [
            'id',
            'name',
            'address',
            'alias',
            'district',
            'email',
            'phone_number',
            'logo',
            'logo_public_id',
            'vice_chancelor',
            'date_added',
        ]


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class CourseFullSerializer(serializers.ModelSerializer):
    '''
        Serializer to display course data
        
    '''
    university = CourseUniSerializer()

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
            'created_on',
        ]
