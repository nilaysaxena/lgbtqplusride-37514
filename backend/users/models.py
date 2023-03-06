from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from general.enum_helper import UserType
from general.models import BaseModel, BaseAddressModel


class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    user_type = models.CharField(max_length=30, choices=UserType.choices(), default=UserType.RIDER.value)
    is_mission_statement_accepted = models.BooleanField(default=False)
    is_payment_terms_accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def is_rider(self):
        return self.user_type == UserType.RIDER.value

    @property
    def is_driver(self):
        return self.user_type == UserType.DRIVER.value

    @property
    def is_app_admin(self):
        return self.user_type == UserType.ADMIN.value


class UserProfile(BaseModel, BaseAddressModel):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone = PhoneNumberField()

    def save(self, *args, **kwargs):
        self.name = f'{self.first_name} {self.last_name}'.strip()
        super().save(*args)
