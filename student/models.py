from django.db import models

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather not Say', 'Rather not Say'),
)


class StudentModel(models.Model):
    '''Model definition for StudentModel.'''

    student_name = models.TextField()
    class_rollno = models.IntegerField()
    batch = models.IntegerField()
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)

    class Meta:
        '''Meta definition for StudentModel.'''

        verbose_name = 'student'
        verbose_name_plural = 'students'

    def __str__(self):
        '''Unicode representation of StudentModel.'''
        return self.student_name
