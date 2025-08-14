from django.urls import path
from .views import home, crear_cliente, crear_producto, busqueda, about

urlpatterns = [
    path('', home, name='home'),
    path('crear_cliente/', crear_cliente, name='crear_cliente'),
    path('crear-producto/', crear_producto, name='crear_producto'),
    path('busqueda/', busqueda, name='busqueda'),
    path('about/', about, name='about'),
]