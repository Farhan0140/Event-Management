
from django.urls import path
from user.views import user_registration

urlpatterns = [
    path("registration/", user_registration, name="user_registration")
]
