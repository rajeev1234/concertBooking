from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import render
# Create your models here.

class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Seat(models.Model):
    seat_choice = (
        ('', 'Select'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no_of_seat = models.CharField(max_length=3,null=True,blank=False)
    seat_type = models.CharField(max_length=8, choices=seat_choice, blank=False)
    each_price = models.CharField(max_length=100,null=True,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Total ' + self.no_of_seat + " seats of INR " + str(self.each_price) + " each"

class Concert(models.Model):
    title = models.CharField(max_length=20,null=True,blank=True)
    concert = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ManyToManyField(Seat)
    description = models.CharField(max_length=200,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    run_length = models.IntegerField(help_text="Enter run length in minutes",null=True,blank=True)
    trailer = models.URLField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='media')
    concert_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Booking(models.Model):
    payment_choice = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card')
    )
    seat_choice = (
        ('', 'Select'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )
    no_of_seat= models.IntegerField(default=0)
    seat_type = models.CharField(max_length=8, choices=seat_choice, blank=False)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=11, choices=payment_choice,default='Credit Card')
    amount = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    paid_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

