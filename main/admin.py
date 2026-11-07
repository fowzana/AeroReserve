from django.contrib import admin

# Register your models here.

from .models import Flight,Booking

admin.site.register(Flight)
admin.site.register(Booking)
