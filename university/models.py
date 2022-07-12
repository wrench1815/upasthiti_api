from django.db import models

from django.utils import timezone


class UniversityModel(models.Model):
    '''Model definition for UniversityModel.'''

    name = models.TextField()
    address = models.TextField()
    alias = models.CharField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for UniversityModel.'''

        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        '''Unicode representation of UniversityModel.'''
        return str(self.name)
