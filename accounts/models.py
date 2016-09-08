from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, address=None):
        """
        Creates and saves a User with the given email, mobile and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = self.model(
                email=self.normalize_email(email),
                mobile=mobile,
            )
            if address is not None:
                user.address=address

            user.set_password(password)
            user.save(using=self._db)
            return user
        raise ValueError("This email already exists")

    def create_superuser(self, email, mobile, password):
        """
        Creates and saves a superuser with the given email, mobile and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.create_user(
            email,
            password=password,
            mobile=mobile,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField('email address', db_index=True)
    mobile = models.CharField('mobile', max_length=10)
    address = models.CharField('address',max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def update_last_login(self):
        self.last_login = timezone.now()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
