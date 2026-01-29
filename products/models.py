from django.db import models

# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=50,unique=True)
  def __str__(self):
    return self.name

  
class ExternalProduct(models.Model):
    external_id = models.IntegerField(unique=True) 
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True) 
    category = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True) 
    rating = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    weight = models.FloatField(null=True, blank=True)
    dimensions_width = models.FloatField(null=True, blank=True)
    dimensions_height = models.FloatField(null=True, blank=True)
    dimensions_depth = models.FloatField(null=True, blank=True)
    warranty_information = models.CharField(max_length=255)
    shipping_information = models.CharField(max_length=255)
    availability_status = models.CharField(max_length=50)
    return_policy = models.CharField(max_length=255)
    thumbnail = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.title
    
class Review(models.Model):
  product = models.ForeignKey(ExternalProduct, on_delete=models.CASCADE, related_name='reviews') 
  rating = models.IntegerField(null=True, blank=True)
  comment = models.TextField(null=True, blank=True)
  date = models.DateTimeField(null=True, blank=True)  
  reviewer_name = models.CharField(max_length=100)
  reviewer_email = models.EmailField(null=True, blank=True)

  def __str__(self):
      return f"{self.reviewer_name} - {self.rating} Stars"
