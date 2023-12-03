# import libraries:
from django import forms
from typing import Any
from .models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm

# main code: 
class LoginForm(AuthenticationForm):
   username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Введите имя пользователя '}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'}))
   class Meta:
       model = User
       fields = ('username', 'password')

class RegisterForm(UserCreationForm):
   username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'} ))
   first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
   last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
   password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
   password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
   class Meta:
      model = User
      fields  = ['username','first_name','last_name','password1','password2']

    # --- check duplicate
   def clean_password2(self):
       cd = self.cleaned_data
       if cd['password1'] != cd['password2']:
           raise forms.ValidationError('Пароли не совпадают')
       return cd['password2']
class ProfileForm(UserChangeForm):
   username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4','readonly':True}))
   first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
   last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
   image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
   class Meta:
      model = User
      fields = ['username','first_name','last_name','image']  
   def clean_username(self):
        # Add custom username validation if needed
        return self.cleaned_data['username']

   def clean_name(self):
        # Add custom name validation if needed
        return self.cleaned_data['name']

   def clean_surname(self):
        # Add custom surname validation if needed
        return self.cleaned_data['surname']

   def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if 'image' in self.cleaned_data and self.cleaned_data['image']:
            user.image = self.cleaned_data['image']
        if commit:
            user.save()
        return user
