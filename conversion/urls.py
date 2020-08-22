from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('protein_conversion', views.protein_conversion, name="protein_conversion")
]