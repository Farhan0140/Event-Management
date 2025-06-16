"""
URL configuration for Event_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from app_admin.views import test, organizer_dashboard, create_event, details, update_event, delete_event, delete_participant, participants_details, edit_participants_details, category_details, edit_category_details, delete_category

urlpatterns = [
    path('', test),
    path('details/', details, name="details"),
    path('organizer_dashboard/', organizer_dashboard, name="organizer_dashboard"),
    path('create_event/', create_event, name="create_event"),
    path('update_event/<int:id>/', update_event, name="update_event"),
    path('delete_event/<int:id>/', delete_event, name="delete_event"),
    path('participants_details/', participants_details, name="participants_details"),
    path('category_details/', category_details, name="category_details"),
    path('edit_category/<int:id>', edit_category_details, name="edit_category"),
    path('delete_participant/<int:id>/', delete_participant, name="delete_participant"),
    path('delete_category/<int:id>/', delete_category, name="delete_category"),
    path('edit_participants_details/<int:id>/', edit_participants_details, name="edit_participants_details"),
] + debug_toolbar_urls()
