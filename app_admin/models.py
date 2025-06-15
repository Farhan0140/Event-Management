from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
    )
    

class Participant(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100) # For using unique=True I got Some Error, Thats why i remove it
    event = models.ManyToManyField(
        Event,
        related_name="participants"
    )