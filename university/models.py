from django.db import models


class UniversityModel(models.Model):
    '''Model definition for UniversityModel.'''

    name = models.TextField()
    address = models.TextField()
    alias = models.CharField(max_length=10)

    class Meta:
        '''Meta definition for UniversityModel.'''

        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        '''Unicode representation of UniversityModel.'''
        return str(self.name)
