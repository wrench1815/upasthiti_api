from django.db import models
from django.utils import timezone

from university.models import UniversityModel


class CourseModel(models.Model):
    '''Model definition for course.'''

    title = models.TextField()
    code = models.CharField(
        max_length=15,
        unique=True,
    )
    university = models.ForeignKey(
        UniversityModel,
        on_delete=models.CASCADE,
    )
    is_practical = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for course.'''

        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        '''Unicode representation of course.'''
        return self.title
