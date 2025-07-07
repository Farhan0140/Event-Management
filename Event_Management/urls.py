from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from user.views import participant_dashboard, events_list, rsvp, view_details, search_event, no_permission
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', participant_dashboard, name="home"),
    path('events_list/', events_list, name="events_list"),
    path('events_details/<int:event_id>/', view_details, name="events_details"),
    path('rsvp/<int:event_id>/', rsvp, name="rsvp"),
    path('search_event/', search_event, name="search_event"),
    path('no_permission/', no_permission, name="no_permission"),
    path("organizer/", include("app_admin.urls")),
    path("user/", include("user.urls")),
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
