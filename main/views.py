from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import unquote
from .models import YouTubeVideo
from app.settings import BASE_DIR


class YouTubeVideoView(APIView):
    def get(self, request,):
        videos = YouTubeVideo.objects.all()
        output = [
            {
                'id': item.id,
                'title': item.title,
                'url': item.url,
            } for item in videos
        ]
        return Response(output)


def send_image(request, image_id):
    image_path = get_object_or_404(YouTubeVideo, id=image_id).image.url
    image_path = str(BASE_DIR) + image_path
        
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    return HttpResponse(image_data, content_type='image/jpeg')
    