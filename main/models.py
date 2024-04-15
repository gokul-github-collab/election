from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)

    avatar = models.ImageField(blank=True, null=True, default='profile.jpg')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    # pass


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, default='logo_iet.png')
    description = models.TextField(blank=True ,null=True)


    def __str__(self):
        return self.name

class CurrentIssues(models.Model):
    name = models.CharField(max_length=200 ,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class PressReleases(models.Model):
    name = models.CharField(max_length=200 ,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TenderAndVacancies(models.Model):
    name = models.CharField(max_length=200 ,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name

class ElectionStories(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', "Female")
)
class Voters(models.Model):
    name = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    gender = models.CharField(max_length = 20,
        choices = GENDER_CHOICES,
        default = '1')
    pob = models.CharField(max_length=20)
    age = models.IntegerField( default=27)
    house_no = models.CharField(max_length=100)
    flat_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    aadhar = models.CharField(max_length=12, unique=True)
    vote = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, default='profile.jpg')

    def __str__(self):
        return self.vote
