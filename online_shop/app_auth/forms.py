# import libraries:
from typing import Any
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm
from captcha.fields import CaptchaField

# main code: 
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "type":'username','class': 'form-control form-control-lg', 'placeholder': 'Введите ваш email '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type":'password','class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'}))
    captcha = CaptchaField(required=True)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'} ))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'} ))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
    captcha = CaptchaField(required=True)
    class Meta:
       model = User
       fields  = ['email','username','first_name','last_name','password1','password2','captcha']
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже зарегистрирован.")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя уже занято.")
        return username
    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')
        if name == surname:
            raise forms.ValidationError("Имя и фамилия не могут быть одинаковыми.")
        return surname
    # def clean_captcha(self):
    #     cd = self.cleaned_data.get('captcha')
    #     if cd != :
    #         raise forms.ValidationError("Капча неверна")
    #     return cd
        
class ProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg','readonly':True}, ))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4','readonly':True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    class Meta:
     model = User
     fields = ['email','username','first_name','last_name','image']  
# Add custom username validation if needed
     def clean_email(self):
          return self.cleaned_data['email']
     def clean_username(self):
          return self.cleaned_data['username']
     def clean_name(self):
          return self.cleaned_data['name']
     def clean_surname(self):
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
