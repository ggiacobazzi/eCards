# Generated by Django 3.1.1 on 2020-10-13 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0010_auto_20201005_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_management.customuser')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True)),
                ('opening_date', models.DateTimeField(auto_now_add=True, verbose_name='Opening Date')),
            ],
        ),
    ]
