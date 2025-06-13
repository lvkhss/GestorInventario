from django.urls import re_path
from .views import * 


urlpatterns = [
    re_path(r'^agregar$', agregar_producto, name='agregar_producto'),

    re_path(r'index$', index, name='index'),


    re_path(r'^sellantes/edit_item/(?P<pk>\d+)$', edit_sellante, name="edit_sellante"),
    re_path(r'^herramientas/edit_item/(?P<pk>\d+)$', edit_herramienta, name="edit_herramienta"),
    re_path(r'^pinturas/edit_item/(?P<pk>\d+)$', edit_pintura, name="edit_pintura"),

    re_path(r'^sellantes/delete/(?P<pk>\d+)$', delete_sellante, name="delete_sellante"),
    re_path(r'^herramientas/delete/(?P<pk>\d+)$', delete_herramienta, name="delete_herramienta"),
    re_path(r'^pinturas/delete/(?P<pk>\d+)$', delete_pintura, name="delete_pintura"),

    re_path(r'^inventario$', inventario, name='inventario'),
    re_path(r'^$', login_view, name='login'),
    re_path(r'^register$', register_view, name='register'),
    re_path(r'^usuarios$', users_view, name='users'),
    re_path(r'^historial$', historial, name='historial'),

]