from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


def validate_coordinates(value):
    try:
        lat, lon = map(float, value.split(','))
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return value
        else:
            raise forms.ValidationError(
                "Invalid coordinates. "
                "Latitude must be between -90° and 90°, and longitude must be between -180° and 180°.")
    except ValueError:
        raise forms.ValidationError("Invalid format. Please enter coordinates in the format 'latitude, longitude'.")


class SpotsForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    location = forms.CharField(max_length=50, required=False, validators=[validate_coordinates])
    max_depth = forms.FloatField(validators=[MaxValueValidator(10000), MinValueValidator(1)], required=False)
    spot_category = forms.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)], required=False)


class FishForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    average_weight = forms.FloatField(validators=[MaxValueValidator(200.0), MinValueValidator(0.1)], required=False)
    fish_category = forms.IntegerField(validators=[MaxValueValidator(2), MinValueValidator(1)], required=False)


class BaitsForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    price = forms.FloatField(validators=[MaxValueValidator(100000), MinValueValidator(0)], required=False)


class EvaluationForm(forms.Form):
    rating = forms.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
