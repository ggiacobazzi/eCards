# Generated by Django 3.1.1 on 2020-10-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_auto_20201005_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(default=None, max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telephone',
            field=models.CharField(default=None, max_length=15, unique=True),
        ),
    ]
