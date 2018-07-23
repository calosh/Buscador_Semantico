# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    log_json = models.TextField()
    texto_json = models.TextField()
    id_chat = models.IntegerField()
    pregunta = models.CharField(max_length=500)
    slots = models.CharField(max_length=20)
    intent = models.FloatField()
    entity = models.CharField(max_length=20,)

    def __unicode__(self):
        return self.pregunta




class ImagenPlanta(models.Model):
    title = models.CharField(max_length=50)
    foto = models.FileField(upload_to="imagenes_plantas")

    def __unicode__(self):
        return self.title

