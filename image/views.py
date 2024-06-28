from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from main.models import YouTubeVideo
from anime.models.anime_model import Anime
from app.settings import BASE_DIR


def send_image_youtube(request, image_id):
    image_path = get_object_or_404(YouTubeVideo, id=image_id).image.url
    image_path = str(BASE_DIR) + image_path
        
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    return HttpResponse(image_data, content_type='image/jpeg')


def send_image_anime(request, image_id):
    image_path = get_object_or_404(Anime, id=image_id).cover_image.url
    image_path = str(BASE_DIR) + image_path

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    return HttpResponse(image_data, content_type='image/jpeg')