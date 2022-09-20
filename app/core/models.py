import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin  

class UserManager(BaseUserManager):
    """Modifing createuser"""
    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError('User must have email address!')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Super user can't be created without email!")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using email instead of username"""
    email=models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD =   'email'
