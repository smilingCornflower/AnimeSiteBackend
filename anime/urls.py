from django.urls import path
from .views import ReleaseView, ScheduleView, FilterView, WatchView


urlpatterns = [
    path('', ReleaseView.as_view(), name='releases'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('watch/', WatchView.as_view(), name='watch'),
]