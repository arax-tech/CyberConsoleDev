import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Company', 'Company'),
    ('Client', 'Client'),
    ('Team', 'Team'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


def upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)


class User(AbstractBaseUser):

    id = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    company = models.CharField(max_length=255,)
    group = models.CharField(max_length=255,)
    team = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255,)
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True,)
    address_first_line = models.CharField(max_length=255, null=True)
    address_second_line = models.CharField(max_length=255, null=True)
    address_town_city = models.CharField(max_length=255, null=True)
    address_country_code = models.CharField(max_length=255, null=True)
    address_country = models.CharField(max_length=255, null=True)
    permissions = ArrayField(models.CharField(max_length=50000, blank=True, default=''), null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(
        max_length=255, choices=ROLE_CHOICES, default="Company")
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='profile/placeholder.jpg')

    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return self.name

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
