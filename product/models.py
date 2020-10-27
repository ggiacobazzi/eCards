from django.db import models

# Create your models here.
from shop.models import Shop


def upload(instance, file):
    path = 'prod_img/{id}/{file}'.format(id=instance.card_id, file=file)
    return path


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    card_id = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to=upload)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    shipment = models.DecimalField(decimal_places=2, max_digits=10, default=1)
    date = models.DateTimeField(verbose_name='date', auto_now_add=True)





