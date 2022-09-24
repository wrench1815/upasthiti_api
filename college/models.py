from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from api.utils import DISTRICTS_CHOICES
from university.models import UniversityModel

User = get_user_model()


class CollegeModel(models.Model):
    '''
        Model Definition for CollegeModel
    '''
    name = models.TextField()
    address = models.TextField()
    district = models.CharField(
        choices=DISTRICTS_CHOICES,
        max_length=11,
        default='Jammu',
    )
    alias_name = models.TextField()
    logo = models.URLField()
    logo_public_id = models.TextField(blank=True, null=True)
    website = models.URLField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(
        ('email address'),
        blank=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    hod = models.ManyToManyField(User, related_name='college')
    teacher = models.ManyToManyField(User, related_name='college_teacher')
    university = models.ForeignKey(
        UniversityModel,
        on_delete=models.CASCADE,
        related_name='college',
        blank=True,
        null=True,
    )
    principal = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='administrated_college',
        blank=True,
        null=True,
    )

    class Meta:
        '''
            Meta definition for CollegeModel.
        '''
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        '''Unicode representation of CollegeModel.'''
        return str(self.name)
