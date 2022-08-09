from rest_framework import serializers

from .models import UniversityModel
from college.models import CollegeModel
from college import serializers as college_serializers


##############################################################################################
# Start:Nested Serialisers
##############################################################################################
class UniCollegeSerializer(serializers.ModelSerializer):
    '''
        Nested CollegeSerializer for University
    '''

    hod = college_serializers.CollegeHODSerializer(many=True)
    principal = college_serializers.CollegePrincipalSerializer()

    class Meta:
        model = CollegeModel
        exclude = ['university']


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class UniversitySerializer(serializers.ModelSerializer):
    '''
        Serializer for LIsting University Data
    '''

    college_affiliated = UniCollegeSerializer(
        source='get_college_affiliated',
        many=True,
    )
    college_affiliated_count = serializers.IntegerField(
        source='get_college_affiliated_count')

    class Meta:
        model = UniversityModel
        fields = [
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
            'college_affiliated',
            'college_affiliated_count',
        ]


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
            'district',
            'phone_number',
            'logo',
            'logo_public_id',
            'vice_chancelor',
        ]
