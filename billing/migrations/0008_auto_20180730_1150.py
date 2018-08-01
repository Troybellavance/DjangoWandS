# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-30 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20180730_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='chargeorder',
            name='outcome_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='chargeorder',
            name='risk_level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='chargeorder',
            name='seller_message',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='chargeorder',
            name='stripe_id',
            field=models.CharField(max_length=100),
        ),
    ]
