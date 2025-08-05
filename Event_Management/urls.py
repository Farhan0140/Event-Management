from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from user.views import events_list, no_permission, dashboard, Search_Event, RSVP, View_Detail, Participant_Dashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', Participant_Dashboard.as_view(), name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('events_list/', events_list, name="events_list"),
    path('events_details/<int:event_id>/', View_Detail.as_view(), name="events_details"),
    path('rsvp/<int:event_id>/', RSVP.as_view(), name="rsvp"),
    path('search_event/', Search_Event.as_view(), name="search_event"),
    path('no_permission/', no_permission, name="no_permission"),
    path("organizer/", include("app_admin.urls")),
    path("user/", include("user.urls")),
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
