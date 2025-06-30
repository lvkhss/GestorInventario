from django.shortcuts import render, redirect, get_object_or_404
from .models import HistorialMovimiento, Suppliers 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from datetime import datetime
from .forms import *
from .forms import UserRegistrationForm, ProductTypeForm
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
from django.contrib.auth.password_validation import validate_password, ValidationError as PasswordValidationError

from django.contrib import messages
from .models import ProductType
@staff_required
def delete_product_type(request, pk):
    if request.method != 'POST':
        messages.error(request, "La eliminación de tipos de producto solo se permite por POST.")
        return redirect('settings_view')
    # Extra: puedes pedir confirmación aquí si quieres
    ProductType.objects.filter(pk=pk).delete()
    messages.success(request, "Tipo de producto eliminado.")
    return redirect('settings_view')


@staff_required
def settings_view(request):
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de producto creado exitosamente.")
            return redirect('settings_view')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = ProductTypeForm()
    
    product_types = ProductType.objects.all()
    return render(request, 'inv/settings.html', {
        'product_types': product_types,
        'form': form
    })
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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                messages.success(request, f"Usuario '{user.username}' creado exitosamente")
                return redirect('users_view')
            except Exception as e:
                messages.error(request, f"Error al crear usuario: {e}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'inv/register.html', {'form': form})

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
    user_filter = request.GET.get('user', '')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    movimientos = HistorialMovimiento.objects.select_related('usuario').all().order_by('-fecha')
    
    # Apply filters
    if query:
        movimientos = movimientos.filter(
            Q(nombre_producto__icontains=query) | 
            Q(codigo_barras__icontains=query)
        )
    
    if product_type_filter:
        movimientos = movimientos.filter(tipo_producto=product_type_filter)
    
    if user_filter:
        movimientos = movimientos.filter(usuario__username=user_filter)
    
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
    # Obtener usuarios que han hecho movimientos
    user_ids = HistorialMovimiento.objects.exclude(usuario__isnull=True).values_list('usuario_id', flat=True).distinct()
    users = User.objects.filter(id__in=user_ids).order_by('username')
    
    context = {
        'movimientos': movimientos,
        'product_types': product_types,
        'users': users,
        'current_query': query,
        'current_type': product_type_filter,
        'current_user': user_filter,
        'current_start': request.GET.get('start', ''),
        'current_end': request.GET.get('end', ''),
    }
    
    return render(request, 'inv/historial.html', context)

@login_required
def profile(request):
    user = request.user
    

    productos_creados = HistorialMovimiento.objects.filter(
        usuario=user,
        motivo='Producto creado'
    ).count()
    
    # Productos editados por el usuario (todos los motivos que representan edición)
    productos_editados = HistorialMovimiento.objects.filter(
        usuario=user
    ).filter(
        Q(motivo='Producto editado') |
        Q(motivo='Edición manual') |
        Q(motivo='Corrección precio') |          
        Q(motivo='Corrección nombre') |          
        Q(motivo__icontains='ajuste de inventario') |
        Q(motivo__icontains='uso interno') |
        Q(motivo__icontains='otro')
    ).count()
    
    # Productos eliminados por el usuario
    productos_eliminados = HistorialMovimiento.objects.filter(
        usuario=user,
        motivo='Producto eliminado'
    ).count()
    
    # Total de ventas (motivo: venta)
    total_ventas = HistorialMovimiento.objects.filter(
        usuario=user,
        motivo__iexact='venta'
    ).count()
    
    # Movimientos totales del usuario
    total_movimientos = HistorialMovimiento.objects.filter(
        usuario=user
    ).count()
    
    # Último movimiento del usuario
    ultimo_movimiento = HistorialMovimiento.objects.filter(
        usuario=user
    ).order_by('-fecha').first()
    
    context = {
        'user': user,
        'productos_creados': productos_creados,
        'productos_editados': productos_editados,
        'productos_eliminados': productos_eliminados,
        'total_ventas': total_ventas,
        'total_movimientos': total_movimientos,
        'ultimo_movimiento': ultimo_movimiento,
    }
    
    return render(request, 'inv/profile.html', context)

@login_required
def user_mov(request):
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
    
    return render(request, 'inv/user_mov.html', context)

@login_required
def index(request):
    
    # Productos más vendidos (por cantidad de ventas en historial)
    ventas = (
        HistorialMovimiento.objects
        .filter(motivo__iexact='venta')
        .values('producto_id', 'nombre_producto', 'tipo_producto')
        .annotate(
            ventas=Count('id'),
            recaudado=Sum('precio')
        )
        .order_by('-ventas', 'nombre_producto')[:10]
    )

    # Obtener info de producto para stock y precio actual
    productos_ids = [v['producto_id'] for v in ventas]
    productos_map = {p.id: p for p in Producto.objects.filter(id__in=productos_ids)}
    productos_mas_vendidos = []
    for v in ventas:
        # Solo productos que existen actualmente
        productos_ids_existentes = set(Producto.objects.values_list('id', flat=True))
        productos_mas_vendidos = []
        for v in ventas:
            if v['producto_id'] in productos_ids_existentes:
                prod = productos_map.get(v['producto_id'])
                productos_mas_vendidos.append({
                    'name': v['nombre_producto'],
                    'tipo': v['tipo_producto'],
                    'ventas': v['ventas'],
                    'stock': prod.stock if prod else '-',
                })

    least_stock_items = Producto.objects.all().order_by('stock', 'date_added')[:10]
    
    context = {
        'productos_mas_vendidos': productos_mas_vendidos,
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
    
  
    product_types = ProductType.objects.filter(is_active=True).order_by('name')
    

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
def upload_products_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():  # Validaciones de archivo se ejecutan automáticamente
            excel_file = request.FILES['file']
            
            try:
                df = pd.read_excel(excel_file)
                existing_types = ProductType.objects.filter(is_active=True)
                type_mapping = {pt.name.lower(): pt for pt in existing_types}
                
                success_count = 0
                error_count = 0
                errors_list = []
                
                for index, row in df.iterrows():
                    try:
                        # Crear form para cada producto para usar validaciones automáticas
                        product_data = {
                            'name': str(row.get('nombre', '')).strip(),
                            'product_type': None,
                            'price': float(row.get('precio', 0)),
                            'stock': int(row.get('stock', 0)),
                            'codigo_barras': str(row.get('codigo de barras', '')).strip() or None
                        }
                        
                        # Buscar tipo de producto
                        tipo_input = str(row.get('tipo', '')).strip().lower()
                        if tipo_input in type_mapping:
                            product_data['product_type'] = type_mapping[tipo_input].id
                        
                        # Usar ProductoForm para validaciones automáticas
                        product_form = ProductoForm(product_data)
                        if product_form.is_valid():
                            product_form.save()
                            success_count += 1
                        else:
                            error_count += 1
                            errors_list.append(f"Fila {index+1}: {'; '.join([f'{field}: {error[0]}' for field, error in product_form.errors.items()])}")
                        
                    except Exception as e:
                        error_count += 1
                        errors_list.append(f"Fila {index+1}: Error - {str(e)}")
                
                # Mostrar resultados
                if success_count > 0:
                    messages.success(request, f"Productos subidos exitosamente: {success_count}")
                
                if error_count > 0:
                    messages.warning(request, f"Productos con errores: {error_count}")
                    for error in errors_list[:5]:  # Mostrar solo los primeros 5 errores
                        messages.error(request, error)
                
            except Exception as e:
                messages.error(request, f"Error procesando archivo: {str(e)}")
        else:
            messages.error(request, 'Por favor corrija los errores en el archivo.')
                
    else:
        form = ExcelUploadForm()
    
    return render(request, 'inv/upload_excel.html', {'form': form})

def detalle_historial(request, pk):
    movimiento = get_object_or_404(HistorialMovimiento, pk=pk)
    stock_inicial = movimiento.stock_final - movimiento.cambio_stock
    return render(request, 'inv/detalle_historial.html', {
        'movimiento': movimiento,
        'stock_inicial': stock_inicial,
    })

@login_required
def detalle_user_mov(request, pk):
    # Verificar que el movimiento pertenece al usuario logueado
    movimiento = get_object_or_404(HistorialMovimiento, pk=pk, usuario=request.user)
    stock_inicial = movimiento.stock_final - movimiento.cambio_stock
    return render(request, 'inv/detalle_user_mov.html', {
        'movimiento': movimiento,
        'stock_inicial': stock_inicial,
    })

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():  # Todas las validaciones se ejecutan automáticamente aquí
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
                precio=producto.price
            )
            messages.success(request, f'Producto "{producto.name}" creado exitosamente.')
            return redirect('inventario')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
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
        if form.is_valid():  # Todas las validaciones se ejecutan automáticamente aquí
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
                precio=updated_producto.price
            )
            messages.success(request, f'Producto "{updated_producto.name}" actualizado exitosamente.')
            return redirect('inventario')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
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

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Datos básicos del usuario
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        new_password2 = request.POST.get('new_password2', '').strip()
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        # Password match validation (always required if changing password)
        if new_password or new_password2:
            if new_password != new_password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'inv/user_edit.html', {'user_obj': user})
            # Password strength validation
            try:
                validate_password(new_password, user)
            except PasswordValidationError as e:
                messages.error(request, e.messages[0])
                return render(request, 'inv/user_edit.html', {'user_obj': user})

        # Validaciones básicas
        if User.objects.exclude(pk=pk).filter(username=username).exists():
            messages.error(request, 'Ya existe un usuario con ese nombre.')
        elif User.objects.exclude(pk=pk).filter(email=email).exists():
            messages.error(request, 'Ya existe un usuario con ese email.')
        else:
            # Actualizar usuario
            user.username = username
            user.email = email.lower()
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            # Cambiar contraseña si se proporciona y es válida
            if new_password:
                user.set_password(new_password)
            user.save()
            messages.success(request, f'Usuario "{username}" actualizado exitosamente.')
            return redirect('users_view')
    return render(request, 'inv/user_edit.html', {'user_obj': user})

@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # No permitir que se elimine a sí mismo
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('users_view')
    
    # No permitir eliminar al último superusuario
    if user.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
        messages.error(request, 'No se puede eliminar al último superusuario del sistema.')
        return redirect('users_view')
    
    username = user.username
    user.delete()
    messages.success(request, f'Usuario "{username}" eliminado exitosamente.')
    return redirect('users_view')

