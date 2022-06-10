from django.db import models
from django.utils import timezone


class ClassesModel(models.Model):
    """Model definition for ClassesModel."""

    class_name = models.TextField()
    session = models.CharField(max_length=4)
    college = models.IntegerField(null=True)
    department = models.IntegerField(null=True)
    course = models.IntegerField(null=True)
    teacher = models.IntegerField(null=True)
    student = models.IntegerField(null=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for ClassesModel."""

        verbose_name = 'Classes'
        verbose_name_plural = 'Classes'

    def __str__(self):
        """Unicode representation of ClassesModel."""
        return self.class_name
