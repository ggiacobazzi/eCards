# Generated by Django 3.1.1 on 2020-10-13 21:58

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='photo',
            field=models.ImageField(blank=True, default='shop_img/default_shop_img.png', upload_to=shop.models.upload),
        ),
    ]
