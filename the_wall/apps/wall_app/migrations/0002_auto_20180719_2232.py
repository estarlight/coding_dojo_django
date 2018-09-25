# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-19 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='messages',
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_comment', to='wall_app.Message'),
        ),
    ]