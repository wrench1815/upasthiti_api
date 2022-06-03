from django.db import models


class StudentModel(models.Model):
    """Model definition for StudentModel."""

    

    class Meta:
        """Meta definition for StudentModel."""

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        """Unicode representation of StudentModel."""
        pass
