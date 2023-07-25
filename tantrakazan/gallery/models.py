from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from photologue import models as ph_models
from sortedm2m.fields import SortedManyToManyField
from unidecode import unidecode


class Gallery(ph_models.Gallery):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Массажист')



class Photo(ph_models.Photo):
    pass
