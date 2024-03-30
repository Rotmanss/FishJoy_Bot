from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from spots.models import *


class AddSpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spot_category'].empty_label = 'Category is not selected'

    class Meta:
        model = Spots
        fields = '__all__'
        exclude = ['likes', 'dislikes', 'user', 'liked_by', 'disliked_by']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'slug': forms.TextInput(attrs={'class': 'form-input'}),
                   'location': forms.TextInput(attrs={'class': 'form-input'}),
                   'max_depth': forms.TextInput(attrs={'class': 'form-input'})}

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        instance.save()
        return instance


class AddFishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fish_category'].empty_label = 'Category is not selected'

    class Meta:
        model = Fish
        fields = '__all__'
        exclude = ['user']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-input'}),
                   'slug': forms.TextInput(attrs={'class': 'form-input'})}

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        instance.save()
        return instance


class AddBaitForm(forms.ModelForm):
    class Meta:
        model = Baits
        fields = '__all__'
        exclude = ['user']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-input'}),
                   'slug': forms.TextInput(attrs={'class': 'form-input'})}

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        instance.save()
        return instance


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(max_length=50, label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {'name': forms.TextInput(attrs={'class': 'form-input'}),
                   'email': forms.TextInput(attrs={'class': 'form-input'})}


# FORMAT_CHOICES = (
#     ('xls', 'xls'),
#     ('csv', 'csv'),
#     ('json', 'json')
# )


# class FormatForm(forms.Form):
#     format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.TextInput(attrs={'class': 'form-input'}))
