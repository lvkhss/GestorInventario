from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

# Ver productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

# Crear producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/formulario_producto.html', {'form': form, 'accion': 'Crear'})

# Editar producto
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/formulario_producto.html', {'form': form, 'accion': 'Editar'})

# Eliminar producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/confirmar_eliminar.html', {'producto': producto})
