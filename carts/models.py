from django.db import models
from users.models import ExternalUser

# Create your models here.
class Product(models.Model):
  external_product_id= models.IntegerField()
  title= models.CharField(max_length=255)
  price = models.FloatField()
  quantity = models.FloatField()
  total =models.FloatField()
  discount_percentage = models.FloatField()
  discounted_total = models.FloatField()
  thumbnail = models.URLField(max_length=500)
  def __str__(self):
    return self.title

class ExternalCart(models.Model):
  external_id = models.CharField(unique=True)
  products = models.ManyToManyField(Product,related_name='carts')
  total = models.FloatField()
  discounted_total = models.FloatField()
  # user_id = models.FloatField()
  user = models.OneToOneField(ExternalUser,on_delete=models.CASCADE,related_name='cart',null=True,blank=True)
  total_products = models.FloatField()
  total_quantity = models.FloatField()
  def __str__(self):
    return f"Cart {self.external_id} - User{self.user_id}"
