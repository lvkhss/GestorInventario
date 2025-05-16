from django.shortcuts import render, redirect, get_object_or_404
from django.db import OperationalError
from .models import Sellantes, Herramientas, Pinturas
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import *

from .forms import *

from django.contrib.auth.models import User
from django.contrib.auth import login



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
    return render(request, 'inv/index.html', context)

def display_herramientas(request):
    try:
        items = Herramientas.objects.all()
    except OperationalError:
        items = []  

    context = {
        'items': items,
        'header': 'Herramientas',
    }
    return render(request, 'inv/inventario.html', context)

def display_sellantes(request):
    items = Sellantes.objects.all()
    context = {
        'items': items,
        'header': 'Sellantes',
    }
    return render(request, 'inv/inventario.html', context)

def display_pinturas(request):
    items = Pinturas.objects.all()
    context = {
        'items': items,
        'header': 'Pinturas',
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
    return render(request, 'inv/add_new.html', {'form': form})

def add_herramienta(request):
    return add_item(request, HerramientaForm)

def add_sellante(request):
    return add_item(request, SellanteForm)

def add_pintura(request):
    return add_item(request, PinturaForm)

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

def edit_herramienta(request, pk):
    return edit_item(request, pk, Herramientas, HerramientaForm)

def edit_sellante(request, pk):
    return edit_item(request, pk, Sellantes, SellanteForm)

def edit_pintura(request, pk):
    return edit_item(request, pk, Pinturas, PinturaForm)

def delete_herramienta(request, pk):
    template = 'inv/inventario.html'
    Herramientas.objects.filter(id=pk).delete()
    items = Herramientas.objects.all()
    context = {'items': items}
    return render(request, template, context)

def delete_sellante(request, pk):
    template = 'inv/inventario.html'
    Sellantes.objects.filter(id=pk).delete()
    items = Sellantes.objects.all()
    context = {'items': items}
    return render(request, template, context)

def delete_pintura(request, pk):
    template = 'inv/inventario.html'
    Pinturas.objects.filter(id=pk).delete()
    items = Pinturas.objects.all()
    context = {'items': items}
    return render(request, template, context)