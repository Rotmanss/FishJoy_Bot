from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class Spots(models.Model):
    title = models.CharField(max_length=50, verbose_name='Spot name')
    location = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="photos/spot/%Y/%m/%d/")
    max_depth = models.FloatField(validators=[MaxValueValidator(10000), MinValueValidator(1)], verbose_name='Max depth')
    spot_category = models.ForeignKey('SpotCategory', on_delete=models.PROTECT)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name = 'Spot'
        verbose_name_plural = 'Spots'
        ordering = ['title']


class Fish(models.Model):
    name = models.CharField(max_length=50, verbose_name='Fish name')
    photo = models.ImageField(upload_to="photos/fish/%Y/%m/%d/")
    average_weight = models.FloatField(validators=[MaxValueValidator(200.0), MinValueValidator(0.1)], verbose_name='Average weight')
    fish_category = models.ForeignKey('FishCategory', on_delete=models.PROTECT)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name = 'Fish'
        verbose_name_plural = 'Fish'
        ordering = ['name']


class Baits(models.Model):
    name = models.CharField(max_length=50, verbose_name='Bait name')
    photo = models.ImageField(upload_to="photos/baits/%Y/%m/%d/")
    price = models.FloatField(validators=[MaxValueValidator(100000), MinValueValidator(0)])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name = 'Bait'
        verbose_name_plural = 'Baits'
        ordering = ['name']


class SpotCategory(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Spot category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Spot category'
        verbose_name_plural = 'Spot categories'
        ordering = ['name']


class FishCategory(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Fish category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fish category'
        verbose_name_plural = 'Fish categories'
        ordering = ['name']


class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'


class Evaluation(models.Model):
    record = models.ForeignKey(Spots, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    @staticmethod
    def update_average_rating_for_record_id(record_id):
        evaluations = Evaluation.objects.filter(record__id=record_id)
        average_rating = evaluations.aggregate(Avg('rating'))['rating__avg'] or 0.0
        record = Spots.objects.get(pk=record_id)
        record.average_rating = average_rating
        record.save()
