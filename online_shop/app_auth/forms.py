from django import forms
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '',
            'id': 'password',
        }
))
    class Meta:
      model = User
      fields  = ['username','password1']
    
class RegisterForm(UserCreationForm):
   def __init__(self, *args: Any, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['username'].widget.attrs.update({
         'requared':'',
         'name':'username',
         'id':'username',
         'type':'text',
         'class':'form-control form-control-lg',
         'placeholder':'',
          'maxlength':'65',
          'maxlength':'65' 
      })
      self.fields['password1'].widget.attrs.update({
         'requared':'',
         'name':'username',
         'id':'username',
         'type':'password',
         'class':'form-control form-control-lg',
         'placeholder':'',
          'maxlength':'65',
          'maxlength':'65' 
      })
      self.fields['password2'].widget.attrs.update({
         'requared':'',
         'name':'username',
         'id':'username',
         'type':'password',
         'class':'form-control form-control-lg',
         'placeholder':'',
          'maxlength':'65',
          'maxlength':'65' 
      })
   class Meta:
      model = User
      fields  = ['username','password1','password2']
