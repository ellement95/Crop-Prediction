from django.db import models

# Create your models here.
class ToDoList(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text

class File(models.Model):
    file = models.FileField(upload_to='files/')
    # Add any additional fields you need for the File model

class CropData(models.Model):
    crop_name = models.CharField(max_length=100)
    yield_value = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    date = models.DateField()