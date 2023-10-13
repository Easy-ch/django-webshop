from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.contrib import admin
from django.forms import ModelForm
# Create your models here.
User = get_user_model()
class OnlineShop(models.Model): 
    title = models.CharField('Заголовок', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10,decimal_places=2)
    auction = models.BooleanField('Торг',help_text='Отметьте, уместен ли торг')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='Создан')
    update_time = models.DateTimeField(auto_now=True,verbose_name='Обновлен')
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    image = models.ImageField('Изображение',upload_to='online_shop/',blank=True)
    
    @admin.display(description='фото')
    def get_html_image(self):
        if self.image:
            return format_html(
                '<img src="{url}" style="max-width: 80px; max-height: 80px;"', url=self.image.url
            )
        else:
                return format_html('<img src="/static/img/shop.png" style="max-width: 80px; max-height: 80px;"')

    
    def __str__(self):
        return f'{self.id} {self.title} {self.price}'
    class Meta:
        db_table = 'advertisements'

     



