from django.db import models


class TeacherModel(models.Model):
    """Model definition for TeacherModel."""

    teacher_name = models.TextField()
    teacher_department = models.IntegerField()

    class Meta:
        """Meta definition for TeacherModel."""

        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        """Unicode representation of TeacherModel."""
        return self.teacher_name
