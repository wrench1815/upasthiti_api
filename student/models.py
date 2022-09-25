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

        - holds the university roll no
        - holds the related university
        - holds the related student

        #! The roll nos must be unique for each university and are tested by API endpoints only
    '''

    university_roll_no = models.CharField(
        max_length=15,
        default=random_rollno,
    )
    university = models.ForeignKey(
        UniversityModel,
        related_name='university',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        'StudentModel',
        related_name='student_university_roll',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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

        - holds the college roll no
        - holds the related college
        - holds the related student

        #! Note: The roll nos must be unique for each college and are tested by API endpoints only
    '''

    class_roll_no = models.CharField(
        max_length=15,
        default=random_rollno,
    )
    college = models.ForeignKey(
        CollegeModel,
        related_name='college',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        'StudentModel',
        related_name='student_college_roll',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
    '''
        Model definition for StudentModel.

        - holds the data for Student
        - must have a unique email
        - data for multiple volleges and universities is shared if same email
        
        #! Note: update the university and college data if user already exist donot create a new student using the API endpoint only
    '''
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField(unique=True)
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
