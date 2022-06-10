from django.db import models
from django.utils import timezone


# Create your models here.
class CourseModel(models.Model):
    '''Model definition for course.'''

    course_name = models.TextField()
    course_code = models.CharField(max_length=50)
    teacher_assigned = models.IntegerField()
    is_practical = models.BooleanField(default=False)
    classes = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for course.'''

        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        '''Unicode representation of course.'''
        return self.course_name
