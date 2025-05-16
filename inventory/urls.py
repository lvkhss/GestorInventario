from django.urls import re_path
from .views import * 


urlpatterns = [
    re_path(r'index$', index, name='index'),
    re_path(r'^laptops$', display_laptops, name="display_laptops"),
    re_path(r'^desktops$', display_desktops, name="display_desktops"),
    re_path(r'^mobiles$', display_mobiles, name="display_mobiles"),

    re_path(r'^add_laptop$', add_laptop, name="add_laptop"),
    re_path(r'^add_desktop$', add_desktop, name="add_desktop"),
    re_path(r'^add_mobile$', add_mobile, name="add_mobile"),

    re_path(r'^laptops/edit_item/(?P<pk>\d+)$', edit_laptop, name="edit_laptop"),
    re_path(r'^desktops/edit_item/(?P<pk>\d+)$', edit_desktop, name="edit_desktop"),
    re_path(r'^mobiles/edit_item/(?P<pk>\d+)$', edit_mobile, name="edit_mobile"),

    re_path(r'^laptops/delete/(?P<pk>\d+)$', delete_laptop, name="delete_laptop"),
    re_path(r'^desktops/delete/(?P<pk>\d+)$', delete_desktop, name="delete_desktop"),
    re_path(r'^mobiles/delete/(?P<pk>\d+)$', delete_mobile, name="delete_mobile"),
    re_path(r'^inventario$', inventario, name='inventario'),
    re_path(r'^$', login_view, name='login'),
    re_path(r'^register$', register_view, name='register'),
    re_path(r'^usuarios$', users_view, name='users'),
]