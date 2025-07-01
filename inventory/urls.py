from django.urls import path, re_path
from .views import *
from . import views 


urlpatterns = [
    path('index', index, name='index'),
    path('historial<int:pk>', detalle_historial, name='detalle_historial'),
    path('settings/', views.settings_view, name='settings_view'),
    path('product_types/<int:pk>/delete/', views.delete_product_type, name='delete_product_type'),

    path('inventario', inventario, name='inventario'),
    path('', login_view, name='login'),
    path('register', register_view, name='register'),
    path('usuarios', users_view, name='users_view'),
    path('usuarios/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('usuarios/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('historial', historial, name='historial'),
    path('profile/', profile, name='profile'),
    path('user-mov/', user_mov, name='user_mov'),

    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    path('productos/', views.producto_list, name='producto_list'),
    path('productos/create/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/edit/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/delete/', views.producto_delete, name='producto_delete'),
    path('productos/upload_excel/', views.upload_products_excel, name='upload_products_excel'),

    path('logout/', logout_custom, name='logout_custom'),
]