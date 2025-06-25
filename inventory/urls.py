from django.urls import path, re_path
from .views import *
from . import views 


urlpatterns = [
    re_path(r'index$', index, name='index'),
    re_path(r'historial(?P<pk>\d+)$', detalle_historial, name='detalle_historial'),
    
    re_path(r'^inventario$', inventario, name='inventario'),
    re_path(r'^$', login_view, name='login'),
    re_path(r'^register$', register_view, name='register'),
    re_path(r'^usuarios$', users_view, name='users'),
    re_path(r'^historial$', historial, name='historial'),
    re_path(r'^suppliers/?$', views.suppliers_list, name='suppliers_list'),
    re_path(r'^suppliers/create/?$', views.supplier_create, name='supplier_create'),
    re_path(r'^suppliers/(?P<pk>\d+)/edit/?$', views.supplier_update, name='supplier_update'),
    re_path(r'^suppliers/(?P<pk>\d+)/delete/?$', views.supplier_delete, name='supplier_delete'),

    
    re_path(r'^productos/?$', views.producto_list, name='producto_list'),
    re_path(r'^productos/create/?$', views.producto_create, name='producto_create'),
    re_path(r'^productos/(?P<pk>\d+)/?$', views.producto_detail, name='producto_detail'),
    re_path(r'^productos/(?P<pk>\d+)/edit/?$', views.producto_update, name='producto_update'),
    re_path(r'^productos/(?P<pk>\d+)/delete/?$', views.producto_delete, name='producto_delete'),
    re_path(r'^productos/upload_excel/?$', views.upload_products_excel, name='upload_products_excel'),
    re_path(r'^logout/$', logout_custom, name='logout_custom'),    

]