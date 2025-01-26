from django import forms

from .models import CourseCardModel

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
