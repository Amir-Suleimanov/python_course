from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import CourseCardModel

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"required": True})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"required": True})
    )
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)


class CourseCardForm(forms.ModelForm):
    class Meta:
        model = CourseCardModel
        fields = ['title', 'description', 'price', 'photo',]
        widgets = {
            'title' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : "Курс",
            }),
            'description' : forms.Textarea( attrs={
                'class': 'form-control',
                'rows': 4,
                'cols': 40,
                'placeholder': "Текст описания"
            }),
            'photo' : forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'price' : forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder' : "0",
            }),
        }


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