from django.shortcuts import render
from users.models import ExternalUser
from products.models import ExternalProduct
from carts.models import ExternalCart

# Create your views here.
def dashboard_view(request):
  users = ExternalUser.objects.all()
  products = ExternalProduct.objects.all()
  carts = ExternalCart.objects.all()

  context = {
    'users': users,
    'products': products,
    'carts': carts,
  }
  
  return render(request,'dashboard.html',context)