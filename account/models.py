from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .validators import validate_admission_number, validate_contact_number


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    username = models.SlugField(max_length=16, unique=True)
    admission_no = models.CharField(max_length=16, unique=True, validators=[validate_admission_number])
    full_name = models.CharField(max_length=32)
    contact_no = models.CharField(max_length=10, validators=[validate_contact_number])
    avatar = models.SmallIntegerField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "admission_no", "full_name", "contact_no", "avatar"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.admission_no = self.admission_no.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
