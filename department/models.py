from django.db import models


# Create your models her
class DepartmentModel(models.Model):
    '''Model definition for DepartmentModel.'''

    PROGRAMMES_OFFERED = (
        ('Under-Graduate', 'Under-Graduate'),
        ('Post-Graduate', 'Post-Graduate'),
        ('Intergrated-PG', 'Intergrated-PG'),
        ('M.Phil', 'M.Phil'),
        ('Ph.D', 'Ph.D'),
        ('Certificate', 'Certificate'),
        ('UG Diploma', 'UG Diploma'),
        ('PG Diploma', 'PG Diploma'),
    )

    TOTAL_SEM = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
    )

    department_name = models.TextField()
    department_code = models.CharField(max_length=50)
    programmes_offered = models.CharField(max_length=16,
                                          choices=PROGRAMMES_OFFERED)
    total_semesters = models.IntegerField(choices=TOTAL_SEM)
    student_intake = models.IntegerField()
    faculty_intake = models.IntegerField()
    no_of_professors = models.IntegerField()
    no_of_associated_professors = models.IntegerField()
    hod = models.IntegerField()

    class Meta:
        '''Meta definition for DepartmentModel.'''

        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self):
        '''Unicode representation of DepartmentModel.'''
        return self.department_name
