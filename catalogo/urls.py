from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.lista_productos, name='catalogo'),
    path('catalogo/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('buscar/', views.buscar, name='buscar'),
    path('sugerencias/', views.sugerencias, name='sugerencias'),
]