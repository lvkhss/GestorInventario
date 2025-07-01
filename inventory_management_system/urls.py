"""inventory_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory import views
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs principales
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_custom, name='logout_custom'),
    
    # Inventario y productos
    path('inventario/', views.inventario, name='inventario'),
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/create/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/edit/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/delete/', views.producto_delete, name='producto_delete'),
    path('productos/upload_excel/', views.upload_products_excel, name='upload_products_excel'),
    
    # Proveedores
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    # Historial
    path('historial/', views.historial, name='historial'),
    path('historial/<int:pk>/', views.detalle_historial, name='detalle_historial'),
    
    # Administración (solo staff)
    path('register/', views.register_view, name='register'),
    path('usuarios/', views.users_view, name='users_view'),
    path('usuarios/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('usuarios/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('settings/', views.settings_view, name='settings_view'),
    path('product_types/<int:pk>/delete/', views.delete_product_type, name='delete_product_type'),
    
    # Error pages
    path('403/', views.permission_denied_view, name='permission_denied'),
    
    # Perfil de usuario
    path('profile/', views.profile, name='profile'),
    path('user-mov/', views.user_mov, name='user_mov'),
    path('user-mov/<int:pk>/', views.detalle_user_mov, name='detalle_user_mov'),
]

# Servir archivos estáticos en modo DEBUG=False para desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'inventory/static'))
