from django.db import models

# Create your models here.
class Address(models.Model):
  address = models.CharField(max_length=255)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  state_code = models.CharField(max_length=10)
  postal_code = models.CharField(max_length=20)
  country = models.CharField(max_length=100)
  lat = models.FloatField(blank=True, null=True)
  lng = models.FloatField(blank=True, null=True)
  def __str__(self):
    return f"{self.city}, {self.country}"
  
class Company(models.Model):
  name = models.CharField(max_length=255)
  department = models.CharField(max_length=255)
  title = models.CharField(max_length=100)
  address= models.OneToOneField(Address,on_delete=models.CASCADE,related_name='company_address')

class ExternalUser(models.Model):
  external_id = models.CharField(unique=True)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  maiden_name = models.CharField(max_length=100, blank=True, null=True)
  age = models.IntegerField(blank=True, null=True)
  gender = models.CharField(max_length=20)
  email = models.EmailField(blank=True, null=True)
  phone = models.CharField(max_length=50)
  username = models.CharField(max_length=100)
  password = models.CharField(max_length=255) 
  birth_date = models.DateField(blank=True, null=True)
  image_url = models.URLField()
  blood_group = models.CharField(max_length=5)
  height = models.FloatField(blank=True, null=True)
  weight = models.FloatField(blank=True, null=True)
  eye_color = models.CharField(max_length=20)
  hair_color = models.CharField(max_length=50)
  hair_type = models.CharField(max_length=50)

  address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='user_address')
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

  card_number = models.CharField(max_length=30)
  crypto_wallet = models.CharField(max_length=255)
  role = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
