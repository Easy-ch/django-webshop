# Generated by Django 4.2.3 on 2023-10-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_online_shop', '0004_onlineshop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineshop',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='onlineshop',
            name='image',
            field=models.ImageField(blank=True, upload_to='online_shop/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='onlineshop',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлен'),
        ),
    ]
