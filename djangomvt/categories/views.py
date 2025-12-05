from django.shortcuts import render

from .models import Category

def show_categories(request):
    categories = Category.objects.all()
    return render(request,'categories.html',{'categories':categories})
# Create your views here.


def add_category(request):
    return render(request, "add_category.html")