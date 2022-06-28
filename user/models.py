from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather not Say', 'Rather not Say'),
)


class User(AbstractBaseUser, PermissionsMixin):
    '''Base User Model'''
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    profile_image = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    date_added = models.DateTimeField(_('date added'), default=timezone.now)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Dont delete Account, uncheck this.'))

    is_admin = models.BooleanField(_('admin'),
                                   default=False,
                                   help_text='Is the Person Admin or not.')

    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=_(
            'Designates whether user can log into the API Admin Site.'))

    is_principal = models.BooleanField(
        _('principal'),
        default=False,
        help_text=_('Is the Person Principal or not.'))

    is_hod = models.BooleanField(_('hod'),
                                 default=False,
                                 help_text=_('Is the Person HOD or not.'))

    is_teacher = models.BooleanField(
        _('teacher'),
        default=False,
        help_text=_('Is the Person Teacher or not'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self):
        '''
            return full name of the User
            format: '<first_name> <last_name>'
        '''
        return str(f'{self.first_name} {self.last_name}')

    def get_short_name(self):
        '''
            return short name of the User
            format '<first_name>'
        '''
        return str(self.first_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
            Sends an email to the User
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
