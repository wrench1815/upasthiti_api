from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from college.models import CollegeModel

User = get_user_model()


class DepartmentModel(models.Model):
    '''Model definition for DepartmentModel.'''

    name = models.ForeignKey(
        'DepartmentTypeModel',
        on_delete=models.CASCADE,
        related_name='department',
    )
    hod = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hod_department',
        null=True,
        blank=True,
    )
    teacher = models.IntegerField(null=True)
    course = models.IntegerField(null=True)
    college = models.ForeignKey(
        CollegeModel,
        on_delete=models.CASCADE,
        related_name='department',
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for DepartmentModel.'''

        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self):
        '''Unicode representation of DepartmentModel.'''
        return str(self.department_name.department_name)


class DepartmentTypeModel(models.Model):
    '''Model definition for DepartmentTypeModel.'''

    department_name = models.TextField(unique=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for DepartmentTypeModel.'''

        verbose_name = 'Department Type'
        verbose_name_plural = 'Department Types'

    def __str__(self):
        '''Unicode representation of DepartmentTypeModel.'''
        return str(self.department_name)
