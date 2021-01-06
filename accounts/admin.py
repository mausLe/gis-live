from django.contrib import admin

# Register your models here.

from .models import User, TrackingData, TrackingDevice

admin.site.register(User)
admin.site.register(TrackingData)
admin.site.register(TrackingDevice)

