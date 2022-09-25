from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from random import choice

from api.utils import DISTRICTS_CHOICES
from user.models import GENDER_CHOICES
from university.models import UniversityModel
from college.models import CollegeModel


def random_gender():
    '''
        Returns a  Random Gender out of Gender List
    '''
    gender = choice(GENDER_CHOICES)
    return gender[1]


def random_rollno():
    '''
        returns a random string of numbers
    '''
    return get_random_string(
        allowed_chars='0123456789',
        length=14,
    )


class UniversityRollNo(models.Model):
    '''
        Model definition for UniversityRollNo.
    '''

    university_roll_no = models.CharField(
        max_length=15,
        unique=True,
        default=random_rollno,
    )
    university = models.ForeignKey(
        UniversityModel,
        related_name='university',
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''
            Meta definition for UniversityRollNo.
        '''

        verbose_name = 'University Roll No'
        verbose_name_plural = 'University Roll Nos'

    def __str__(self):
        '''
            Unicode representation of UniversityRollNo.
        '''

        return f'{self.university_roll_no}'


class CollegeRollNo(models.Model):
    '''
        Model definition for CollegeRollNo.
    '''

    class_roll_no = models.CharField(max_length=15)
    college = models.ForeignKey(
        CollegeModel,
        related_name='college',
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''
            Meta definition for CollegeRollNo.
        '''

        verbose_name = 'College Roll No'
        verbose_name_plural = 'College Roll Nos'

    def __str__(self):
        '''
            Unicode representation of CollegeRollNo.
        '''

        return f'{self.class_roll_no}'


class StudentModel(models.Model):
    '''Model definition for StudentModel.'''
    first_name = models.TextField()
    last_name = models.TextField()
    # class_rollno = models.CharField(
    #     max_length=50,
    #     default=random_rollno,
    # )
    # university_rollno = models.CharField(
    #     unique=True,
    #     max_length=50,
    #     default=random_rollno,
    # )
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    district = models.CharField(
        choices=DISTRICTS_CHOICES,
        max_length=11,
        default='Jammu',
    )
    profile_image = models.URLField()
    profile_image_public_id = models.TextField(
        blank=True,
        null=True,
    )
    gender = models.CharField(max_length=15,
                              choices=GENDER_CHOICES,
                              default=random_gender)
    college = models.ManyToManyField(
        CollegeRollNo,
        related_name='student_college',
    )
    university = models.ManyToManyField(
        UniversityRollNo,
        related_name='student_university',
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        '''Meta definition for StudentModel.'''

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self):
        '''
            return full name of the student
            format: '<student_first_name> <student_last_name>'
        '''
        return str(f'{self.first_name} {self.last_name}')
