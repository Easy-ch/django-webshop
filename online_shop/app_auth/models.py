from django.db import models
from django.contrib.auth.models import AbstractUser
import random
class User(AbstractUser):
    image = models.ImageField(upload_to='auth/', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False, null=False, blank=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email
class Captcha(models.Model):
    expected_value = models.CharField(max_length=50)
    def generate_expected_captcha():
        captcha_value =''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=4))
        return captcha_value