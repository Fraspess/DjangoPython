from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .forms import CustomUserLogin
from .utils import compress_image
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib import admin
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone = form.cleaned_data['phone']
                if 'image' in request.FILES:
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(300,300))
                    user.image_small.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(800,800))
                    user.image_medium.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(1200,1200))
                    user.image_large.save(image_name, optimized_image, save=False)
                user.save()
                return redirect('categories:show_categories')
            except Exception as e:
                messages.error(request, f'Помилка при реєстрації: {str(e)}')
        else:
            messages.success(request, 'Виправте помилки в формі')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLogin(request, data=request.POST)
        if form.is_valid():
                user = form.get_user()
                login(request,user)
                return redirect('categories:show_categories')            
    else:
        form = CustomUserLogin()
    return render(request, 'login.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('categories:show_categories')


def recover_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email is not None:
            user = CustomUser.objects.filter(email=email).first()
            messages.success(request, 'Інструкції для відновлення пароля надіслані на вашу електронну пошту.')
            if user is not None:
                print()
        return render(request, 'recoverPassword.html')
    return render(request, 'recoverPassword.html')


@login_required(login_url='/users/login')
def user_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        current_user = request.user
        if current_user.is_authenticated:   
            if first_name is not None:
                current_user.first_name = first_name
            if last_name is not None:
                current_user.last_name = last_name
            current_user.save()
    return render(request,'profile.html')