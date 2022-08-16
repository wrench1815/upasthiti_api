from django.contrib import admin

from .models import ContactModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    '''Admin View for ContactModel'''

    list_display = [
        'first_name',
        'email',
        'date_added',
    ]
    list_filter = [
        'contact_district',
    ]
    ordering = [
        '-date_added',
    ]
