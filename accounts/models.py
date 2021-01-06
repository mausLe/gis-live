from django.db import models

# Create your models here.
class User(models.Model):
    userID = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__ (self):
        return self.userName

class TrackingDevice (models.Model):
    # Provide some devices id to refer
    deviceID = models.IntegerField(primary_key=True)
    deviceName = models.CharField(max_length=30, null=True)
    mfd = models.DateTimeField(auto_now_add=True, null=True)
    warranty = models.DateTimeField(auto_now_add=True, null=True)

    userid = models.ForeignKey(User, null=True,  on_delete=models.SET_NULL)


class TrackingData (models.Model):
    dataID = models.IntegerField(primary_key=True)
    longitude = models.FloatField(null=True)
    lattitude = models.FloatField(null=True)
    timeRecorded = models.DateTimeField(auto_now_add=True, null=True)
    
    deviceid = models.ForeignKey(TrackingDevice, null=True, on_delete=models.SET_NULL)
    

