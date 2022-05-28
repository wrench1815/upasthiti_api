from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer for User List and Detail
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
        Serializer for User Creation, Update
    '''
    password = serializers.CharField(min_length=8,
                                     max_length=16,
                                     validators=[validate_password])
    confirm_password = serializers.CharField(min_length=8,
                                             max_length=16,
                                             validators=[validate_password])

    class Meta:
        model = User
        fields = [
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
