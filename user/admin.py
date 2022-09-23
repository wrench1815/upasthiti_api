from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import UserForm

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    '''Admin View for User'''

    add_form = UserForm

    list_display = ['email', 'first_name', 'last_name']
    ordering = ['email']
    list_filter = [
        'is_active',
        'is_admin',
        'is_principal',
        'is_hod',
        'is_teacher',
    ]
    search_fields = ['first_name', 'last_name', 'email']

    #? fieldsets for viewing
    fieldsets = [
        [
            'Basic Info', {
                'fields': [
                    'profile_image',
                    'first_name',
                    'last_name',
                    'gender',
                    'email',
                    'mobile',
                    'district',
                    'address',
                    'password',
                ],
            }
        ],
        ['Dates', {
            'fields': [
                'date_added',
                'last_login',
            ]
        }],
        [
            'Permissions', {
                'fields': [
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'is_admin',
                    'is_principal',
                    'is_hod',
                    'is_teacher',
                ]
            }
        ],
        ['Groups', {
            'fields': [
                'groups',
            ]
        }],
    ]

    #? fieldsets for Creation
    add_fieldsets = [
        [
            'Basic Info', {
                'fields': [
                    'profile_image',
                    'first_name',
                    'last_name',
                    'gender',
                    'email',
                    'mobile',
                    'district',
                    'address',
                    'password',
                ]
            }
        ],
        ['Dates', {
            'fields': [
                'date_added',
                'last_login',
            ]
        }],
        [
            'Permissions', {
                'fields': [
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'is_admin',
                    'is_principal',
                    'is_hod',
                    'is_teacher',
                ]
            }
        ],
        ['Groups', {
            'fields': [
                'groups',
            ]
        }],
    ]
