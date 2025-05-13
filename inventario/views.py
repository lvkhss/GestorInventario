from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

# Ver productos
def lista_productos(request):
    return render(request, 'inventario/lista_productos.html')

def inventario_view(request):
    return render(request, 'inventario/inventario.html') 

def proveedores_view(request):
    return render(request, 'inventario/proveedores.html')
