import requests
import logging
from django.core.management.base import BaseCommand
from users.models import ExternalUser, Address, Company
from products.models import ExternalProduct, Tag
from carts.models import ExternalCart, Product
from .data_utils import export_json, export_csv

user_logger = logging.getLogger('sync_user')
product_logger = logging.getLogger('sync_product')
cart_logger = logging.getLogger('sync_cart')

class Command(BaseCommand):
    help = 'Fetch and clean User data from DummyJSON'

    def add_arguments(self, parser):
        parser.add_argument('--action', type=str, help='create,update,delete', default='create')

    def handle(self, *args, **options):
        action = options.get('action', 'create')
        if action == 'delete':
            self.clear_all_data()
        elif action == 'update':
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
        response = requests.get('https://dummyjson.com/products?limit=50')
        products = response.json().get('products', [])
        updated_count = 0

        for product in products:
            ext_id = product.get('id')
            new_price = product.get('price')
            new_rating = product.get('rating')

            try:
                obj = ExternalProduct.objects.get(external_id=ext_id)
                old_price = obj.price
                old_rating = obj.rating

                if old_price != new_price or old_rating != new_rating:
                    obj.price = new_price
                    obj.rating = new_rating
                    obj.save()
                    updated_count += 1
                    
                    product_logger.info(
                        f"PRODUCT ID {ext_id} UPDATED: "
                        f"Price: [{old_price} -> {new_price}], "
                        f"Rating: [{old_rating} -> {new_rating}]"
                    )
            except ExternalProduct.DoesNotExist:
                product_logger.warning(f"Product {ext_id} not found, skipping update.")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} products' prices."))

    def sync_all_data(self):
        self.handleUser()
        self.handleProduct()
        self.handleCarts()

    def handleUser(self, *args, **kwargs):
        ExternalUser.objects.all().delete()
        Address.objects.all().delete()
        Company.objects.all().delete()

        response = requests.get('https://dummyjson.com/users?limit=50')
        users = response.json().get('users', [])

        for u in users:
            username = u.get('username')
            if not username: continue

            addr_data = u.get('address', {})
            home_address, _ = Address.objects.update_or_create(
                address=addr_data.get('address'),
                city=addr_data.get('city'),
                defaults={
                    'state': addr_data.get('state'),
                    'state_code': addr_data.get('stateCode'),
                    'postal_code': addr_data.get('postalCode'),
                    'country': addr_data.get('country'),
                    'lat': addr_data.get('coordinates', {}).get('lat'),
                    'lng': addr_data.get('coordinates', {}).get('lng'),
                }
            )

            comp_data = u.get('company', {})
            comp_addr_data = comp_data.get('address', {})
            
            comp_address, _ = Address.objects.update_or_create(
                address=comp_addr_data.get('address', 'N/A'),
                city=comp_addr_data.get('city', 'N/A'),
                defaults={
                    'state': comp_addr_data.get('state', 'N/A'),
                    'country': comp_addr_data.get('country', 'N/A'),
                }
            )

            company_obj, _ = Company.objects.update_or_create(
                name=comp_data.get('name'),
                defaults={
                    'department': comp_data.get('department'),
                    'title': comp_data.get('title'),
                    'address': comp_address,
                }
            )

            user_defaults = {
                'external_id': u.get('id'),
                'first_name': u.get('firstName'),
                'last_name': u.get('lastName'),
                'maiden_name': u.get('maiden_name','N/A'),
                'age': u.get('age', 0),
                'gender': u.get('gender', ''),
                'email': u.get('email'),
                'phone': u.get('phone', ''),
                'username': u.get('username', 'N/A'),
                'password': u.get('password', 'N/A'),
                'birth_date': u.get('birth_date'),
                'image_url': u.get('image', 'N/A'),
                'blood_group': u.get('blood_group', 'N/A'),
                'height': u.get('height', 0),
                'weight': u.get('birth_date', 0),
                'eye_color': u.get('eye_color', 'N/A'),
                'hair_color': u.get('hair_color', 'N/A'),
                'hair_type': u.get('hair_type', 'N/A'),
                'address': home_address,
                'company': company_obj,
                'card_number': u.get('card_number', 'N/A'),
                'crypto_wallet': u.get('crypto_wallet', 'N/A'),
                'role': u.get('role', 'user'),
            }

            obj, created = ExternalUser.objects.update_or_create(
                username=username,
                defaults=user_defaults
            )
            
            if created:
                user_logger.info(f"USER CREATED: {username}")
            else:
                user_logger.info(f"USER SYNCED: {username}")

            export_json(users, 'backup_users.json')
            export_csv(users, 'backup_users.csv')

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(users)} users'))

    def handleProduct(self, *args, **kwargs):
        self.stdout.write("Fetching Products data...")
        response = requests.get('https://dummyjson.com/products?limit=50')
        products = response.json().get('products', [])

        for product in products:
            ext_id = product.get('id')
            
            product_data = {
                'title': product.get('title'),
                'description': product.get('description'),
                'category': product.get('category'),
                'price': product.get('price', 0),
                'discount_percentage': product.get('discountPercentage', 0),
                'rating': product.get('rating', 0),
                'stock': product.get('stock', 0),
                'brand': product.get('brand'),
                'sku': product.get('sku','N/A'),
                'weight': product.get('weight',0),
                'dimensions_width': product.get('dimensions_width',0),
                'dimensions_height': product.get('dimensions_height',0),
                'dimensions_depth': product.get('dimensions_depth',0),
                'warranty_information': product.get('warranty_information','N/A'),
                'shipping_information': product.get('shipping_information','N/A'),
                'availability_status': product.get('availability_status','N/A'),
                'return_policy': product.get('return_policy','N/A'),
                'thumbnail': product.get('thumbnail'),
            }

            old_obj = ExternalProduct.objects.filter(external_id=ext_id).first()
            
            obj, created = ExternalProduct.objects.update_or_create(
                external_id=ext_id,
                defaults=product_data
            )

            if created:
                if float(old_obj.price) != float(product_data['price']):
                    product_logger.info(f"PRODUCT {ext_id} PRICE CHANGE: [{old_obj.price} -> {product_data['price']}]")
            else:
                product_logger.info(f"PRODUCT CREATED: {product_data['title']} (ID: {ext_id})")

            export_json(products, 'backup_products.json')
            export_csv(products, 'backup_products.csv')

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(products)} products'))    
    
    def handleCarts(self, *args, **kwargs):
        self.stdout.write("Fetching Carts data...")    
        response = requests.get('https://dummyjson.com/carts?limit=50')
        carts_data = response.json().get('carts', [])
        all_users = list(ExternalUser.objects.all().order_by('id'))

        for cart_json, user_json in zip(carts_data, all_users):
            cart_ext_id = cart_json.get('id')
            new_discounted_total = cart_json.get('discountedTotal', 0)

            product_instances = []
            for p in cart_json.get('products', []):
                p_ext_id = p.get('id')
                
                p_obj, _ = Product.objects.update_or_create(
                    external_product_id=p_ext_id,
                    defaults={
                        'title': p.get('title'),
                        'price': p.get('price', 0),
                        'quantity': p.get('quantity', 0),
                        'total': p.get('total', 0),
                        'discount_percentage': p.get('discountPercentage', 0),
                        'discounted_total': p.get('discountedTotal', 0),
                        'thumbnail': p.get('thumbnail', '')
                    }
                )
                product_instances.append(p_obj)

            cart_obj, created = ExternalCart.objects.update_or_create(external_id=cart_ext_id)
            
            if created:
                cart_logger.info(f"CART CREATED: ID {cart_ext_id} for User {user_json.username}")
            else:
                old_discounted = float(cart_obj.discounted_total or 0)
                if old_discounted != float(new_discounted_total):
                    cart_logger.info(
                        f"CART ID {cart_ext_id} UPDATED: "
                        f"Discounted Total: [{old_discounted} -> {new_discounted_total}]"
                    )

            cart_obj.total = cart_json.get('total', 0)
            cart_obj.discounted_total = new_discounted_total
            cart_obj.user = user_json
            cart_obj.total_products = cart_json.get('totalProducts', 0)
            cart_obj.total_quantity = cart_json.get('totalQuantity', 0)
            cart_obj.save()
            
            cart_obj.products.set(product_instances)

            export_json(carts_data, 'backup_carts_data.json')
            export_csv(carts_data, 'backup_carts_data.csv')
            
        self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(carts_data)} carts"))