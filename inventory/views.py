from django.shortcuts import render, redirect, get_object_or_404
from .models import HistorialMovimiento, Suppliers 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from .forms import *
import pandas as pd
from .forms import ExcelUploadForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import HistorialMovimiento
from django.contrib.auth import logout
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from .decorators import staff_required

MODEL_MAP = {
    'producto': Producto,  
}

from django.contrib import messages
from .models import ProductType
@staff_required
def delete_product_type(request, pk):
    ProductType.objects.filter(pk=pk).delete()
    messages.success(request, "Tipo de producto eliminado.")
    return redirect('settings_view')

@staff_required
def settings_view(request):
    if request.method == 'POST':
        name_value = request.POST.get('type', '').strip() 
        description = request.POST.get('description', '').strip()
        if not name_value:
            messages.error(request, "El tipo es obligatorio.")
        elif ProductType.objects.filter(name__iexact=name_value).exists():
            messages.error(request, "Ya existe un tipo de producto con ese nombre.")
        else:
            ProductType.objects.create(name=name_value, description=description)
            messages.success(request, "Tipo de producto creado exitosamente.")
    product_types = ProductType.objects.all()
    return render(request, 'inv/settings.html', {'product_types': product_types})
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
        form = SupplierForm(request.POST)
        if form.is_valid():
            try:
                supplier = form.save()
                messages.success(request, f'Proveedor "{supplier.empresa}" creado exitosamente.')
                return redirect('suppliers_list')
            except ValidationError as e:
                messages.error(request, f'Error al crear proveedor: {e}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = SupplierForm()
    
    return render(request, 'inv/suppliers_form.html', {  # Change this line
        'form': form,
        'title': 'Crear Proveedor'
    })

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            try:
                supplier = form.save()
                messages.success(request, f'Proveedor "{supplier.empresa}" actualizado exitosamente.')
                return redirect('suppliers_list')
            except ValidationError as e:
                messages.error(request, f'Error al actualizar proveedor: {e}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'inv/suppliers_form.html', {  # Change this line
        'form': form,
        'title': 'Editar Proveedor',
        'supplier': supplier
    })

@login_required
def supplier_delete(request, pk):
    try:
        supplier = Suppliers.objects.get(pk=pk)
        supplier.delete()
        messages.success(request, 'Proveedor eliminado exitosamente')
    except Suppliers.DoesNotExist:
        messages.error(request, 'El proveedor no existe o ya fue eliminado')
    
    return redirect('suppliers_list')

@staff_required
def users_view(request):
    users = User.objects.all()
    return render(request, 'inv/users.html', {'users': users})

@staff_required
def register_view(request):
    error = None
    success_message = None
    if request.method == 'POST':
        print(f"POST data received: {request.POST}")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        print(f"Username: {username}, Email: {email}")
        print(f"Password1: {'presente' if password1 else 'ausente'}")
        print(f"Password2: {'presente' if password2 else 'ausente'}")
        
        if password1 != password2:
            error = "Las contraseñas no coinciden."
            print("ERROR: Las contraseñas no coinciden")
        elif User.objects.filter(username=username).exists():
            error = "El usuario ya existe."
            print(f"ERROR: Usuario {username} ya existe")
        elif User.objects.filter(email=email).exists():
            error = "El email ya está registrado."
            print(f"ERROR: Email {email} ya está registrado")
        else:
            try:
                print("Intentando crear usuario...")
                user = User.objects.create_user(username=username, password=password1, email=email)
                print(f"Usuario creado exitosamente: {username}")
                success_message = f"Usuario '{username}' creado exitosamente"
            except Exception as e:
                print(f"Error creando usuario: {e}")
                error = f"Error al crear usuario: {e}"
    return render(request, 'inv/register.html', {'error': error, 'success_message': success_message})

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
    product_type_filter = request.GET.get('type', '')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    movimientos = HistorialMovimiento.objects.all().order_by('-fecha')
    
    # Apply filters
    if query:
        movimientos = movimientos.filter(
            Q(nombre_producto__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type_filter:
        movimientos = movimientos.filter(tipo_producto=product_type_filter)
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            movimientos = movimientos.filter(fecha__date__gte=start_date)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            movimientos = movimientos.filter(fecha__date__lte=end_date)
        except ValueError:
            pass
    

    for mov in movimientos:
        mov.stock_inicial = mov.stock_final - mov.cambio_stock
    
    # Pagination
    paginator = Paginator(movimientos, 20)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    

    product_types = HistorialMovimiento.objects.values_list('tipo_producto', flat=True).distinct().order_by('tipo_producto')
    
    context = {
        'movimientos': movimientos,
        'product_types': product_types,  
        'current_query': query,
        'current_type': product_type_filter,
        'current_start': request.GET.get('start', ''),
        'current_end': request.GET.get('end', ''),
    }
    
    return render(request, 'inv/historial.html', context)

@login_required
def profile(request):
    """Vista para mostrar el perfil del usuario"""
    return render(request, 'inv/profile.html', {
        'user': request.user
    })

@login_required
def user_movements(request):
    """Vista para mostrar los movimientos del usuario logueado"""
    query = request.GET.get('q', '')
    product_type_filter = request.GET.get('type', '')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    # Filtrar movimientos por el usuario logueado
    movimientos = HistorialMovimiento.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Apply filters (same as historial view)
    if query:
        movimientos = movimientos.filter(
            Q(nombre_producto__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type_filter:
        movimientos = movimientos.filter(tipo_producto=product_type_filter)
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            movimientos = movimientos.filter(fecha__date__gte=start_date)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            movimientos = movimientos.filter(fecha__date__lte=end_date)
        except ValueError:
            pass
    
    # Calculate stock inicial for each movement
    for mov in movimientos:
        mov.stock_inicial = mov.stock_final - mov.cambio_stock
    
    # Pagination
    paginator = Paginator(movimientos, 20)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    
    # Get product types from user's movements only
    product_types = HistorialMovimiento.objects.filter(usuario=request.user).values_list('tipo_producto', flat=True).distinct().order_by('tipo_producto')
    
    context = {
        'movimientos': movimientos,
        'product_types': product_types,  
        'current_query': query,
        'current_type': product_type_filter,
        'current_start': request.GET.get('start', ''),
        'current_end': request.GET.get('end', ''),
        'user': request.user
    }
    
    return render(request, 'inv/user_movements.html', context)

@login_required
def index(request):
    
    latest_items = Producto.objects.all().order_by('-date_added')[:10]
    
   
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
    
 
    productos = Producto.objects.all().order_by('-date_added')
    
   
    if query:
        productos = productos.filter(
            Q(name__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type_filter:
        productos = productos.filter(product_type__name=product_type_filter)
    
  
    product_types = ProductType.objects.filter(is_active=True)
    

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
                producto_id=producto.id,
    nombre_producto=producto.name,
    tipo_producto=producto.product_type.name,
    codigo_barras=producto.codigo_barras,
    cambio_stock=cambio_stock,
    stock_final=producto.stock,
    motivo=motivo,
    usuario=request.user,
    precio=producto.price, 
)
            updated_item.save()
            return redirect('inventario')
    else:
        form = cls(instance=item)
    return render(request, 'inv/edit_item.html', {'form': form})

@login_required
def upload_products_excel(request):
    success_message = None
    debug_info = [] 
    
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            
            try:
               
                df = pd.read_excel(excel_file)
                
               
                existing_types = ProductType.objects.filter(is_active=True)
                existing_type_names = [pt.name.lower() for pt in existing_types]
                type_mapping = {pt.name.lower(): pt for pt in existing_types}
                
                success_count = 0
                error_count = 0
                
                for index, row in df.iterrows():
                    try:
                        tipo_input = str(row.get('tipo', '')).strip()
                        nombre = str(row.get('nombre', '')).strip()
                        codigo_barras = str(row.get('codigo de barras', '')).strip()
                        
          
                        debug_info.append(f"Row {index+1}: nombre='{nombre}', tipo='{tipo_input}'")
                        
             
                        if not nombre:
                            error_count += 1
                            debug_info.append(f"Row {index+1}: SKIPPED - No name")
                            continue
                        
               
                        if not tipo_input:
                            error_count += 1
                            debug_info.append(f"Row {index+1}: SKIPPED - No product type")
                            continue
                            
                        tipo_lower = tipo_input.lower()
                        if tipo_lower not in existing_type_names:
                            error_count += 1
                            debug_info.append(f"Row {index+1}: SKIPPED - Product type '{tipo_input}' not found")
                            continue
    
                        if Producto.objects.filter(name__iexact=nombre).exists():
                            error_count += 1
                            debug_info.append(f"Row {index+1}: SKIPPED - Duplicate name '{nombre}'")
                            continue
                        
            
                        if codigo_barras and Producto.objects.filter(codigo_barras=codigo_barras).exists():
                            error_count += 1
                            debug_info.append(f"Row {index+1}: SKIPPED - Duplicate barcode '{codigo_barras}'")
                            continue
                        
                      
                        product_type = type_mapping[tipo_lower]
            
                        product = Producto.objects.create(
                            name=nombre,
                            product_type=product_type,
                            price=float(row.get('precio', 0)),
                            stock=int(row.get('stock', 0)),
                            codigo_barras=codigo_barras if codigo_barras else None
                        )
                        
                        success_count += 1
                        debug_info.append(f"Row {index+1}: SUCCESS - Created '{nombre}'")
                        
                    except Exception as e:
                        error_count += 1
                        debug_info.append(f"Row {index+1}: ERROR - {str(e)}")
                
              
                if success_count > 0:
                    success_message = f"Productos subidos exitosamente: {success_count}"
                
               
                if debug_info:
                    debug_message = "<br>".join(debug_info[:10])
                    messages.info(request, f"Debug info: {debug_message}")
                
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                
    else:
        form = ExcelUploadForm()
    
    return render(request, 'inv/upload_excel.html', {
        'form': form,
        'success_message': success_message
    })

def detalle_historial(request, pk):
    movimiento = get_object_or_404(HistorialMovimiento, pk=pk)
    stock_inicial = movimiento.stock_final - movimiento.cambio_stock
    return render(request, 'inv/detalle_historial.html', {
        'movimiento': movimiento,
        'stock_inicial': stock_inicial,
    })



@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            
            HistorialMovimiento.objects.create(
                producto_id=producto.id,
                nombre_producto=producto.name,
                tipo_producto=producto.product_type.name,
                codigo_barras=producto.codigo_barras or '',
                cambio_stock=producto.stock,
                stock_final=producto.stock,
                motivo='Producto creado',
                usuario=request.user,
                precio=producto.price  # Add this line
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

    movimientos = HistorialMovimiento.objects.filter(producto_id=pk).order_by('-fecha')[:10]
    

    referer = request.GET.get('next') or request.META.get('HTTP_REFERER', '')
    back_url = 'inventario'  
    back_text = 'Inventario'  
    

    if 'historial' in referer:
        back_url = 'historial'
        back_text = 'Historial'
    elif 'inventario' in referer:
        back_url = 'inventario'
        back_text = 'Inventario'
    
    return render(request, 'inv/producto_detail.html', {
        'producto': producto,
        'movimientos': movimientos,
        'back_url': back_url,
        'back_text': back_text
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

            HistorialMovimiento.objects.create(
                producto_id=updated_producto.id,
                nombre_producto=updated_producto.name,
                tipo_producto=updated_producto.product_type.name,
                codigo_barras=updated_producto.codigo_barras or '',
                cambio_stock=cambio_stock,
                stock_final=stock_nuevo,
                motivo=motivo,
                usuario=request.user,
                precio=updated_producto.price  # <-- agrega esto
            )
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inv/edit_item.html', {  
        'form': form, 
        'producto': producto
    })


@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    HistorialMovimiento.objects.create(
        producto_id=producto.id,
        nombre_producto=producto.name,
        tipo_producto=producto.product_type.name,
        codigo_barras=producto.codigo_barras or '',
        cambio_stock=-producto.stock,
        stock_final=0,
        motivo='Producto eliminado',
        usuario=request.user,
        precio=producto.price  # Add this line
    )
    producto.delete()
    return redirect('inventario')

def permission_denied_view(request, exception=None):
    return render(request, 'inv/403.html', status=403)