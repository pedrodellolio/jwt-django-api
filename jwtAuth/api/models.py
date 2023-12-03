from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

'''
This is only to show how to create a custom User. 
This model inherits from AbstractBaseUser, which only includes password, last_login, and is_active.
If you want to keep the default attributes, this User model should be deleted, and you should use the User from django.contrib.auth.models.
'''

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, username, first_name, last_name, email, password, **extra_fields):
        if not username or not first_name or not last_name or not email or not password:
            raise ValueError(
                'The username, first_name, last_name, email and password must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create(username, first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create(username, first_name, last_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

