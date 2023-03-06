from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAddressModel(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=6)
    apartment = models.CharField(max_length=30, blank=True)

    class Meta:
        abstract = True
