from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from .models import CustomUser
from .models import Message
from .models import Permission


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class MessageForm(forms.ModelForm):
    topic = forms.CharField(required=True)
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                    "rows": 16,
                                                                    "cols": 70
                                                                    }))

    class Meta:
        model = Message
        fields = ('topic', 'text', 'contain', "user_to")


class PermissionForm(forms.ModelForm):

    user_key = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Permission
        fields = ('user', 'user_key')


