from django.db import models
from django.utils import timezone


class CollegeModel(models.Model):
    '''
        Model Definistion for CollegeModel
    '''
    institute_name = models.TextField()
    institute_address = models.TextField()
    institute_alias_name = models.TextField()
    #todo: discussion about this field
    #TODO: Add relations
    institute_principal = models.IntegerField()
    institute_logo = models.URLField()
    institute_website = models.URLField()
    institute_mobile = models.CharField(max_length=15)
    institute_email = models.EmailField(
        ('email address'),
        blank=True,
    )
    location =models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''
            Meta definition for CollegeModel.
        '''
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        '''Unicode representation of MODELNAME.'''
        return str(self.institute_name)
