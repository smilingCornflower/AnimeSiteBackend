from django.urls import path
from .views import send_image_youtube, send_image_anime


urlpatterns = [
    path('youtube/<int:image_id>/', send_image_youtube, name='youtube_image'),   
    path('anime/<int:image_id>/', send_image_anime, name='send_image_anime'),
]
