
from django.urls import path
from user.views import user_registration, sign_up

urlpatterns = [
    path("sign-up/", user_registration, name="sign-up"),
    path("sign-in/", sign_up, name="sign-in"),
]
