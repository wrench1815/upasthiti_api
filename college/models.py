from django.db import models
from django.utils import timezone

from api.utils import DISTRICTS_CHOICES


class CollegeModel(models.Model):
    '''
        Model Definition for CollegeModel
    '''
    institute_name = models.TextField()
    institute_address = models.TextField()
    district = models.CharField(
        choices=DISTRICTS_CHOICES,
        max_length=11,
        blank=True,
        null=True,
    )
    institute_alias_name = models.TextField()
    institute_principal = models.IntegerField()
    institute_logo = models.URLField()
    institute_website = models.URLField()
    institute_mobile = models.CharField(max_length=15)
    institute_email = models.EmailField(
        ('email address'),
        blank=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''
            Meta definition for CollegeModel.
        '''
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        '''Unicode representation of MODELNAME.'''
        return str(self.institute_name)
