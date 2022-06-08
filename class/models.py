from django.db import models


class ClassModel(models.Model):
    """Model definition for ClassModel."""
    #todo Pavitr rista (relations)
    name = models.TextField()
    session = models.CharField()
    college = models.IntegerField()
    department = models.IntegerField()
    teacher = models.IntegerField()
    course = models.IntegerField()
    student = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ClassModel."""

        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        """Unicode representation of ClassModel."""
        pass
