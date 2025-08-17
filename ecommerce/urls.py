from django.urls import path
from .views import (
    home, crear_cliente, crear_producto, busqueda, about,
    ClienteListView, ClienteDetailView, ClienteUpdateView, ClienteDeleteView
)

urlpatterns = [
    path('', home, name='home'),
    path('crear_cliente/', crear_cliente, name='crear_cliente'),
    path('clientes/', ClienteListView.as_view(), name='listar_clientes'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/<int:pk>/borrar/', ClienteDeleteView.as_view(), name='borrar_cliente'),
    path('crear-producto/', crear_producto, name='crear_producto'),
    path('busqueda/', busqueda, name='busqueda'),
    path('about/', about, name='about'),
]