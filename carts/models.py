from django.db import models
from users.models import ExternalUser

# Create your models here.
class Product(models.Model):
  external_product_id= models.IntegerField(null=True, blank=True)
  title= models.CharField(max_length=255)
  price = models.FloatField(null=True, blank=True)
  quantity = models.FloatField(null=True, blank=True)
  total =models.FloatField(null=True, blank=True)
  discount_percentage = models.FloatField(null=True, blank=True)
  discounted_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
  thumbnail = models.URLField(max_length=500)
  def __str__(self):
    return self.title

class ExternalCart(models.Model):
  external_id = models.CharField(unique=True)
  products = models.ManyToManyField(Product,related_name='carts')
  total = models.FloatField(null=True, blank=True)
  discounted_total = models.FloatField(null=True, blank=True)
  # user_id = models.FloatField()
  user = models.OneToOneField(ExternalUser,on_delete=models.CASCADE,related_name='cart',null=True,blank=True)
  total_products = models.FloatField(null=True, blank=True)
  total_quantity = models.FloatField(null=True, blank=True)
  def __str__(self):
    return f"Cart {self.external_id} - User{self.user_id}"
