from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput


User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs) -> None:
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['email'].required = True

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        
        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError(
                'Пользователь с таким адресом электронной почты уже зарегистрирован.'
            )
        return email

  