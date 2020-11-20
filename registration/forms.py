from django import forms
from django.contrib.auth.models import User

from .models import Profile

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'type': 'text', 'name': 'First name', 'placeholder': 'Имя'}),
        label='Имя')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'my-input'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'my-input'}), required=False)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'my-input'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'my-input'}), required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'avatar')

    