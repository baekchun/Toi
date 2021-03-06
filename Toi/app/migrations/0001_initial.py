# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-24 01:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('taken_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bristol_type', models.TextField()),
                ('date', models.DateTimeField()),
                ('contains_blood', models.BooleanField()),
                ('contains_mucus', models.BooleanField()),
                ('color_distribution', models.TextField()),
                ('bar_chart', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='stool',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile'),
        ),
    ]
