from django.db import models
from django.utils import timezone


class AttendanceModel(models.Model):
    """Model definition for AttendanceModel."""

    is_present = models.BooleanField()
    is_absent = models.BooleanField()
    is_late = models.BooleanField()
    date = models.DateTimeField()
    student = models.IntegerField(null=True)
    classes = models.IntegerField(null=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for AttendanceModel."""

        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        """Unicode representation of AttendanceModel."""
        pass
