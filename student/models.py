from django.db import models
from django.utils import timezone


class StudentModel(models.Model):
    '''Model definition for StudentModel.'''
    student_first_name = models.TextField()
    student_last_name = models.TextField(null=True)
    class_rollno = models.IntegerField()
    email = models.EmailField(null=True)
    phone_no = models.CharField(max_length=15)
    profile_image = models.URLField()
    courses = models.IntegerField(null=True)
    department = models.IntegerField(null=True)
    classes = models.IntegerField(null=True)
    attendance = models.IntegerField(null=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for StudentModel.'''

        verbose_name = 'student'
        verbose_name_plural = 'students'

    def __str__(self):
        '''Unicode representation of StudentModel.'''
        return self.student_name
