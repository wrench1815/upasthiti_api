from django.db import models

from django.utils import timezone

from api.utils import DISTRICTS_CHOICES


class UniversityModel(models.Model):
    '''Model definition for UniversityModel.'''

    name = models.TextField(unique=True)
    address = models.TextField(blank=True, null=True)
    alias = models.CharField(max_length=10)
    district = models.CharField(
        choices=DISTRICTS_CHOICES,
        max_length=11,
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    logo_public_id = models.TextField(blank=True, null=True)
    vice_chancelor = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for UniversityModel.'''

        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        '''Unicode representation of UniversityModel.'''
        return str(self.name)
