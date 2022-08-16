from django.db import models
from django.utils import timezone

from api.utils import DISTRICTS_CHOICES_WITH_NONE


class ContactModel(models.Model):
    """Model definition for ContactModel."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    contact_district = models.CharField(
        choices=DISTRICTS_CHOICES_WITH_NONE,
        max_length=20,
    )
    message = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for ContactModel."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of ContactModel."""
        return f'{self.first_name} {self.last_name}'
