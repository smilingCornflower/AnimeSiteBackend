from rest_framework.views import APIView
from rest_framework.response import Response
from .models import YouTubeVideo
from anime.models.anime_model import Anime

from my_toos.image_data import get_image_data_youtube, get_image_data_anime


class YouTubeVideoView(APIView):
    @staticmethod
    def get(request):
        videos = YouTubeVideo.objects.all()
        output = [
            {
                'id': item.id,
                'title': item.title,
                'url': item.url,
                'image_data': get_image_data_youtube(YouTubeVideo, img_id=item.id),
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
                'image_data': get_image_data_anime(Anime, img_id=anime.id),
            } for anime in last_five_updated_anime
        ]
        return Response(output)
