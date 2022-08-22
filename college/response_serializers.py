from rest_framework import serializers

from api.utils import DISTRICTS_CHOICES


class ResponseCollegeCreateSerializer(serializers.Serializer):
    '''
        Response Serializer for College Creation
    '''
    id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField()
    district = serializers.ChoiceField(DISTRICTS_CHOICES)
    alias_name = serializers.CharField()
    logo = serializers.URLField()
    logo_public_id = serializers.CharField()
    website = serializers.URLField()
    mobile = serializers.CharField()
    email = serializers.EmailField()
    university = serializers.IntegerField()
    principal = serializers.IntegerField()
