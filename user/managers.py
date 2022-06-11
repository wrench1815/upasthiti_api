from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, email, password, **kwargs):
        '''
            Creates and saves a User with the given email and password
        '''
        if not email:
            raise ValueError('Email Address required')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)

        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_admin', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be a Staff')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Please check Superuser')

        return self._create_user(email, password, **kwargs)
