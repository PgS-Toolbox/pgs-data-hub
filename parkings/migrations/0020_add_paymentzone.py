# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-22 08:06
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0019_permits'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentZone',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='time created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='time modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)], verbose_name='zone number')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='geometry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
