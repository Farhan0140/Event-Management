from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User( AbstractUser ):
    profile_img = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default.jpg")
    phone = models.CharField(max_length=15, blank=True)
