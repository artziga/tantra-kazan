from datetime import datetime

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from taggit.managers import TaggableManager

from tantrakazan import settings


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name='автор',
                               related_query_name='articles')
    title = models.CharField(max_length=100, null=True, verbose_name='название')
    slug = AutoSlugField(verbose_name='слаг', db_index=True, unique=True, populate_from='title')
    text = RichTextField(verbose_name='Текст статьи')
    date_added = models.DateTimeField('дата создания',
                                      auto_now_add=True)
    last_update = models.DateTimeField('дата редактирования',
                                       auto_now=True)
    tags = TaggableManager()

    class Meta:
        unique_together = [('author', 'slug'), ('author', 'title')]
        ordering = ['-last_update', '-pk']
        get_latest_by = 'last_update'
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def get_absolute_url(self):
        return reverse('articles:article', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
