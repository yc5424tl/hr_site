from django.core.validators import URLValidator, EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app.hr_django import settings


class Show(models.Model):
    date = models.DateField(null=False, blank=False, default=None)
    time = models.TimeField(null=False, blank=False, default=None)
    venue = models.ForeignKey("hr_live.Venue", on_delete=models.PROTECT, related_name="shows")
    date_created = models.DateTimeField(auto_add_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="shows_added")


class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default=None)
    address = models.CharField(max_length=200, blank=False, null=False, defualt=None)
    website = models.URLField(max_length=250, blank=True, null=True, default=None, validators=URLValidator())
    phone_number = PhoneNumberField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None, validators=EmailValidator())



class Booker(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False, default=None)
    last_name  = models.CharField(max_length=50, blank=False, null=False, default=None)
    nickname = models.CharField(max_length=100, blank=False, null=True, default=None)
    phone_number = PhoneNumberField(blank=False, null=False, default=None)
    email = models.EmailField(blank=False, null=False, default=None, validators=EmailValidator())
    venues = models.ManyToManyField(Venue)


    class Meta:
        ordering = ['first_name', 'last_name', 'phone_number', 'email', 'nickname']


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def add_venue(self, venue: Venue):
        if isinstance(venue, Venue) and venue not in self.venues:
            self.venues.add(venue)
            self.save()
            return True
        return False

    def remove_venue(self, venue: Venue):
        if venue in self.venues.all():
            self.venues.remove(venue)
            self.save()
            return True
        return False

    def upcoming_shows(self):
        pass


class Artist(models.Model):
    name = models.CharField(max_length=500, blank=False, null=False, default=None)
    website = models.URLField(max_length=500, blank=True, null=True, default=None, validators=URLValidator())