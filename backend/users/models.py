from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    User manager.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model.
    """
    email = models.EmailField(
        primary_key=True,
        max_length=254,
        verbose_name='E-mail',
        help_text="Enter the user's e-mail."
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='First name',
        help_text="Enter the user's first name."
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Last name',
        help_text="Enter the user's last name."
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text=(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        "superuser",
        default=False,
    )
    date_joined = models.DateTimeField(
        "date joined",
        default=timezone.now
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class AuthCode(models.Model):
    """
    Authorization code model.
    """
    code = models.CharField(
        max_length=6,
        verbose_name='Authorization code'
    )
    user = models.ForeignKey(
        User,
        related_name='auth_codes',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    datetime_end = models.DateTimeField(
        verbose_name='Time of action'
    )
    used = models.BooleanField(
        default=False,
        verbose_name='Used'
    )

    class Meta:
        ordering = ('-datetime_end',)
        verbose_name = 'Authorization code'
        verbose_name_plural = 'Activation codes'

    def __str__(self):
        return f'{self.code}/{self.used}'
