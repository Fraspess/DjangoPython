from django.shortcuts import render

def homePage(request):
    return render(request, 'home.html')

def registration(request):
    return render(request, 'registration.html')