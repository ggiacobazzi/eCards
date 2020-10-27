from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from card_ecommerce import settings
from django.utils.text import slugify


# Create your models here.
from user_management.models import CustomUser


def upload(instance, file):
    path = 'shop_img/{user}/{file}'.format(user=instance.user.username, file=file)
    return path


class Shop(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to=upload, blank=True, default='shop_img/default_shop_img.png')
    opening_date = models.DateTimeField(verbose_name='Opening Date', auto_now_add=True)
    # slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    # def slug(self):
    #     return slugify(self.name)
    #
    # def save(self, *args, **kwargs):
    #     self.slug = self.slug or slugify(self.name)
    #     super().save(*args, **kwargs)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    review = models.TextField(blank=True)
    account = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('account', 'shop',)
