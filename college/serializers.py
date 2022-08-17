from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models
from university import models as uni_models

User = get_user_model()

##############################################################################################
# Start:Nested Serialisers
##############################################################################################

USER_FIELDS = [
    'id',
    'email',
    'first_name',
    'last_name',
    'full_name',
    'short_name',
    'profile_image',
    'profile_image_public_id',
    'gender',
    'mobile',
    'address',
    'district',
    'date_added',
    'is_admin',
    'is_principal',
    'is_hod',
    'is_teacher',
    'is_active',
]


class CollegeHODSerializer(serializers.ModelSerializer):
    '''
        Nested HODSerializer for College
    '''

    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    class Meta:
        model = User
        fields = USER_FIELDS


class CollegePrincipalSerializer(serializers.ModelSerializer):
    '''
        Nested PrincipalSerializer for College
    '''
    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    class Meta:
        model = User
        fields = USER_FIELDS


class CollegeUniSerializer(serializers.ModelSerializer):
    '''
        Nested UniversitySerializer for College
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


class CollegeSerializer(serializers.ModelSerializer):
    '''
        Serializer to Display College Data
    '''

    hod = CollegeHODSerializer(many=True)
    principal = CollegePrincipalSerializer()
    university = CollegeUniSerializer()

    class Meta:
        model = models.CollegeModel
        fields = '__all__'


class CollegeCreateUpdateSerializer(serializers.ModelSerializer):
    '''
        Serializer to Create and Update College
    '''

    class Meta:
        model = models.CollegeModel
        exclude = [
            'created_on',
            'hod',
        ]
