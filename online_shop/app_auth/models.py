from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
class User(AbstractUser):
    image = ProcessedImageField(upload_to='auth/', processors=[ResizeToFill(200, 200)],format='JPEG',options={'quality': 60},default=None)
    is_verified_email = models.BooleanField(default=False, null=False, blank=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email
