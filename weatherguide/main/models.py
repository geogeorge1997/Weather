from django.db import models

# Create your models here.

# Me : Each class need to migrate to use in our Database
#      This will create a python file in appname/migartions/(ex:0001)....


class CurrentAttributes(models.Model):
    placename=models.CharField(max_length=30)
    time=models.CharField(max_length=30)
    summary=models.CharField(max_length=50)
    rainProb=models.CharField(max_length=5)
    temperature=models.CharField(max_length=5)
    appTemperature=models.CharField(max_length=5)
    uvindex=models.CharField(max_length=5)
    icon=models.CharField(max_length=30)

class Hour24Attributes(models.Model):
    placename = models.CharField(max_length=30)
    mainsummary = models.CharField(max_length=50)
    time=models.CharField(max_length=30)
    summary=models.CharField(max_length=50)
    rainProb=models.CharField(max_length=5)
    temperature=models.CharField(max_length=5)
    appTemperature=models.CharField(max_length=5)
    uvindex=models.CharField(max_length=5)
    icon = models.CharField(max_length=30)



class WeeklyAttributes(models.Model):
    placename = models.CharField(max_length=30)
    mainsummary=models.CharField(max_length=50)
    time=models.CharField(max_length=30)
    summary=models.CharField(max_length=50)
    rainProb=models.CharField(max_length=5)
    temperatureLow = models.CharField(max_length=10)
    appTemperatureHigh = models.CharField(max_length=10)
    temperatureHigh = models.CharField(max_length=10)
    appTemperatureLow = models.CharField(max_length=10)
    icon = models.CharField(max_length=30)

