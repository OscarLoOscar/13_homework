import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from users.models import ExternalUser, Address, Company
from products.models import ExternalProduct,Tag,Review
from carts.models import ExternalCart,Product

class Command(BaseCommand):
  help = 'Fetch and clean User data from DummyJSON'

  def add_arguments(self, parser):
    return super().add_arguments('--action',type=str,help = 'create,update,delete',default = 'create')
  
  def handle(self,*args,**options):
    action = options['action']

    if action=='delete':
      self.clear_all_data()
    elif action =='update':
      self.update_existing_data()
    else:
      self.sync_all_data()

  def clear_all_data(self):
      self.stdout.write(self.style.WARNING('Deleting all data...'))
      ExternalUser.objects.all().delete()
      Address.objects.all().delete()
      Company.objects.all().delete()
      ExternalProduct.objects.all().delete()
      Tag.objects.all().delete()
      ExternalCart.objects.all().delete()
      Product.objects.all().delete()
      self.stdout.write(self.style.SUCCESS('All data cleared.'))

  def update_existing_data(self):
    self.stdout.write('Checking for price updates...')
    response = requests.get('https://dummyjson.com/products?limit=25')
    products = response.json().get('products',[])
    updated_count = 0

    for product in products:
      affected = ExternalProduct.objects.filter(external_id=product.get('id')).update(price =product.get('price'),rating =product.get('rating'))
      if affected:updated_count+=1
      self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} products' prices."))
  
  def sync_all_data(self):
    self.handleUser()
    self.handleProduct()
    self.handleCarts()


  def handleUser(self,*args,**kwargs):
    # ExternalUser.objects.all().delete()
    # Address.objects.all().delete()
    # Company.objects.all().delete()

    response = requests.get('https://dummyjson.com/users?limit=25')
    data = response.json()
    users = data.get('users',[])

    for u in users:
      if not u.get('email'): continue
      raw_date=u.get('birthDate')
      formatted_date = datetime.strptime(raw_date,'%Y-%m-%d').date()

      address_data = u.get('address',{})
      home_address = Address.objects.create(
        address=address_data.get('address'),
        city=address_data.get('city'),
        state=address_data.get('state'),
        state_code=address_data.get('stateCode'),
        postal_code=address_data.get('postalCode'),
        country=address_data.get('country'),
        lat=address_data.get('coordinates', {}).get('lat', 0),
        lng=address_data.get('coordinates', {}).get('lng', 0)
      )

      company_data = u.get('company',{})
      company_address_data = company_data.get('address',{})
      company_address = Address.objects.create(
        address=company_address_data.get('address', 'N/A'),
        city=company_address_data.get('city', 'N/A'),
        state=company_address_data.get('state', 'N/A'),
        state_code=company_address_data.get('stateCode', 'N/A'),
        postal_code=company_address_data.get('postalCode', 'N/A'),
        country=company_address_data.get('country', 'N/A'),
        lat=company_address_data.get('coordinates', {}).get('lat', 0),
        lng=company_address_data.get('coordinates', {}).get('lng', 0)
      )

      user_company = Company.objects.create(
        name=company_data.get('name'),
        department=company_data.get('department'),
        title=company_data.get('title'),
        address=company_address
      )

      ExternalUser.objects.update_or_create(
        username = u.get('username'),
        defaults={
          'external_id':u.get('id'),
          'first_name': u.get('firstName'),
          'last_name': u.get('lastName'),
          'maiden_name': u.get('maidenName'),
          'age': u.get('age'),
          'gender': u.get('gender'),
          'email': u.get('email'),
          'phone': u.get('phone'),
          'password': u.get('password'),
          'birth_date': formatted_date,
          'image_url': u.get('image'),
          'blood_group': u.get('bloodGroup'),
          'height': u.get('height'),
          'weight': u.get('weight'),
          'eye_color': u.get('eyeColor'),
          'hair_color': u.get('hair', {}).get('color'),
          'hair_type': u.get('hair', {}).get('type'),
          'address': home_address,
          'company': user_company,
          'card_number': u.get('bank', {}).get('cardNumber'),
          'crypto_wallet': u.get('crypto', {}).get('wallet'),
          'role': u.get('role'),
        }
      )

    self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(users)} users'))

  def handleProduct(self,*args,**kwargs):
    # ExternalProduct.objects.all().delete()
    response = requests.get('https://dummyjson.com/products?limit=25')
    data = response.json()
    products = data.get('products',[])

    self.stdout.write("Fetching Products data...")
    for product in products:
      product_obj,create = ExternalProduct.objects.update_or_create(
        external_id=product.get('id'),
        defaults={
            'title': product.get('title'),
            'description': product.get('description'),
            'category': product.get('category'),
            'price': product.get('price'),
            'discount_percentage': product.get('discountPercentage'),
            'rating': product.get('rating'),
            'stock': product.get('stock'),
            'brand': product.get('brand'),
            'sku': product.get('sku'),
            'weight': product.get('weight'),
            'dimensions_width': product.get('dimensions', {}).get('width'),
            'dimensions_height': product.get('dimensions', {}).get('height'),
            'dimensions_depth': product.get('dimensions', {}).get('depth'),
            'warranty_information': product.get('warrantyInformation'),
            'shipping_information': product.get('shippingInformation'),
            'availability_status': product.get('availabilityStatus'),
            'return_policy': product.get('returnPolicy'),
            'thumbnail': product.get('thumbnail'),
        }
      )

      for tag in product.get('tags',[]):
        tag,_ = Tag.objects.get_or_create(name=tag.lower())
        product_obj.tags.add(tag)
    
      for review in product.get('reviews',[]):
        Review.objects.get_or_create(
          product=product_obj,
              reviewer_email=review.get('reviewerEmail'),
              defaults={
                  'rating': review.get('rating'),
                  'comment': review.get('comment'),
                  'date': review.get('date'), 
                  'reviewer_name': review.get('reviewerName'),
          }
        )
    self.stdout.write(self.style.SUCCESS(f'Successfully imported products'))

  def handleCarts(self,*args,**kwargs):
    # ExternalCart.objects.all().delete()
    # Product.objects.all().delete()

    self.stdout.write("Fetching Carts data...")    
    response = requests.get('https://dummyjson.com/carts?limit=25')
    data = response.json()
    carts_data = data.get('carts',[])

    all_users = list(ExternalUser.objects.all().order_by('id'))

    for cart_json , user_json in zip(carts_data,all_users):
      product_instances = []
      for product in cart_json.get('products',[]):
        product_object = Product.objects.create(
          external_product_id=product.get('id'),
          title=product.get('title'),
          price=product.get('price'),
          quantity=product.get('quantity'),
          total=product.get('total'),
          discount_percentage=product.get('discountPercentage'),
          discounted_total=product.get('discountedTotal'),
          thumbnail=product.get('thumbnail')        
      )
        product_instances.append(product_object)

      cart_obj = ExternalCart.objects.create(
        external_id=cart_json.get('id'),
        total=cart_json.get('total'),
        discounted_total=cart_json.get('discountedTotal'),
        # user_id=carts_data.get('userId'),
        user = user_json,
        total_products=cart_json.get('totalProducts'),
        total_quantity=cart_json.get('totalQuantity')
      )

      # cart_obj.products.add(*product_instances)
      cart_obj.products.set(*product_instances) #.set() will better than .add() for ManyToMany

    self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(carts_data)} carts"))