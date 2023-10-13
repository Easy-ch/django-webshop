from django import forms
from django import forms
from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control form-control-lg"
            }
        ),error_messages={
               'required': 'The username field is required.'
        })
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control form-control-lg"
            }
        ),error_messages={
               'required': 'The password field is required.'
        })
    class Meta:
       model = User
       fields  = ['username','password']
       
    
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
