from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product
import json


def get_products(request):
    products = Product.objects.all().values('name', 'description', 'quantity', 'price')
    return JsonResponse(list(products), safe=False)

def get_date(request):
    dates = Product.objects.all().values('date')
    return JsonResponse(list(dates), safe=False)

def index(request):
   return render(request, 'inventory/index.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'inventory/product_detail.html', {'product': product})

def get_products_by_dates(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    products = Product.objects.filter(date_added__range=(start_date, end_date))
    
    data = [{
        'name': product.name,
        'description': product.description,
        'quantity': product.quantity,
        'price': product.price,
    } for product in products]
    
    return JsonResponse(data, safe=False)