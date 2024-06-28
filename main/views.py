from rest_framework.views import APIView
from rest_framework.response import Response
from .models import YouTubeVideo
from anime.models.anime_model import Anime


class YouTubeVideoView(APIView):
    @staticmethod
    def get(request,):
        videos = YouTubeVideo.objects.all()
        output = [
            {
                'id': item.id,
                'title': item.title,
                'url': item.url,
            } for item in videos
        ]
        return Response(output)


class SidePanelView(APIView):
    @staticmethod
    def get(request):
        last_five_updated_anime = [i for i in Anime.objects.order_by("updated_at")][-5:]
        output = [
            {
                'id': anime.id,
                'title': anime.title,
                'description': anime.description[:100],
                'episodes_number': anime.episodes_number,
            } for anime in last_five_updated_anime
        ]
        return Response(output)
