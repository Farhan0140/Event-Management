from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from app_admin.views import organizer_dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', organizer_dashboard, name="home"),
    path("organizer/", include("app_admin.urls")),
] + debug_toolbar_urls()
