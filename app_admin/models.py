from django.db import models
from django.contrib.auth.models import User


# class RSVP(models.Model):
#     event = models.ManyToManyField(
#         "Event",
#         related_name="event",
#     )
#     user = models.ManyToManyField(
#         User,
#         related_name="user",
#     )


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.category_name


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    event_image = models.ImageField(upload_to='event_images', default="event_images/default_event.jpg")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
    )
    participant = models.ManyToManyField(
        User,
        related_name="rsvp_events",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.event_name
    

