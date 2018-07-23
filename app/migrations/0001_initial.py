# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenPlanta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('foto', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('log_json', models.TextField()),
                ('texto_json', models.TextField()),
                ('id_chat', models.IntegerField()),
                ('pregunta', models.CharField(max_length=500)),
                ('slots', models.CharField(max_length=20)),
                ('intent', models.FloatField()),
                ('entity', models.CharField(max_length=20)),
            ],
        ),
    ]
