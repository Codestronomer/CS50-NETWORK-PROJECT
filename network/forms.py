from django import forms
from .models import Profile, User


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'bio', 'photo', 'location')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')