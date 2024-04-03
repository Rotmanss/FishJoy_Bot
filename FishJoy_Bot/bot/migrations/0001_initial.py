# Generated by Django 5.0.3 on 2024-03-30 10:48

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('email', models.EmailField(db_index=True, max_length=50)),
                ('subject', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedback',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FishCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Fish category')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Fish category',
                'verbose_name_plural': 'Fish categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpotCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Spot category')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Spot category',
                'verbose_name_plural': 'Spot categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Baits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Bait name')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('photo', models.ImageField(upload_to='photos/baits/%Y/%m/%d/')),
                ('price', models.FloatField(validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)])),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bait',
                'verbose_name_plural': 'Baits',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Fish name')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('photo', models.ImageField(upload_to='photos/fish/%Y/%m/%d/')),
                ('average_weight', models.FloatField(validators=[django.core.validators.MaxValueValidator(200.0), django.core.validators.MinValueValidator(0.1)], verbose_name='Average weight')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('baits', models.ManyToManyField(to='bot.baits')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fish_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.fishcategory')),
            ],
            options={
                'verbose_name': 'Fish',
                'verbose_name_plural': 'Fish',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Spots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Spot name')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('location', models.CharField(max_length=50)),
                ('photo', models.ImageField(upload_to='photos/spot/%Y/%m/%d/')),
                ('max_depth', models.FloatField(validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(1)], verbose_name='Max depth')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('dislikes', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('disliked_by', models.ManyToManyField(blank=True, related_name='disliked_spots', to=settings.AUTH_USER_MODEL)),
                ('fish', models.ManyToManyField(to='bot.fish')),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_spots', to=settings.AUTH_USER_MODEL)),
                ('spot_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.spotcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Spot',
                'verbose_name_plural': 'Spots',
                'ordering': ['title'],
            },
        ),
    ]