from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Flight(models.Model):
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    travel_class = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='flights/', blank=True, null=True)

    def __str__(self):
        return f"{self.airline} - {self.flight_number}"
    

class Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    passenger_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    seat_number = models.CharField(max_length=10, null=True, blank=True)

    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.flight.flight_number}"
