from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
from .tasks import all_bucket_objects_task

from django.conf import settings
# Create your views here.

class HomeView(View):


    def get(self, request):
        products = Product.objects.filter(available=True)
        for product in products:
            print(product.image.url)
        return render(request, 'home/home.html', {'products': products})


class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/product_detail.html', {'product': product})

class BucketHome(View):
    templates_name='home/bucket.html'


    def get(self,request):
        objects = all_bucket_objects_task()
        return render(request,self.templates_name,{'objects':objects})