from rest_framework import serializers

from .models import ContactModel


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactModel
        fields = '__all__'


class ContactCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'contact_district',
            'message',
        ]
