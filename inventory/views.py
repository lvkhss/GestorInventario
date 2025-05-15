from django.shortcuts import render, redirect, get_object_or_404
from django.db import OperationalError
from .models import Laptops, Desktops, Mobiles

# Create your views here.

from .models import *

from .forms import *




def inventario(request):
    return render(request, 'inv/inventario.html')

def index(request):
    try:
        laptops = Laptops.objects.all()
    except OperationalError:
        laptops = []

    try:
        desktops = Desktops.objects.all()
    except OperationalError:
        desktops = []

    try:
        mobiles = Mobiles.objects.all()
    except OperationalError:
        mobiles = []

    items = [
        {"item": laptop, "category": "Laptops"} for laptop in laptops
    ] + [
        {"item": desktop, "category": "Desktops"} for desktop in desktops
    ] + [
        {"item": mobile, "category": "Mobiles"} for mobile in mobiles
    ]

    context = {
        'items': items,
    }
    return render(request, 'inv/index.html', context)

def display_laptops(request):
    try:
        items = Laptops.objects.all()
    except OperationalError:
        items = []  

    context = {
        'items': items,
        'header': 'Laptops',
    }
    return render(request, 'inv/inventario.html', context)


def display_desktops(request):
    items = Desktops.objects.all()
    context = {
        'items': items,
        'header': 'Desktops',
    }
    return render(request, 'inv/inventario.html', context)


def display_mobiles(request):
    items = Mobiles.objects.all()
    context = {
        'items': items,
        'header': 'Mobiles',
    }
    return render(request, 'inv/inventario.html', context)

def add_item(request, cls):
    if request.method == "POST":
        form = cls(request.POST)

        if form.is_valid():
            form.save()
            return redirect('inventario')

    else:
        form = cls()
        return render(request, 'inv/add_new.html', {'form' : form})


def add_laptop(request):
    return add_item(request, LaptopForm)


def add_desktop(request):
    return add_item(request, DesktopForm)


def add_mobile(request):
    return add_item(request, MobileForm)


def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = cls(instance=item)

        return render(request, 'inv/edit_item.html', {'form': form})



def edit_laptop(request, pk):
    return edit_item(request, pk, Laptops, LaptopForm)


def edit_desktop(request, pk):
    return edit_item(request, pk, Desktops, DesktopForm)


def edit_mobile(request, pk):
    return edit_item(request, pk, Mobiles, MobileForm)


def delete_laptop(request, pk):

    template = 'inv/inventario.html'
    Laptops.objects.filter(id=pk).delete()

    items = Laptops.objects.all()

    context = {
        'items': items,
    }

    return render(request, template, context)


def delete_desktop(request, pk):

    template = 'inv/inventario.html'
    Desktops.objects.filter(id=pk).delete()

    items = Desktops.objects.all()

    context = {
        'items': items,
    }

    return render(request, template, context)


def delete_mobile(request, pk):

    template = 'inv/inventario.html'
    Mobiles.objects.filter(id=pk).delete()

    items = Mobiles.objects.all()

    context = {
        'items': items,
    }

    return render(request, template, context)
