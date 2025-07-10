# Manual de Sistema - Gestor de Inventario

## Información del Proyecto
- Nombre del Proyecto: GestorInventario
- Versión: 2.0
- Fecha: Enero 2025
- Framework: Django 5.2.1
- Base de Datos: SQLite3 (db.sqlite3)
- Frontend: Bootstrap 5.3, JavaScript Vanilla, CSS3
- Python: 3.7+ (compatible hasta 3.13)

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Modelos de Datos Específicos](#modelos-de-datos-específicos)
4. [Estructura del Código Fuente](#estructura-del-código-fuente)
5. [Lógica de Negocio Específica](#lógica-de-negocio-específica)
6. [APIs y Endpoints](#apis-y-endpoints)
7. [Frontend y Componentes JavaScript](#frontend-y-componentes-javascript)
8. [Configuración y Despliegue](#configuración-y-despliegue)
9. [Mantenimiento y Solución de Problemas](#mantenimiento-y-solución-de-problemas)
10. [Glosario Técnico](#glosario-técnico)
11. [Contacto y Soporte](#contacto-y-soporte)

---

## Introducción

### Propósito del Sistema
El Gestor de Inventario es una aplicación web completa desarrollada en Django 5.2.1 específicamente diseñada para empresas chilenas. Incluye funcionalidades especializadas como validación de RUT chileno, generación de códigos de boleta secuenciales, gestión avanzada de tipos de productos dinámicos, y un sistema de carrito de compras con animaciones interactivas.

### Características Principales
- Gestión de Productos con Tipos Dinámicos: Sistema flexible de categorización
- Validación RUT Chileno: Frontend y backend con algoritmo verificador
- Sistema de Carrito Interactivo: Con animaciones CSS y contador en tiempo real
- Códigos de Boleta Secuenciales: Sistema BOL-00000001 automático
- Gestión de Proveedores: Con datos de contacto y RUT empresarial
- Historial Completo: Seguimiento de todos los movimientos de stock
- Sistema de Roles: Staff y usuarios regulares con permisos diferenciados
- Carga Masiva Excel: Importación de productos vía archivos XLSX
- Interfaz Responsiva: Optimizada para 1280x720 y resoluciones superiores

### Tecnologías Utilizadas
- Backend: Django 5.2.1, Python 3.7+
- Base de Datos: SQLite3 (desarrollo), PostgreSQL (producción)
- Frontend: Bootstrap 5.3, JavaScript ES6, HTML5, CSS3
---

## Arquitectura del Sistema

### Stack Tecnológico Detallado
```
Frontend:
├── Bootstrap 5.3 (framework CSS)
├── JavaScript Vanilla (sin jQuery)
├── CSS3 personalizado (inventory/static/css/style.css)
├── Iconografía SVG inline
└── Animaciones CSS (@keyframes wiggle)

Backend:
├── Django 5.2.1
├── Python 3.7+ (testado hasta 3.13)
├── SQLite3 (archivo: db.sqlite3)
├── WhiteNoise 6.9.0 (servir archivos estáticos)
└── django-import-export 4.3.7 (carga Excel)

Dependencias Clave:
├── pandas 2.3.0 (procesamiento Excel)
├── openpyxl 3.1.5 (lectura archivos Excel)
├── numpy 2.3.0 (cálculos numéricos)
└── django-humanize (formateo de números)
```

### Estructura de Directorios Específica
```
GestorInventario/
├── manage.py                    # Comando Django principal
├── db.sqlite3                  # Base de datos SQLite
├── productos.xlsx              # Archivo ejemplo para carga masiva
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Configuración Docker
│
├── inventory_management_system/  # Configuración Django
│   ├── settings.py             # SECRET_KEY, DEBUG=True, ALLOWED_HOSTS=["*"]
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuración WSGI
│
├── inventory/                   # App principal
│   ├── models.py               # 6 modelos: Suppliers, ProductType, Producto, 
│   │                          #   HistorialMovimiento, CartSale, CartSaleItem
│   ├── views.py                # 30+ vistas (937 líneas)
│   ├── forms.py                # 8 formularios con validaciones (339 líneas)
│   ├── urls.py                 # 20+ endpoints
│   ├── admin.py                # Configuración Django Admin
│   ├── decorators.py           # @staff_required decorator
│   ├── validators.py           # Validadores personalizados
│   │
│   ├── static/inventory/
│   │   ├── css/style.css       # 800+ líneas CSS personalizado
│   │   ├── js/main.js          # JavaScript funcional (carrito, RUT, etc.)
│   │   └── images/pencil.ico   # Favicon personalizado
│   │
│   ├── templates/inv/          # 20+ plantillas HTML
│   │   ├── base.html           # Template base con sidebar responsivo
│   │   ├── index.html          # Dashboard principal
│   │   ├── inventario.html     # Lista de productos
│   │   ├── cart_panel.html     # Panel carrito con badge animado
│   │   └── ...                 # Otras plantillas específicas
│   │
│   └── templatetags/           # Filtros personalizados Django
│       ├── cart_sale_filters.py
│       └── number_filters.py
│
└── staticfiles/                # Archivos estáticos recolectados
    ├── admin/                  # Django Admin assets
    ├── css/, js/, images/      # Assets de la app
    └── import_export/          # Assets django-import-export
```

---

## Modelos de Datos Específicos

### 1. Modelo Suppliers
```python
class Suppliers(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # RUT empresarial
    empresa = models.CharField(max_length=100)          # Nombre empresa
    encargado = models.CharField(max_length=100)        # Persona contacto
    email = models.EmailField(unique=True)              # Email único
    numero = models.CharField(max_length=15)            # Teléfono
    direccion = models.TextField()                      # Dirección completa
```

Características específicas:
- RUT como CharField para manejar guiones y puntos
- Email único para evitar duplicados
- Validación RUT con algoritmo chileno estándar

### 2. Modelo ProductType (Dinámico)
```python
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)       # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
```

Funcionalidad específica:
- Creación dinámica desde panel de configuración
- Soft delete con campo `is_active`
- Solo staff puede crear/eliminar tipos

### 3. Modelo Producto (Unificado)
```python
class Producto(models.Model):
    name = models.CharField(max_length=200, default='Sin nombre')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    price = models.IntegerField()                       # Precio en pesos chilenos
    stock = models.IntegerField(default=0)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(default=now, editable=False)
    
    @property
    def type(self):
        """Retrocompatibilidad con versiones anteriores"""
        return self.product_type.name
```

Características específicas:
- Precio como IntegerField (pesos chilenos sin decimales)
- Código de barras opcional
- Propiedad `type` para retrocompatibilidad
- Método `table_exists()` para verificar migración

### 4. Modelo HistorialMovimiento (Auditoría Completa)
```python
class HistorialMovimiento(models.Model):
    producto_id = models.IntegerField()                 # ID producto
    nombre_producto = models.CharField(max_length=200)
    tipo_producto = models.CharField(max_length=50)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(default=now)
    cambio_stock = models.IntegerField()                # +/- unidades
    stock_final = models.IntegerField()                 # Stock después del cambio
    motivo = models.CharField(max_length=255, blank=True)  # 'Venta', 'Ajuste', etc.
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    precio = models.IntegerField()                      # Precio al momento del movimiento
    boleta_codigo = models.CharField(max_length=32, blank=True, null=True)  # BOL-00000001
```

Funcionalidad específica:
- Conserva información del producto aunque sea eliminado
- Códigos de boleta secuenciales automáticos
- Tracking completo de usuario y timestamp
- Motivos personalizables ('Venta', 'Ajuste Manual', etc.)

### 5. Sistema CartSale (Carrito de Compras)
```python
class CartSale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_code = models.CharField(max_length=64, unique=True)  # UUID único
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total(self):
        return sum(item.quantity * item.price_at_sale for item in self.items.all())
    
    @property
    def total_units(self):
        return sum(item.quantity for item in self.items.all())

class CartSaleItem(models.Model):
    cart_sale = models.ForeignKey(CartSale, related_name='items')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.IntegerField()               # Precio congelado al momento
```

Características específicas:
- Código único por carrito (UUID)
- Precio congelado al momento de agregar
- Propiedades calculadas para total y unidades
- Relación many-to-many a través de CartSaleItem

Categoria (1) ────── (N) Producto
Producto (1) ─────── (N) MovimientoStock

Proveedor ────────────── (Independiente)
```

### Consideraciones de Diseño

1. Denormalización Intencional:
   - `MovimientoStock` almacena `precio_unitario` y `valor_total` para mantener histórico
   - `DetalleVenta` almacena `producto_nombre` para evitar pérdida de datos históricos

2. Integridad Referencial:
   - `CASCADE` en relaciones críticas (Categoria -> Producto)
   - `PROTECT` implícito para evitar eliminación accidental de datos históricos

3. Indexación:
   - Campos `unique=True` crean índices automáticamente
   - `fecha` en modelos de movimiento para consultas temporales eficientes

---

## Estructura del Código Fuente

### Vistas Principales (inventory/views.py - 937 líneas)

#### Vistas de Autenticación y Usuarios
```python
def login_view(request)                    # Login con validación
def register_view(request)                 # Registro con UserRegistrationForm
def logout_custom(request)                 # Logout y redirect
def users_view(request)                    # Lista usuarios (solo staff)
def user_edit(request, pk)                 # Editar usuario (solo staff)
def user_delete(request, pk)               # Eliminar usuario (solo staff)
def profile(request)                       # Perfil con estadísticas semanales
```

#### Vistas de Productos
```python
def inventario(request)                    # Lista productos con paginación
def producto_list(request)                 # Vista tabla productos
def producto_create(request)               # Crear producto con ProductoForm
def producto_detail(request, pk)           # Detalle individual
def producto_update(request, pk)           # Editar producto
def producto_delete(request, pk)           # Eliminar con confirmación
def upload_products_excel(request)         # Carga masiva Excel
```

#### Vistas de Carrito y Ventas
```python
def cart_checkout(request)                 # Procesar venta carrito
def tabla_cart_sales(request)              # Historial ventas
def detalle_cart_sale(request, pk)         # Detalle venta específica
```

#### Vistas de Configuración
```python
@staff_required
def settings_view(request)                 # Panel configuración tipos
def delete_product_type(request, pk)       # Eliminar tipo producto
```

### Sistema de URLs (inventory/urls.py)
```python
urlpatterns = [
    # Dashboard y autenticación
    path('', login_view, name='login'),
    path('index', index, name='index'),
    path('register', register_view, name='register'),
    path('logout/', logout_custom, name='logout_custom'),
    
    # Gestión productos
    path('inventario', inventario, name='inventario'),
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/create/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/edit/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/delete/', views.producto_delete, name='producto_delete'),
    path('productos/upload_excel/', views.upload_products_excel, name='upload_products_excel'),
    
    # Carrito y ventas
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('tabla_cart_sales/', views.tabla_cart_sales, name='tabla_cart_sales'),
    path('cart_sale/<int:pk>/', views.detalle_cart_sale, name='detalle_cart_sale'),
    
    # Proveedores
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    # Configuración y administración
    path('settings/', views.settings_view, name='settings_view'),
    path('product_types/<int:pk>/delete/', views.delete_product_type, name='delete_product_type'),
    path('usuarios', users_view, name='users_view'),
    path('usuarios/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('usuarios/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Historial y reportes
    path('historial', historial, name='historial'),
    path('historial<int:pk>', detalle_historial, name='detalle_historial'),
    path('tabla_historial/', views.tabla_historial, name='tabla_historial'),
    path('user-mov/', user_mov, name='user_mov'),
    path('profile/', profile, name='profile'),
]
```

---

## Lógica de Negocio Específica

### 1. Sistema de Códigos de Boleta Chilenos
```python
def generar_boleta_codigo():
    """Genera código secuencial BOL-00000001"""
    ultimo = HistorialMovimiento.objects.filter(
        boleta_codigo__startswith='BOL-'
    ).order_by('-id').first()
    
    if ultimo and ultimo.boleta_codigo:
        try:
            num = int(ultimo.boleta_codigo.replace('BOL-', ''))
        except Exception:
            num = 0
    else:
        num = 0
    return f"BOL-{num+1:08d}"  # BOL-00000001, BOL-00000002, etc.
```

### 2. Creación de Historial Automático
```python
def crear_historial_venta(**kwargs):
    """Crea HistorialMovimiento para ventas"""
    return HistorialMovimiento.objects.create(**kwargs)
```

### 3. Estadísticas Semanales de Usuario
```python
# En profile_view - Cálculo de recaudación semanal
today = timezone.now().date()
start_week = today - timedelta(days=today.weekday())
end_week = start_week + timedelta(days=7)

# Total global (todos los usuarios)
recaudado_semana_global = Movimiento.objects.filter(
    fecha__gte=start_week,
    fecha__lt=end_week,
    motivo='Venta'
).aggregate(total=Sum('total'))['total'] or 0

# Total del usuario actual
recaudado_semana = Movimiento.objects.filter(
    fecha__gte=start_week,
    fecha__lt=end_week,
    motivo='Venta',
    usuario=request.user
).aggregate(total=Sum('total'))['total'] or 0
```

### 4. Decorador de Permisos Staff
```python
# En inventory/decorators.py
def staff_required(view_func):
    """Decorador que requiere permisos de staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'inv/403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
```
    
@login_required
def inventario(request):
    # Todos los usuarios autenticados
```

#### Proceso de Creación de Usuarios:
1. Solo administradores pueden crear usuarios
2. Contraseña inicial generada automáticamente
3. Usuario debe cambiar contraseña en primer login
4. Validación de unicidad de email

### Módulo de Carrito de Compras

#### Funcionalidades:
1. Gestión Local (localStorage):
   - Agregar/quitar productos
   - Modificar cantidades
   - Persistencia entre sesiones

2. Checkout AJAX:
   ```javascript
   fetch('/cart_checkout/', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
           'X-CSRFToken': getCSRFToken(),
       },
       body: JSON.stringify({
           cart: items, 
           cart_code: cartCode
       })
   })
   ```

3. Procesamiento Backend:
   - Validación de stock disponible
   - Creación de MovimientoStock para cada item
   - Creación de DetalleVenta agrupado por boleta
   - Transacción atómica para consistencia

#### Animaciones y UX:
- Animación "wiggle" al agregar items
- Contador de items en tiempo real
- Panel deslizable responsivo

### Módulo de Dashboard/Reportes

#### Consultas Principales:
```python
# Productos con stock bajo
productos_bajo_stock = Producto.objects.filter(
    stock__lte=F('stock_minimo')
).order_by('stock')

# Productos más vendidos
mas_vendidos = MovimientoStock.objects.filter(
    tipo='venta'
).values('producto__nombre').annotate(
    total_vendido=Sum('cantidad')
).order_by('-total_vendido')[:10]

# Ventas por mes
ventas_mensuales = MovimientoStock.objects.filter(
    tipo='venta',
    fecha__year=current_year
).extra(
    select={'month': 'strftime("%%m", fecha)'}
).values('month').annotate(
    total=Sum('valor_total')
).order_by('month')
```

---

## APIs y Endpoints

### Endpoints Principales

#### Autenticación
- `POST /login/` - Autenticación de usuarios
- `POST /logout/` - Cerrar sesión
- `POST /register/` - Registro de nuevos usuarios (solo admin)

#### Productos
- `GET /inventario/` - Lista de productos con filtros
- `POST /productos/add/` - Crear nuevo producto
- `POST /productos/<id>/edit/` - Editar producto
- `POST /productos/<id>/delete/` - Eliminar producto
- `POST /upload-excel/` - Carga masiva desde Excel

#### Movimientos
- `GET /historial/` - Historial de movimientos
- `GET /user-mov/` - Movimientos del usuario actual
- `POST /productos/<id>/edit/` - Registrar movimiento

#### Carrito
- `POST /cart_checkout/` - Procesar carrito de compras
- `GET /tabla_cart_sales/` - Vista de ventas del carrito
- `GET /tabla_historial/` - Vista de historial normal

#### Proveedores
- `GET /suppliers/` - Lista de proveedores
- `POST /suppliers/add/` - Crear proveedor
- `POST /suppliers/<id>/edit/` - Editar proveedor

#### Reportes
- `GET /` - Dashboard principal con estadísticas
- `GET /detalle_historial/<id>/` - Detalle de movimiento
- `GET /detalle_cart_sale/<codigo>/` - Detalle de venta

### Estructura de Respuestas AJAX

#### Checkout del Carrito:
```json
{
    "success": true,
    "message": "Venta procesada correctamente",
    "movimientos_creados": 5,
    "total_venta": 125000.00
}
```

#### Error de Validación:
```json
{
    "success": false,
    "error": "Stock insuficiente para producto: Vidrio templado 6mm",
    "producto_id": 123
}
```

---

## Frontend y Componentes JavaScript

### Archivo Principal: main.js

#### Funcionalidades Implementadas:

1. Sistema de Tablas Dinámicas:
   ```javascript
   function initializeToggleButton() {
       // Alternar columnas rayadas
       // Persistencia en localStorage
       // Re-aplicación después de actualizaciones AJAX
   }
   ```

2. Filtrado en Tiempo Real:
   ```javascript
   function updateTable() {
       // Inventario
   }
   
   function updateHistorialTable() {
       // Historial con filtros múltiples
   }
   
   function updateUserMovementsTable() {
       // Movimientos del usuario
   }
   ```

3. Carrito de Compras:
   ```javascript
   // Gestión local con localStorage
   function getCart() { /* ... */ }
   function renderCart() { /* ... */ }
   function updateCartCounter() { /* ... */ }
   function triggerCartWiggle() { /* ... */ }
   ```

4. Validaciones Frontend:
   - Validación de RUT chileno
   - Validación de formularios
   - Confirmaciones de eliminación

#### Animaciones CSS:
```css
@keyframes wiggle {
    0% { transform: rotate(0deg); }
    25% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
    75% { transform: rotate(-3deg); }
    100% { transform: rotate(0deg); }
}
```

### Componentes de UI:

1. Panel Deslizable del Carrito:
   - Posición fija con z-index alto
   - Transiciones CSS smooth
   - Gestión de eventos click fuera del panel

2. Contador de Items:
   - Badge circular con conteo en tiempo real
   - Ocultación automática cuando está vacío
   - Límite visual "99+"

3. Sistema de Filtros:
   - Filtros combinados (búsqueda + tipo + usuario + fechas)
   - Validación de rangos de fechas
   - Actualización de URL para bookmarking

---

## Configuración y Despliegue

### Requisitos del Sistema

#### Dependencias Python (requirements.txt):
```
Django>=4.0,<5.0
pandas>=1.3.0
openpyxl>=3.0.0
django-import-export>=2.8.0
gunicorn>=20.1.0
psycopg2-binary>=2.9.0  # Para PostgreSQL
whitenoise>=6.0.0       # Para archivos estáticos
```

#### Versiones:
- Python: 3.7+
- Django: 4.x
- Base de Datos: SQLite3 (dev) / PostgreSQL 12+ (prod)

### Configuración de Desarrollo

1. Clonar repositorio:
   ```bash
   git clone <repository-url>
   cd GestorInventario
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar base de datos:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Ejecutar servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

### Configuración de Producción

#### Variables de Entorno:
```bash
# settings.py configuración
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### Archivo settings.py (Producción):
```python
import os
import dj_database_url

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Base de datos
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Despliegue con Gunicorn:
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar aplicación
gunicorn inventory_management_system.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
```

#### Configuración Nginx (Opcional):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker (Opcional)

#### Dockerfile existente:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "inventory_management_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Mantenimiento y Solución de Problemas

### 1. Problemas Comunes y Soluciones

#### Error: "No module named 'inventory'"
Causa: App no está en INSTALLED_APPS
Solución:
```python
# En settings.py, verificar:
INSTALLED_APPS = [
    # ...
    'inventory',  # Debe estar presente
]
```

#### Error: "table doesn't exist"
Causa: Migraciones pendientes
Solución:
```bash
python manage.py makemigrations inventory
python manage.py migrate
```

#### Error: Validación RUT Frontend vs Backend diferente
Causa: Algoritmos desincronizados
Solución: Verificar que tanto `main.js` como `forms.py` usen el mismo algoritmo

#### Error: Carrito no actualiza contador
Causa: JavaScript no encuentra elementos DOM
Solución: Verificar que `cart_panel.html` esté incluido en `base.html`

#### Error: SVG icons muy pequeños en sidebar
Causa: CSS de tabla afecta íconos globalmente
Solución: Usar selectores específicos para proteger sidebar

### 2. Comandos de Diagnóstico
```bash
# Verificar estructura base de datos
python manage.py dbshell
.tables
.schema inventory_producto

# Verificar migraciones
python manage.py showmigrations

# Verificar usuarios y permisos
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Verificar archivos estáticos
python manage.py findstatic css/style.css

# Limpiar archivos estáticos
python manage.py collectstatic --clear --noinput
```

### 3. Logs y Debugging
```python
# En settings.py para debugging avanzado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'inventory': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### 4. Backup y Restauración
```bash
# Backup base de datos
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Exportar datos específicos
python manage.py dumpdata inventory.Producto > productos_backup.json
python manage.py dumpdata inventory.Suppliers > proveedores_backup.json

# Restaurar datos
python manage.py loaddata productos_backup.json
```

### 5. Optimización Performance
```python
# En views.py, usar select_related para reducir queries
def producto_list(request):
    productos = Producto.objects.select_related('product_type').all()
    
# Paginación para tablas grandes
def historial(request):
    movimientos = HistorialMovimiento.objects.all().order_by('-fecha')
    paginator = Paginator(movimientos, 25)  # 25 por página
```

### 6. Actualización de Dependencias
```bash
# Verificar versiones actuales
pip list --outdated

# Actualizar Django (con cuidado)
pip install Django==5.2.2

# Verificar compatibilidad
python manage.py check --deploy
```

---

## Glosario Técnico

### Términos del Sistema
- ProductType: Modelo para tipos de productos dinámicos (Vidrio, Aluminio, etc.)
- HistorialMovimiento: Registro de auditoría de todos los cambios de stock
- CartSale: Venta realizada a través del carrito
- staff_required: Decorador para vistas que requieren permisos de staff
- boleta_codigo: Código de boleta chileno secuencial (BOL-00000001)

### Términos de Frontend
- wiggle: Animación CSS del ícono carrito
- cart-counter: Badge numérico del carrito
- table-responsive: Clase para tablas adaptativas
- sidebar: Panel lateral de navegación

### Términos de Backend
- clean_rut(): Método de validación RUT en formularios
- generar_boleta_codigo(): Función para códigos secuenciales
- crear_historial_venta(): Función para auditoría de ventas
- profile_view(): Vista con estadísticas de usuario

### Archivos Clave
- `models.py`: 6 modelos principales (123 líneas)
- `views.py`: 30+ vistas (937 líneas)
- `forms.py`: 8 formularios con validaciones (339 líneas)
- `main.js`: JavaScript funcional (carrito, RUT, animaciones)
- `style.css`: CSS personalizado (800+ líneas)
- `base.html`: Template principal con sidebar
- `db.sqlite3`: Base de datos SQLite

---

## Contacto y Soporte

Para soporte técnico, consultar:
- Documentación Django: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Repositorio del proyecto: [GitHub URL]

Última actualización: Enero 2025
Versión del manual: 2.0
Mantenido por: Equipo de desarrollo GestorInventario
