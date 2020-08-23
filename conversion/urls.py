from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('protein', views.protein, name="protein"),
    path('coding', views.coding, name="coding")
]