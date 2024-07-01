from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from app.settings import BASE_DIR
from django.http import FileResponse, StreamingHttpResponse, HttpResponse

from django.core.paginator import Paginator
from .models.anime_model import Anime

import os
import re

from my_toos.image_data import get_image_data
from urllib.parse import unquote
import json

from django.http import HttpResponse, Http404
from django.conf import settings
from wsgiref.util import FileWrapper
from mimetypes import guess_type


class ReleaseView(APIView):
    @staticmethod
    def get(request, page_number=1):
        anime_by_popularity = Anime.objects.all().order_by('-favorites_count')
        output = [
            {
                'id': anime.id,
                'title': anime.title,
                'description': anime.description,
                'episodes_number': anime.episodes_number,
                'image_data': get_image_data(Anime, anime.id),
            } for anime in anime_by_popularity
        ]

        paginator = Paginator(output, 12)
        output_page = list(paginator.page(page_number))

        return Response(output_page)


class ScheduleView(APIView):
    @staticmethod
    def get(request):
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        output = {
            day: [
                {
                    'id': anime.id,
                    'title': anime.title,
                    'description': anime.description[:80],
                    'episodes_number': anime.episodes_number,
                    'image_data': get_image_data(Anime, anime.id),
                }
                for anime in Anime.objects.filter(new_episode_every=day)
            ] for day in weekdays
        }
        return Response(output)


class FilterView(APIView):
    @staticmethod
    def get(request, page_number=1):
        # It's supposed that get request is of form
        # localhost: 8000 / release / filter?data = {
        #     "genres": [genre1, genre2, ...] or null,
        #     "year": int or null,
        #     "season": "winter" or "summer" or "autumn" or "spring" or null,
        #     "popular_or_new": "popular", "new", null,
        #     "is_completed": true or null,  Logic for false is not exist
        # }

        anime_list = [
            {
                'id': anime.id,
                'title': anime.title,
                'description': anime.description,
                'episodes_number': anime.episodes_number,
                'year': anime.year,
                'season': anime.season,
                'favorites_count': anime.favorites_count,
                'updated_at': anime.updated_at,
                'status': anime.status,
                'image_data': get_image_data(Anime, anime.id),
                'genres': [i.name for i in anime.genres.all()],
            } for anime in Anime.objects.all()
        ]

        req_data = request.GET.get('data')
        if req_data is not None:
            req_data = json.loads(unquote(req_data))
        else:
            req_data = {}

        if req_data.get('genres', None) is not None:
            result = []
            for anime in anime_list:
                if all([i in anime['genres'] for i in req_data['genres']]):
                    result.append(anime)
            anime_list = result

        if req_data.get('year', None) is not None:
            anime_list = [anime for anime in anime_list if anime['year'] == req_data['year']]
        if req_data.get('season', None) is not None:
            anime_list = [anime for anime in anime_list if anime['season'] == req_data['season']]

        if req_data.get('popular_or_new', None) == 'popular':
            anime_list.sort(key=lambda x: x['favorites_count'], reverse=True)
        elif req_data.get('popular_or_new', None) == 'new':
            anime_list.sort(key=lambda x: x['updated_at'], reverse=True)

        if req_data.get('is_completed', None):
            anime_list = [anime for anime in anime_list if anime['status'] == 'completed']

        anime_list = [
            {
                'id': anime['id'],
                'title': anime['title'],
                'description': anime['description'],
                'episodes_number': anime['episodes_number'],
                'image_data': anime['image_data']
            } for anime in anime_list
        ]

        paginator = Paginator(anime_list, 9)
        output_page = list(paginator.page(page_number))

        return Response(output_page)


class WatchView(APIView):
    @staticmethod
    def get(request, anime_id):
        # It's supposed that get request is of form
        # localhost:8000/release/watch?id=IntNumber
        # anime_id = int(request.GET.get('id'))
        anime = get_object_or_404(Anime, id=anime_id)
        anime_info = {
            'id': anime.id,
            'title': anime.title,
            'description': anime.description,
            'episodes_number': anime.episodes_number,
            'year': anime.year,
            'season': anime.season,
            'favorites_count': anime.favorites_count,
            'status': anime.status,
            'image_data': get_image_data(Anime, anime.id),
            'genres': [i.name for i in anime.genres.all()],
            'voices': [i.name for i in anime.voices.all()],
            'timings': [i.name for i in anime.timing.all()],
            'subtitles': [i.name for i in anime.subtitles.all()],
        }
        return Response(anime_info)


def watch_episode(request, anime_id: int, episode_number: str):
    episode_path = os.path.join(settings.MEDIA_ROOT, f"{anime_id}/{episode_number}.mp4")

    if not os.path.exists(episode_path):
        return Http404("File not found")

    size = os.path.getsize(episode_path)
    content_type, content_encoding = guess_type(episode_path)

    range_header = request.headers.get("Range", "").strip()
    range_match = re.match(r'bytes=([0-9]+)-([0-9]*)', range_header)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1

        if last_byte > size:
            last_byte = size - 1

        with open(episode_path, 'rb') as episode_file:
            episode_file.seek(first_byte)
            content_length = last_byte - first_byte + 1
            wrapper = FileWrapper(episode_file, blksize=16384)
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = str(content_length)
            response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
            response['Accept-Ranges'] = 'bytes'
    else:
        response = HttpResponse(open(episode_path, 'rb'), content_type=content_type)
        response['Content-Length'] = str(size)
        response['Accept-Ranges'] = 'bytes'

    return response


