# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wandsproducts', '0006_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='abcd'),
        ),
    ]
