from django.db import models

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='files/')

class CropData(models.Model):
    date = models.DateField()
    commodity = models.CharField(max_length=100,default='Unknown')
    variety = models.CharField(max_length=100)
    classification = models.CharField(max_length=100, default='Crop')
    category = models.CharField(max_length=100, default='Default Category')
    high_price = models.FloatField()
    low_price = models.FloatField()
    yield_value = models.FloatField()
    time_variable = models.TimeField()
