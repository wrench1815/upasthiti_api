from django.db import models
from django.utils import timezone


class ClassModel(models.Model):
    """Model definition for ClassModel."""

    name = models.TextField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    college = models.IntegerField()
    department = models.IntegerField()
    teacher = models.IntegerField()
    course = models.IntegerField()
    student = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for ClassModel."""

        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        """Unicode representation of ClassModel."""
        pass
