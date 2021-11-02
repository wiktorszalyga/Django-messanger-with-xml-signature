from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



from .models import CustomUser, Message, Permission, Key

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
    text = forms.CharField(required=False, widget=forms.Textarea(
                                                    attrs={
                                                        "rows": 16,
                                                        "cols": 70
                                                    }
                                                )
                                            )

    class Meta:
        model = Message
        fields = ('topic', 'text', 'contain', "user_to")


class PermissionForm(forms.ModelForm):

    user_key = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Permission
        fields = ('user', 'user_key')


