from django.db import models


class StudentModel(models.Model):
    '''Model definition for StudentModel.'''
    #Todo add relations
    student_first_name = models.TextField()
    student_last_name = models.TextField()
    class_rollno = models.IntegerField()
    email = models.EmailField()
    phone_no = models.IntegerField(max_length=15)
    profile_image = models.URLField()
    courses = models.IntegerField()
    department = models.IntegerField()
    classes = models.IntegerField()
    attendance = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''Meta definition for StudentModel.'''

        verbose_name = 'student'
        verbose_name_plural = 'students'

    def __str__(self):
        '''Unicode representation of StudentModel.'''
        return self.student_name
