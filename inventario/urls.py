from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('proveedores/', views.proveedores_view, name='proveedores'),
]
