from django.urls import path
from . import views

app_name="categories"

urlpatterns = [
    path('', views.show_categories, name='show_categories'),
    path('add/', views.add_category, name='add_category'),
    path('delete/',views.delete_category, name='delete_category'),
    path('edit/',views.edit_category, name='edit_category'),
]