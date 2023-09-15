from django.contrib import admin

# Register your models here.
from .models import Booking, Concert, User, Seat

class BookingAdmin(admin.ModelAdmin):
	class Meta:
		model = Booking

admin.site.register(Booking,BookingAdmin)

class ConcertAdmin(admin.ModelAdmin):
	class Meta:
		model = Concert

admin.site.register(Concert,ConcertAdmin)
admin.site.register(User)
admin.site.register(Seat)