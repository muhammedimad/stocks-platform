#__author__ = Mohammad Abdin
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    """ edit user's profile form"""
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name' )

class ProfileForm(forms.ModelForm):
    """ user's profile form"""
    class Meta:
        model = Profile
        fields = ('job', 'image')  # Note that we didn't mention user field here.
