from django.urls import path
from .views import registro, login_view, logout_view, UserAdministrationView, UserDeleteView, UsuarioPasswordChangeView
from django.shortcuts import render




urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('administracion/', UserAdministrationView.as_view(), name='administracion'),
    path('eliminar/', UserDeleteView.as_view(), name='eliminar_usuario'),
    path('cambiar-contrasena/', UsuarioPasswordChangeView.as_view(), name='cambiar_contrasena'),
    path('cambiar-contrasena/exito/', lambda request: render(request, 'usuarios/cambiar_contrasena_exito.html'), name='cambiar_contrasena_exito'),
]