from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from .models import Cliente


def registro(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        rut = request.POST.get('rut', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()

        # 1. Validación de campos obligatorios
        if not all([username, email, password, rut, telefono, direccion]):
            error = 'Todos los campos son obligatorios.'
            return render(request, 'clientes/registro.html', {'error': error})

        # 2. Validación previa de unicidad 
        if User.objects.filter(username__iexact=username).exists():
            error = 'El nombre de usuario ya está registrado.'
            return render(request, 'clientes/registro.html', {'error': error})

        if User.objects.filter(email__iexact=email).exists():
            error = 'El correo electrónico ya está en uso.'
            return render(request, 'clientes/registro.html', {'error': error})

        if Cliente.objects.filter(rut=rut).exists():
            error = 'El RUT ya se encuentra registrado.'
            return render(request, 'clientes/registro.html', {'error': error})

        # 3. Validación de política de contraseñas (AUTH_PASSWORD_VALIDATORS)
        try:
            validate_password(password)
        except ValidationError as e:
            error = ' '.join(e.messages)
            return render(request, 'clientes/registro.html', {'error': error})

        # 4.si falla Cliente, se revierte User
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                Cliente.objects.create(
                    user=user,
                    rut=rut,
                    telefono=telefono,
                    direccion=direccion
                )
            return redirect('login')
        except IntegrityError:
            error = 'No se pudo completar el registro debido a datos duplicados.'
            return render(request, 'clientes/registro.html', {'error': error})

    return render(request, 'clientes/registro.html', {'error': error})


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
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