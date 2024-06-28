from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from app.settings import BASE_DIR
from urllib.parse import unquote
import json
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.anime_model import Anime
from .models.other_models import Genre, Voice, Timing, Subtitles


class ReleaseView(APIView):
    @staticmethod
    def get(request):
        anime_by_popularity = Anime.objects.all().order_by('-favorites_count')
        output = [
            {
                'id': anime.id,
                'title': anime.title,
                'description': anime.description,
                'episodes_number': anime.episodes_number,
            } for anime in anime_by_popularity
        ]
        
        return Response(output)



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
                }
                for anime in Anime.objects.filter(new_episode_every=day)
            ] for day in weekdays
        }
        return Response(output)


class FilterView(APIView):
    @staticmethod
    def get(request):
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
                'genres': [i.name for i in anime.genres.all()],
                'voices': [i.name for i in anime.voices.all()],
                'timings': [i.name for i in anime.timing.all()],
                'subtitles': [i.name for i in anime.subtitles.all()],
            } for anime in Anime.objects.all()
        ]
        
        req_data = unquote(request.GET.get('data'))
        req_data = json.loads(req_data)

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
             } for anime in anime_list
        ]

        return Response(anime_list)

