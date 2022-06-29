from django.contrib.auth.models import AbstractUser
from django.db import models

# Standard User Account, which indicates the type of user
class User(AbstractUser):
    is_active = models.BooleanField(default=True)

class Country(models.Model):
    name = models.CharField(max_length=255, blank=True)
    formatted_name = models.CharField(max_length=255, blank=True)

class RaceResult(models.Model):
    country = models.ForeignKey(to = 'Country', on_delete=models.CASCADE)
    race_datetime = models.IntegerField()
    position_1 = models.CharField(max_length=255, blank=True)
    position_2 = models.CharField(max_length=255, blank=True)
    position_3 = models.CharField(max_length=255, blank=True)
    position_4 = models.CharField(max_length=255, blank=True)
    position_5 = models.CharField(max_length=255, blank=True)
    position_6 = models.CharField(max_length=255, blank=True)
    position_7 = models.CharField(max_length=255, blank=True)
    position_8 = models.CharField(max_length=255, blank=True)
    position_9 = models.CharField(max_length=255, blank=True)
    position_10 = models.CharField(max_length=255, blank=True)

class BetResult(models.Model):
    user = models.ForeignKey(to = 'User', on_delete=models.CASCADE)
    race = models.ForeignKey(to = 'RaceResult', on_delete=models.CASCADE)
    country = models.ForeignKey(to = 'Country', on_delete=models.CASCADE)
    race_datetime = models.IntegerField()
    bet_amount = models.IntegerField()
    winnings = models.IntegerField()
    bet_type = models.CharField(max_length=255, blank=True)
    bet_value = models.CharField(max_length=255, blank=True)
    result_value = models.CharField(max_length=255, blank=True)