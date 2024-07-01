from django.urls import path
from .views import ReleaseView, ScheduleView, FilterView, WatchView, watch_episode


urlpatterns = [
    path('', ReleaseView.as_view(), name='releases'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('watch/<int:anime_id>', WatchView.as_view(), name='watch'),
    path('watch/<str:anime_id>/<str:episode_number>', watch_episode, name='watch_episode'),
]