from django.db import models
from django.utils import timezone

from student.models import StudentModel
from classes.models import ClassModel


class AttendanceModel(models.Model):
    '''Model definition for AttendanceModel.'''

    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=True)
    is_late = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.CASCADE,
        related_name='attendance_student',
    )
    for_class = models.ForeignKey(
        ClassModel,
        on_delete=models.CASCADE,
        related_name='attendance_class',
        blank=True,
        null=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for AttendanceModel.'''

        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        '''Unicode representation of AttendanceModel.'''
        return self.student.first_name
