from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Wall(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок поста')
    slug = AutoSlugField(populate_from='title', unique=True)
    text = models.TextField(max_length=500, verbose_name='Текст поста')
    private = models.BooleanField(verbose_name='Опубликовать анонимно')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, default=None, blank=True, null=True, verbose_name='Автор')
    likes = models.ManyToManyField(get_user_model(), default=None, blank=True, verbose_name='Лайкнувшие пользователи', related_name='likes')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("wallapp:post", kwargs={"post_slug": self.slug})
    
    