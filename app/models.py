# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from spacy.errors import models_warning


class Log(models.Model):
    #time = models.DateTimeField(auto_now_add=True)
    log_json = models.TextField()



