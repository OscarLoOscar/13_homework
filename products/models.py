from django.db import models

# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=50,unique=True)
  def __str__(self):
    return self.name

  
class ExternalProduct(models.Model):
    external_id = models.IntegerField(unique=True) 
    title = models.CharField(max_length=255)
    description = models.TextField() 
    category = models.CharField(max_length=100)
    price = models.FloatField()
    discount_percentage = models.FloatField() 
    rating = models.FloatField()
    stock = models.IntegerField()
    brand = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    weight = models.FloatField()
    dimensions_width = models.FloatField()
    dimensions_height = models.FloatField()
    dimensions_depth = models.FloatField()
    warranty_information = models.CharField(max_length=255)
    shipping_information = models.CharField(max_length=255)
    availability_status = models.CharField(max_length=50)
    return_policy = models.CharField(max_length=255)
    thumbnail = models.URLField()
    tags = models.ManyToManyField(Tag, related_name='products')

    def __str__(self):
        return self.title
    
class Review(models.Model):
  product = models.ForeignKey(ExternalProduct, on_delete=models.CASCADE, related_name='reviews') 
  rating = models.IntegerField()
  comment = models.TextField()
  date = models.DateTimeField()  
  reviewer_name = models.CharField(max_length=100)
  reviewer_email = models.EmailField()

  def __str__(self):
      return f"{self.reviewer_name} - {self.rating} Stars"
