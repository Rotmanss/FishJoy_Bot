from django.contrib import admin
from .models import *


@admin.register(Spots)
class SpotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'spot_category', 'photo', 'location', 'max_depth', 'time_update')


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fish_category', 'photo', 'average_weight')


@admin.register(Baits)
class BaitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(SpotCategory)
class SpotCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(FishCategory)
class FishCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'subject')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'rating')
