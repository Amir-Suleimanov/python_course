from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"required": True})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"required": True})
    )
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)

class PasswordResetFrom(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"required": True})
    )

class CheckPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"required": True})
    )
    password2 = forms.CharField(
        label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"required": True})
    )



class RegistrationForm(UserCreationForm):    
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user