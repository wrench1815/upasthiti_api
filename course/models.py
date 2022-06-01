from django.db import models


# Create your models here.
class CourseModel(models.Model):
    """Model definition for course."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for course."""

        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        """Unicode representation of course."""
        pass
