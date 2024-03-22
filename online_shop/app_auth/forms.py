# import libraries:
from typing import Any
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm,PasswordResetForm,SetPasswordForm
from django_recaptcha.fields import ReCaptchaField,ReCaptchaV2Checkbox
from django.conf import settings
# main code: 
# Создаем поля формы аутентификации:
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "type":'username','class': 'form-control form-control-lg', 'placeholder': 'Введите ваш email '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type":'password','class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'}))
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

# Создаем поля формы регистрации:
class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'} ))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'} ))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
       model = User
       fields  = ['email','username','first_name','last_name','password1','password2','recaptcha']
# Кастомная валидация кажого поля формы:
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
# Создаем поля формы профиля:
class ProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg','readonly':True}, ))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4','readonly':True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    class Meta:
     model = User
     fields = ['email','username','first_name','last_name','image']  
#Кастомная валидация полей формы
    def clean_username(self):
         return self.cleaned_data['username']
    def clean_image(self):
        image = self.cleaned_data.get('image',None)
        if image:
            if image.size>settings.MAX_IMAGE_UPLOAD_SIZE:
                raise forms.ValidationError('Размер изображения слишком большой (макс 4МБ)')
            return image
        else:
            raise forms.ValidationError('Не удалось загрузить изображение')
        
    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if 'image' in self.cleaned_data and self.cleaned_data['image']:
            user.image = self.cleaned_data['image']
            if commit:
                user.save()
            return user
# создаем поле для ввода почты при смене пароля:
class PasswordResetFormCustom(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg','placeholder': 'Введите логин '} ))
    class Meta:
        model = User
        fields = ['email']
# создаем поле для ввода нового пароля
class CustomChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg' }))

    class Meta:
        model = User
        fields = ['new_password1','new_password2']  

    def __init__(self,*args,**kwargs):
        email = kwargs.pop('email',None)
        super().__init__(None,*args, **kwargs)
        self.email = email
# Проверка нового пароля на схожесть со старым
    def clean_new_password1(self):
        new_password1 =self.cleaned_data.get("new_password1")
        email = self.email
        if email:
            user = User.objects.get(email=email)
            if user.check_password(new_password1):
                raise forms.ValidationError("Новый пароль похож на старый")
        return new_password1