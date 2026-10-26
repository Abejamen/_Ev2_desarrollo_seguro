from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from .models import Producto, Categoria


@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/lista.html', {
        'productos': productos,
        'categorias': categorias,
    })


@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'catalogo/detalle.html', {'producto': producto})


@login_required
def buscar(request):
    q = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    precio_max = request.GET.get('precio_max', '')

    sql = "SELECT id, codigo, nombre, precio, stock FROM catalogo_producto WHERE nombre LIKE '%" + q + "%'"
    if categoria:
        sql += " AND categoria_id = " + categoria
    if precio_max:
        sql += " AND precio <= " + precio_max

    with connection.cursor() as cursor:
        cursor.execute(sql)
        filas = cursor.fetchall()

    resultados = [
        {'id': f[0], 'codigo': f[1], 'nombre': f[2], 'precio': f[3], 'stock': f[4]}
        for f in filas
    ]
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/buscar.html', {
        'resultados': resultados,
        'categorias': categorias,
        'q': q,
    })


@login_required
def sugerencias(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=q)[:5]
    return JsonResponse({'sugerencias': [p.nombre for p in productos]})