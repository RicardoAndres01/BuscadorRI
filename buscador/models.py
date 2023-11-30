# en buscador/models.py

from django.db import models

class IndiceInvertido(models.Model):
    palabra = models.CharField(max_length=100)
    url = models.URLField()
    frecuencia = models.IntegerField()
