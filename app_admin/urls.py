
from django.urls import path
from app_admin.views import organizer_dashboard, create_event, update_event, delete_event, category_details, edit_category_details, delete_category, search_event, create_category

urlpatterns = [
    path('organizer_dashboard/', organizer_dashboard, name="organizer_dashboard"),
    path('create_event/', create_event, name="create_event"),
    path('update_event/<int:id>/', update_event, name="update_event"),
    path('delete_event/<int:id>/', delete_event, name="delete_event"),
    path('create_category/', create_category, name="create_category"),
    path('category_details/', category_details, name="category_details"),
    path('edit_category/<int:id>', edit_category_details, name="edit_category"),
    path('delete_category/<int:id>/', delete_category, name="delete_category"),
    path('search_event/', search_event, name="search_event"),
    
    # delete_participant, participants_details, edit_participants_details, details,
    # path('details/', details, name="details"),
    # path('participants_details/', participants_details, name="participants_details"),
    # path('delete_participant/<int:id>/', delete_participant, name="delete_participant"),
    # path('edit_participants_details/<int:id>/', edit_participants_details, name="edit_participants_details"),
]
