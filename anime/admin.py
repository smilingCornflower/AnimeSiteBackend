from django.contrib import admin
from .models.anime_model import Anime
from .models.other_models import Genre, Voice, Timing, Subtitles
from .models.episode_model import Episode

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'title_latin',)
    exclude = ('updated_at',)
    filter_horizontal = ('genres', 'voices', 'timing', 'subtitles')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Timing)
class TimingAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Subtitles)
class SubtitlesAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['anime']
    search_fields = ['anime__title__icontains']