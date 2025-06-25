from django.shortcuts import render, redirect, get_object_or_404
from .models import  HistorialMovimiento
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from datetime import datetime, timedelta
from .forms import *
import pandas as pd
from .forms import ExcelUploadForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import HistorialMovimiento
from django.contrib.auth import logout


def logout_custom(request):
    logout(request)
    return redirect('login') 

@login_required
def suppliers_list(request):
    suppliers = Suppliers.objects.all()
    return render(request, 'inv/suppliers_list.html', {'suppliers': suppliers})
@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = suplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = suplierForm()
    return render(request, 'inv/suppliers_form.html', {'form': form})
@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        form = suplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = suplierForm(instance=supplier)
    return render(request, 'inv/supplier_form.html', {'form': form})
@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers_list')
    return render(request, 'inv/supplier_confirm_delete.html', {'supplier': supplier})

@login_required
def users_view(request):
    users = User.objects.all()
    return render(request, 'inv/users.html', {'users': users})

def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = "Las contraseñas no coinciden."
        elif User.objects.filter(username=username).exists():
            error = "El usuario ya existe."
        elif User.objects.filter(email=email).exists():
            error = "El email ya está registrado."
        else:
            user = User.objects.create_user(username=username, password=password1, email=email)
            login(request, user)
            return redirect('index')
    return render(request, 'inv/register.html', {'error': error})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            error = "Usuario o contraseña incorrectos."
    return render(request, 'inv/login.html', {'error': error})



@login_required
def historial(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('type', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    movimientos_list = HistorialMovimiento.objects.all().order_by('-fecha')

    if query:
        movimientos_list = movimientos_list.filter(nombre_producto__icontains=query)

    if tipo:
        movimientos_list = movimientos_list.filter(tipo_producto=tipo)

    try:
        if start:
            start_date = datetime.strptime(start, "%Y-%m-%d")
        else:
            start_date = None

        if end:
            # le sumamos 1 día para incluir todos los registros del día seleccionado
            end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        else:
            end_date = None

        # validamos coherencia
        if start_date and end_date:
            if start_date > end_date:
                movimientos_list = movimientos_list.none()
            else:
                movimientos_list = movimientos_list.filter(fecha__gte=start_date, fecha__lt=end_date)
        elif start_date:
            movimientos_list = movimientos_list.filter(fecha__gte=start_date)
        elif end_date:
            movimientos_list = movimientos_list.filter(fecha__lt=end_date)

    except ValueError:
        pass  # Si alguna fecha es inválida, simplemente no filtra por fecha

    paginator = Paginator(movimientos_list, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)

    return render(request, 'inv/historial.html', {'movimientos': movimientos})
@login_required
def index(request):
    # Get last 10 added products (by date_added, not edited)
    latest_items = Producto.objects.all().order_by('-date_added')[:10]
    
    # Get 10 products with lowest stock (including 0)
    least_stock_items = Producto.objects.all().order_by('stock', 'date_added')[:10]
    
    context = {
        'latest_items': latest_items,
        'least_stock_items': least_stock_items
    }
    
    return render(request, 'inv/index.html', context)


@login_required
def inventario(request):
    query = request.GET.get('q', '')
    product_type_filter = request.GET.get('type', '')
    
    # Get all products
    productos = Producto.objects.all().order_by('-date_added')
    
    # Apply filters
    if query:
        productos = productos.filter(
            Q(name__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type_filter:
        productos = productos.filter(product_type__name=product_type_filter)
    
    # Get all product types for the filter dropdown
    product_types = ProductType.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    context = {
        'productos': productos,
        'product_types': product_types,
        'current_query': query,
        'current_type': product_type_filter
    }
    
    return render(request, 'inv/inventario.html', context)


@login_required
def add_item(request, cls):
    if request.method == "POST":
        form = cls(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = cls()
    return render(request, 'inv/add_new.html', {'form': form})

@login_required
def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)
    stock_field = 'stock'
    stock_anterior = getattr(item, stock_field, None)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        motivo = request.POST.get('motivo', 'Edición manual')
        if form.is_valid():
            updated_item = form.save(commit=False)
            stock_nuevo = getattr(updated_item, stock_field, None)
            cambio_stock = 0
            stock_final = stock_anterior
            if stock_anterior is not None and stock_nuevo is not None and stock_anterior != stock_nuevo:
                cambio_stock = stock_nuevo - stock_anterior
                stock_final = stock_nuevo
            # Always create historial entry
            HistorialMovimiento.objects.create(
                producto_id=item.id,
                nombre_producto=getattr(updated_item, 'name', ''),
                tipo_producto=getattr(updated_item, 'type', ''),
                codigo_barras=getattr(updated_item, 'codigo_barras', ''),
                cambio_stock=cambio_stock,
                stock_final=stock_final,
                motivo=motivo,
                usuario=request.user
            )
            updated_item.save()
            return redirect('inventario')
    else:
        form = cls(instance=item)
    return render(request, 'inv/edit_item.html', {'form': form})

@login_required
def upload_products_excel(request):
    msg = ""
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                print(row)
                model_name = row['type']
                model = MODEL_MAP.get(model_name)
                if not model:
                    print(f"Tipo '{model_name}' no reconocido. Fila omitida.")
                    continue
                obj, created = model.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'price': row['price'],
                        'stock': row.get('stock', 0),
                        'type': row['type'],
                        'codigo_barras': row.get('codigo_barras', ''),
                    }
                )
            msg = "Productos cargados o actualizados exitosamente."
    else:
        form = ExcelUploadForm()
    return render(request, 'inv/upload_products_excel.html', {'form': form, 'msg': msg})

def detalle_historial(request, pk):
    movimiento = get_object_or_404(HistorialMovimiento, pk=pk)
    return render(request, 'inv/detalle_historial.html', {'movimiento': movimiento})



@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            # Create history entry for new product
            HistorialMovimiento.objects.create(
                producto_id=producto.id,
                nombre_producto=producto.name,
                tipo_producto=producto.product_type.name,
                codigo_barras=producto.codigo_barras or '',
                cambio_stock=producto.stock,
                stock_final=producto.stock,
                motivo='Producto creado',
                usuario=request.user
            )
            return redirect('inventario')
    else:
        form = ProductoForm()
    return render(request, 'inv/add_new.html', {'form': form})

@login_required
def producto_list(request):
    query = request.GET.get('q', '')
    product_type = request.GET.get('product_type', '')
    
    productos = Producto.objects.all().order_by('-date_added')
    
    if query:
        productos = productos.filter(
            Q(name__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type:
        productos = productos.filter(product_type__id=product_type)
    
    # Get all product types for filter dropdown
    product_types = ProductType.objects.filter(is_active=True)
    
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    return render(request, 'inv/producto_list.html', {
        'productos': productos, 
        'product_types': product_types,
        'current_query': query,
        'current_type': product_type
    })

@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Get recent movements for this product
    movimientos = HistorialMovimiento.objects.filter(producto_id=pk).order_by('-fecha')[:10]
    return render(request, 'inv/producto_detail.html', {
        'producto': producto,
        'movimientos': movimientos
    })
@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    stock_anterior = producto.stock
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        motivo = request.POST.get('motivo', 'Producto editado')
        if form.is_valid():
            updated_producto = form.save()
            stock_nuevo = updated_producto.stock
            cambio_stock = stock_nuevo - stock_anterior
            
            # Create history entry
            HistorialMovimiento.objects.create(
                producto_id=updated_producto.id,
                nombre_producto=updated_producto.name,
                tipo_producto=updated_producto.product_type.name,
                codigo_barras=updated_producto.codigo_barras or '',
                cambio_stock=cambio_stock,
                stock_final=stock_nuevo,
                motivo=motivo,
                usuario=request.user
            )
            return redirect('producto_detail', pk=pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inv/edit_item.html', {  # Changed from producto_form.html
        'form': form, 
        'producto': producto
    })


@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Create history entry before deletion
        HistorialMovimiento.objects.create(
            producto_id=producto.id,
            nombre_producto=producto.name,
            tipo_producto=producto.product_type.name,
            codigo_barras=producto.codigo_barras or '',
            cambio_stock=-producto.stock,
            stock_final=0,
            motivo='Producto eliminado',
            usuario=request.user
        )
        producto.delete()
        return redirect('producto_list')
    return render(request, 'inv/producto_confirm_delete.html', {'producto': producto})