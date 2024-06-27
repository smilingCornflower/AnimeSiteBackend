from django.urls import path
from .views import YouTubeVideoView, send_image


urlpatterns = [
    path('main_page/', YouTubeVideoView.as_view(), name='main_page'),
    path('image/youtube/<int:image_id>/', send_image, name='youtube_image'),
]