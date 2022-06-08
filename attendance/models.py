from django.db import models

class AttendanceModel(models.Model):
    """Model definition for AttendanceModel."""
    #todo add relation
    is_present=models.BooleanField()
    is_absent=models.BooleanField()
    is_last=models.BooleanField()
    date=models.DateTimeField()
    student=models.IntegerField()
    classes = models.IntegerField(auto_now_add=True)



    class Meta:
        """Meta definition for AttendanceModel."""

        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        """Unicode representation of AttendanceModel."""
        pass
