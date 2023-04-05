import os.path

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from django.utils import timezone
from uuid import uuid4


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields.setdefault("birthdate", date.today())

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    birthdate = models.DateField()

    gender = models.BooleanField(default=True)  # true : man false:woman

    address = models.TextField()

    contact = models.CharField(max_length=15)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.set_password(self.password)
    #
    #     super().save(*args, **kwargs)

    @property
    def isAdminCollege(self) -> bool:
        try:
            return self.college is not None

        except College.DoesNotExist:
            return False

    @property
    def profile_picture(self):
        pf = self.profile_pictures.filter(isCurrent=True)
        if not pf.first():
            return None
        return pf.first().image_url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)


def upload_to(path):
    def wrapper(instance, filename: str):
        ext = filename.split(".")[-1]

        #         set the filename as a random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)

    return wrapper


def upload_pdp(instance, filename):
    return upload_to("pf")(instance, filename)


class ProfilePicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name="profile_pictures")

    image_url = models.ImageField(upload_to=upload_pdp)

    created_at = models.DateTimeField(default=timezone.now)

    isCurrent = models.BooleanField(default=True)


class College(models.Model):
    name = models.CharField(max_length=100)

    website = models.CharField(max_length=150)

    email = models.EmailField()

    address = models.TextField()

    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name="college")

    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CollegeUser(models.Model):
    user = models.ForeignKey(User, related_name="colleges", on_delete=models.CASCADE)
    college = models.ForeignKey(College, related_name="users", on_delete=models.CASCADE)
    isAlumni = models.BooleanField(default=False)
    isConfirmed = models.BooleanField(default=False)
    dateRequested = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s request to be %s to %s" % (
            self.user.first_name,
            "an Alumni" if self.isAlumni else "a Student",
            self.college.name
        )
