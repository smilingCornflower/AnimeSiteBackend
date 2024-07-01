from django.core.files.base import ContentFile
from django.db import models
from .other_models import Genre, Voice, Timing, Subtitles
from django.core.validators import FileExtensionValidator

from PIL import Image
from io import BytesIO

SEASON_CHOICES = [
    ('summer', 'лето'),
    ('autumn', 'осень'),
    ('spring', 'весна'),
    ('winter', 'зима'),
]

STATUS_CHOICES = [
    ('ongoing', 'онгоинг'),
    ('completed', 'завершен'),
    ('announcement', 'анонс'),
]

WEEKDAY_CHOICES = [
    ('mon', 'Понедельник'),
    ('tue', 'Вторник'),
    ('wed', 'Среда'),
    ('thu', 'Четверг'),
    ('fri', 'Пятница'),
    ('sat', 'Суббота'),
    ('sun', 'Воскресенье'),
]


class Anime(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название [русское]')
    title_latin = models.CharField(max_length=200, unique=True, verbose_name='Название [латинское]')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    season = models.CharField(max_length=6, choices=SEASON_CHOICES, verbose_name='Сезон')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, verbose_name='Статус озвучки')

    favorites_count = models.PositiveIntegerField(default=0, verbose_name='Количество в любимых')
    new_episode_every = models.CharField(
            max_length=11, blank=True, null=True, 
            choices=WEEKDAY_CHOICES, verbose_name='Новый эпизод еженедельно')
    episodes_number = models.PositiveSmallIntegerField(default=0, verbose_name='Количество серии')
    image = models.ImageField(upload_to='anime_covers',
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])],
                                    verbose_name='Постер')

    genres = models.ManyToManyField(to=Genre, related_name='anime_list', verbose_name='Жанры')
    voices = models.ManyToManyField(to=Voice, related_name='anime_list', verbose_name='Голоса')
    timing = models.ManyToManyField(to=Timing, related_name='anime_list', verbose_name='Тайминг')
    subtitles = models.ManyToManyField(to=Subtitles, related_name='anime_list', verbose_name='Субтитры')
    
    # excluded in admin panel
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anime'
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
        ordering = ['title']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            img_compressed = BytesIO()
            img.save(img_compressed, format='jpeg', quality=80)
            img_compressed.seek(0)

            self.image = ContentFile(img_compressed.read(), self.image.name)

        super().save(*args, **kwargs)