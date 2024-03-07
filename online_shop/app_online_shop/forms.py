from django import forms
from .models import OnlineShop 
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class Advertisementform(ModelForm):

    class Meta:
        model = OnlineShop
        fields = ['title','description','price','auction','image','user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols':80,'rows':10}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'auction': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
    }
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(Advertisementform, self).__init__(*args, **kwargs)
         # Сохраняем user_id внутри экземпляра формы
        self.user_id = user_id
    def save(self, commit=True):
        instance = super(Advertisementform, self).save(commit=False)
        if self.user_id:
            instance.user_id = self.user_id
        if commit:
            instance.save()
        return instance
    
    def clean_title(self):
        title = self.title = self.cleaned_data['title']
        if '?' in title:
            raise ValidationError('Заголовок не может содержать знак "?" ')
        return title