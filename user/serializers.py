from dataclasses import fields
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from college.models import CollegeModel

User = get_user_model()

##############################################################################################
# Start:Nested Serialisers
##############################################################################################


class PrincipalCollegeSerializer(serializers.ModelSerializer):
    '''
        Nested College Serializer for User objects
    '''

    class Meta:
        model = CollegeModel
        exclude = [
            'hod',
            'principal',
        ]


class HODCollegeSerializer(serializers.ModelSerializer):
    '''
        Nested College Serializer for User objects
    '''

    class Meta:
        model = CollegeModel
        exclude = [
            'hod',
        ]


##############################################################################################
# End:Nested Serialisers
##############################################################################################


class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer for User
    '''
    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    college = HODCollegeSerializer(many=True, read_only=True)
    administrated_college = PrincipalCollegeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'full_name',
            'short_name',
            'email',
            'gender',
            'date_added',
            'is_active',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
            'college',
            'administrated_college',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    '''
        Serializer for User Creation
    '''
    password = serializers.CharField(
        min_length=8,
        max_length=16,
    )
    confirm_password = serializers.CharField(
        min_length=8,
        max_length=16,
    )

    class Meta:
        model = User
        fields = [
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'password',
            'confirm_password',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
        ]

    def validate_password(self, value):
        #? check if password is minimum 8 digit long
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long")

        #? check if password contains atleast 1 number
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one number")

        #? check if password contains atleast 1 capital letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one capital letter")

        #? check if password contains atleast 1 small letter
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one small letter")

        #? check if password contains atleast 1 special character
        if not any(char in '!@#$%^&*()_+' for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character")

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'error': 'Confirm Password does not match Password'})

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    '''
        Serializer for User Update
    '''

    class Meta:
        model = User
        fields = [
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
        ]


class UserPasswordSerializer(serializers.Serializer):
    '''
        Serializer to Update User Password
    '''

    password = serializers.CharField(min_length=8,
                                     max_length=16,
                                     validators=[validate_password])
    confirm_password = serializers.CharField(min_length=8,
                                             max_length=16,
                                             validators=[validate_password])

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'error': 'Confirm Password does not match Password'})

        return attrs


class HODSerializer(serializers.ModelSerializer):
    '''
        Serializer for listing HODs
    '''
    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    college = HODCollegeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'full_name',
            'short_name',
            'email',
            'gender',
            'date_added',
            'is_active',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
            'college',
        ]


class PrincipalSerializer(serializers.ModelSerializer):
    '''
        Serializer for listing Principals
    '''
    # get full name from model User
    full_name = serializers.CharField(source='get_full_name')

    # get short name from model User
    short_name = serializers.CharField(source='get_short_name')

    administrated_college = PrincipalCollegeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'profile_image',
            'profile_image_public_id',
            'first_name',
            'last_name',
            'full_name',
            'short_name',
            'email',
            'gender',
            'date_added',
            'is_active',
            'is_admin',
            'is_principal',
            'is_hod',
            'is_teacher',
            'administrated_college',
        ]
