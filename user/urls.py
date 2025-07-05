
from django.urls import path
from user.views import user_registration, sign_up, sign_out

urlpatterns = [
    path("sign-up/", user_registration, name="sign-up"),
    path("sign-in/", sign_up, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
]
