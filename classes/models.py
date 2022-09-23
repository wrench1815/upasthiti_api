from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from college.models import CollegeModel
from department.models import DepartmentModel
from course.models import CourseModel
from student.models import StudentModel

User = get_user_model()


class ClassModel(models.Model):
    '''Model definition for ClassModel.'''

    name = models.TextField()
    code = models.CharField(
        max_length=15,
        unique=True,
    )
    session_start = models.DateField(
        blank=True,
        null=True,
    )
    session_end = models.DateField(
        blank=True,
        null=True,
    )
    college = models.ForeignKey(
        CollegeModel,
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        DepartmentModel,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for ClassModel.'''

        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        '''Unicode representation of ClassModel.'''
        return self.class_name
