from ast import In
from django.db import models
from django.utils import timezone


class CollegeModel(models.Model):
    """
        Model Definistion for CollegeModel
    """

    INSTITUTE_TYPES = (
        ('University', 'University'),
        ('Autonomous College', 'Autonomous College'),
        ('Afflitiated UG College', 'Afflitiated UG College'),
        ('Affliated PG College', 'Affliated PG College'),
        ('Teacher Education College', 'Teacher Education College'),
    )
    INSTITUTE_FOR = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Co-Education', 'Co-Education'),
    )
    LOCATION_TYPE = (
        ('Rural', 'Rural'),
        ('Urban', 'Urban'),
        ('Semi-Urban', 'Semi-Urban'),
    )
    FINANCIAL_MODEL = (
        ('Govt. Funded', 'Govt. Funded'),
        ('Self Financed', 'Self Financed'),
        ('Public Private Partnership (PPP)',
         'Public Private Partnership (PPP)'),
    )
    institute_name = models.TextField()
    institute_address = models.TextField()
    institute_principal = models.IntegerField()
    institute_logo = models.URLField()
    institute_website = models.URLField()
    institute_type = models.CharField(max_length=26, choices=INSTITUTE_TYPES)
    affiliating_university = models.TextField()
    institute_alias_name = models.TextField()
    institute_mobile = models.CharField(max_length=15)
    institute_alternate_mobile = models.CharField(max_length=15, blank=True)
    institute_email = models.EmailField(
        ('email address'),
        blank=True,
    )
    institute_alternate_email = models.EmailField(
        ('email address'),
        blank=True,
    )
    institute_state = models.TextField()
    institute_city = models.TextField()
    institute_pincode = models.CharField(max_length=10)
    running_frm_own_campus = models.BooleanField(default=True)
    institute_for = models.CharField(max_length=14, choices=INSTITUTE_FOR)
    location_type = models.CharField(max_length=11, choices=LOCATION_TYPE)
    financial_model = models.CharField(max_length=33, choices=FINANCIAL_MODEL)
    campus_area = models.CharField(max_length=50)
    built_up_area = models.CharField(max_length=50)
    minority_institution = models.BooleanField(default=False)
    recognised_under_sec_2F = models.BooleanField(default=False)
    recognised_under_sec_12B = models.BooleanField(default=False)
    recognised_as_college_with_potential_for_excellence = models.BooleanField(
        default=False)
    institute_mission = models.TextField(blank=True)
    institute_vision = models.TextField(blank=True)
    quality_policy = models.TextField(blank=True)
    naac_accredited = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.institute_name

    class Meta:
        """
            Meta definition for CollegeModel.
        """

        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
