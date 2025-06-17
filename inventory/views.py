from django.shortcuts import render, redirect, get_object_or_404
from django.db import OperationalError
from .models import Sellantes, Herramientas, Pinturas, HistorialMovimiento
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from datetime import datetime
from .forms import *
import pandas as pd
from .models import ProductoReal, Sellantes, Herramientas, Pinturas
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
def inventario(request):
    return render(request, 'inv/inventario.html')

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

    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            movimientos_list = movimientos_list.filter(fecha__gte=start_date)
        except ValueError:
            pass

    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            movimientos_list = movimientos_list.filter(fecha__lte=end_date)
        except ValueError:
            pass

    paginator = Paginator(movimientos_list, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)

    return render(request, 'inv/historial.html', {'movimientos': movimientos})
@login_required
# views.py
def index(request):
    try:
        sellantes = Sellantes.objects.all()
    except OperationalError:
        sellantes = []

    try:
        herramientas = Herramientas.objects.all()
    except OperationalError:
        herramientas = []

    try:
        pinturas = Pinturas.objects.all()
    except OperationalError:
        pinturas = []

    all_items = [
        {"item": sellante, "category": "Sellantes"} for sellante in sellantes
    ] + [
        {"item": herramienta, "category": "Herramientas"} for herramienta in herramientas
    ] + [
        {"item": pintura, "category": "Pinturas"} for pintura in pinturas
    ]

    # Last 10 added products (by date_added descending)
    latest_items = sorted(
        all_items,
        key=lambda x: getattr(x["item"], "date_added", None) or 0,
        reverse=True
    )[:10]

    # 10 products with the least stock (ascending)
    least_stock_items = sorted(
        all_items,
        key=lambda x: getattr(x["item"], "stock", None) if getattr(x["item"], "stock", None) is not None else float('inf')
    )[:10]

    context = {
        'latest_items': latest_items,
        'least_stock_items': least_stock_items,
    }
    return render(request, 'inv/index.html', context)
@login_required
def inventario(request):
    q = request.GET.get('q', '')
    tipo = request.GET.get('type', '')

    sellantes = Sellantes.objects.all()
    herramientas = Herramientas.objects.all()
    pinturas = Pinturas.objects.all()

    if q:
        sellantes = sellantes.filter(name__icontains=q)
        herramientas = herramientas.filter(name__icontains=q)
        pinturas = pinturas.filter(name__icontains=q)

    if tipo:
        # Filtra solo la categoría elegida, vacía las otras
        if tipo == "Sellantes":
            herramientas = Herramientas.objects.none()
            pinturas = Pinturas.objects.none()
        elif tipo == "Herramientas":
            sellantes = Sellantes.objects.none()
            pinturas = Pinturas.objects.none()
        elif tipo == "Pinturas":
            sellantes = Sellantes.objects.none()
            herramientas = Herramientas.objects.none()

    items = [
        {"item": sellante, "category": "Sellantes"} for sellante in sellantes
    ] + [
        {"item": herramienta, "category": "Herramientas"} for herramienta in herramientas
    ] + [
        {"item": pintura, "category": "Pinturas"} for pintura in pinturas
    ]

    context = {
        'items': items,
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
def add_herramienta(request):
    return add_item(request, HerramientaForm)
@login_required
def add_sellante(request):
    return add_item(request, SellanteForm)
@login_required
def add_pintura(request):
    return add_item(request, PinturaForm)
@login_required
def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)
    stock_field = 'stock'  # Adjust if your field is named differently
    stock_anterior = getattr(item, stock_field, None)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        if form.is_valid():
            updated_item = form.save(commit=False)
            stock_nuevo = getattr(updated_item, stock_field, None)
            if stock_anterior is not None and stock_nuevo is not None and stock_anterior != stock_nuevo:
                # Save history only if stock changed
                HistorialMovimiento.objects.create(
                    producto_id=item.id,
                    nombre_producto=getattr(item, 'name', ''),  
                    tipo_producto=getattr(item, 'type', ''),   
                    codigo_barras=getattr(item, 'codigo_barras', ''), 
                    cambio_stock=stock_nuevo - stock_anterior,
                    stock_final=stock_nuevo,
                    motivo=request.POST.get('motivo', 'Edición manual'),
                    usuario=request.user # Add the username of the user making the change
                )
            updated_item.save()
            return redirect('inventario')
    else:
        form = cls(instance=item)
    return render(request, 'inv/edit_item.html', {'form': form})
@login_required
def edit_herramienta(request, pk):
    return edit_item(request, pk, Herramientas, HerramientaForm)
@login_required
def edit_sellante(request, pk):
    return edit_item(request, pk, Sellantes, SellanteForm)
@login_required
def edit_pintura(request, pk):
    return edit_item(request, pk, Pinturas, PinturaForm)
@login_required
def delete_herramienta(request, pk):
    Herramientas.objects.filter(id=pk).delete()
    return redirect('inventario')
@login_required
def delete_sellante(request, pk):
    Sellantes.objects.filter(id=pk).delete()
    return redirect('inventario') 
@login_required
def delete_pintura(request, pk):
    Pinturas.objects.filter(id=pk).delete()
    return redirect('inventario')
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['type']
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            codigo_barras = form.cleaned_data.get('codigo_barras', '')

            if tipo == 'Sellantes':
                Sellantes.objects.create(name=name, codigo_barras=codigo_barras, price =price, type=tipo)
            elif tipo == 'Herramientas':
                Herramientas.objects.create(name=name, codigo_barras=codigo_barras, price =price, type=tipo)
            elif tipo == 'Pinturas':
                Pinturas.objects.create(name=name, codigo_barras=codigo_barras, price =price, type=tipo)

            return redirect('inventario')
    else:
        form = ProductoForm()

    return render(request, 'inv/add_new.html', {'form': form, 'header': 'Agregar Producto'})

MODEL_MAP = {
    'ProductoReal': ProductoReal,
    'Sellantes': Sellantes,
    'Herramientas': Herramientas,
    'Pinturas': Pinturas,
}
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

