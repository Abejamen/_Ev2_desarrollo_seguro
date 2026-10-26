from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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