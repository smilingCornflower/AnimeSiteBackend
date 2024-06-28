from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Жанр')
    
    class Meta:
        db_table = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Voice(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Голос')
    
    class Meta:
        db_table = 'voice'
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Timing(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тайминг')
    
    class Meta:
        db_table = 'timing'
        verbose_name = 'Тайминг'
        verbose_name_plural = 'Тайминги'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Subtitles(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Субтитры')
    
    class Meta:
        db_table = 'subtitles'
        verbose_name = 'Субтитры'
        verbose_name_plural = 'Субтитры' 
        ordering = ['name']
    
    def __str__(self):
        return self.name