from django.db import models
from django.contrib.auth.models import User

class RoomCategory(models.Model):
    name = models.CharField(max_length=255)
    base_price = models.IntegerField(default=0)

class Room(models.Model):
    room_number =models.CharField(max_length=255)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, null=True)
    is_available = models.BooleanField(default=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room =models.CharField(max_length=255)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    customer_name = models.CharField(max_length=255)
    total_price = models.FloatField(default=0.0)

class SpecialRate(models.Model):
    room_category =models.CharField(max_length=255)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    room_multiplier = models.IntegerField(default=0)

