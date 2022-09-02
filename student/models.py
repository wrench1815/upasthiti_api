from django.db import models
from django.utils import timezone

from api.utils import DISTRICTS_CHOICES


class StudentModel(models.Model):
    '''Model definition for StudentModel.'''
    first_name = models.TextField()
    last_name = models.TextField()
    class_rollno = models.IntegerField()
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    district = models.CharField(
        choices=DISTRICTS_CHOICES,
        max_length=11,
        default='Jammu',
    )
    profile_image = models.URLField()
    profile_image_public_id = models.TextField(
        blank=True,
        null=True,
    )
    courses = models.IntegerField(null=True)
    department = models.IntegerField(null=True)
    classes = models.IntegerField(null=True)
    attendance = models.IntegerField(null=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for StudentModel.'''

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self):
        '''
            return full name of the student
            format: '<student_first_name> <student_last_name>'
        '''
        return str(f'{self.first_name} {self.last_name}')
