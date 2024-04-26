from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import CroppedImage


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','mobile']



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CroppedImage
        fields = ('file',)