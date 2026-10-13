from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.all()[:10]
    return render(request, 'home/index.html', {'products': products})
