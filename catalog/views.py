from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, 'catalog/base.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def index(request):
    return render(request, 'catalog/index.html')


def about(request):
    return render(request, 'catalog/about.html')


def menu(request):
    return render(request, 'catalog/menu.html')


def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products.html', context)
