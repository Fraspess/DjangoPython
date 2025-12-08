import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Category
from django.utils.text import slugify
from unidecode import unidecode

def show_categories(request):
    categories = Category.objects.all()
    return render(request,'categories.html',{'categories':categories})
# Create your views here.


def add_category(request):
    print(request)
    if request.method == "POST":
        category_name = request.POST.get("name")
        print(category_name)
        category_slug = slugify(unidecode(category_name))
        category_description = request.POST.get("description")
        category_is_active = request.POST.get("is_active") == "checked"
        category_image = request.FILES.get("image")

        category_created_at = datetime.datetime.now()
        category_updated_at = datetime.datetime.now()

        category = Category(name = category_name, slug = category_slug, description = category_description, created_at = category_created_at, updated_at = category_updated_at, is_active = category_is_active, image = category_image)
        category.save()

        return redirect('/categories/')
    return render(request, "add_category.html")