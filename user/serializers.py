from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer for User
    '''

    class Meta:
        model = User
        exclude = [
            'is_staff',
            'is_superuser',
            'groups',
            'password',
            'last_login',
            'user_permissions',
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
