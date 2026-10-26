from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cliente


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rut = request.POST.get('rut')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        user = User.objects.create_user(username=username, email=email, password=password)
        Cliente.objects.create(user=user, rut=rut, telefono=telefono, direccion=direccion)
        return redirect('login')
    return render(request, 'clientes/registro.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('inicio')
        error = 'Usuario o contraseña incorrectos'
    return render(request, 'clientes/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def inicio(request):
    cliente = Cliente.objects.filter(user=request.user).first()
    return render(request, 'clientes/inicio.html', {'cliente': cliente})