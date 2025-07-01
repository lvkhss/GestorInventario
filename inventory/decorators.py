from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

def staff_required(function):
    """
    Decorador que requiere que el usuario sea staff
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si no está autenticado, redirigir al login
            return redirect('login')
        elif not request.user.is_staff:
            # Si está autenticado pero no es staff, mostrar error 403
            return render(request, 'inv/403.html', status=403)
        else:
            # Si es staff, permitir acceso
            return function(request, *args, **kwargs)
    
    return wrapper