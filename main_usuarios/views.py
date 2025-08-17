from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from .forms import formularioRegistro, formularioLogin
from .models import UsuarioSistema
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, View
from django.urls import reverse_lazy
from .forms import UsuarioEditForm, UsuarioPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView



class UsuarioPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UsuarioPasswordChangeForm
    template_name = 'usuarios/cambiar_contrasena.html'
    success_url = reverse_lazy('cambiar_contrasena_exito')

    def form_valid(self, form):
        messages.success(self.request, '¡Contraseña cambiada correctamente!')
        return super().form_valid(form)

def debug_session_info(request):
    """
    Función de utilidad para depuración de sesiones.
    Muestra información detallada sobre la sesión actual y el usuario autenticado.
    Solo para desarrollo - no usar en producción.
    """
    if hasattr(request, 'session'):
        session_key = request.session.session_key
        active_sessions = Session.objects.filter(expire_date__gt=timezone.now()).count()

        print(f"=== DEBUG SESIÓN ===")
        print(f"Session Key: {session_key}")
        print(f"User autenticado: {request.user.is_authenticated}")
        print(f"User ID: {request.user.id}")
        print(f"Email: {getattr(request.user, 'email', None)}")
        print(f"Sesiones activas totales: {active_sessions}")
        print(f"==================")


def login_required_custom(view_func):
    """
    Componente (decorador) especializado para requerir login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def registro(request):
    """
    Vista para registro de nuevos usuarios en el sistema.
    Permite a nuevos usuarios crear una cuenta con validación completa.
    Incluye hash seguro de contraseñas y login automático tras registro.
    Features:
        - Validación de email y usuario único.
        - Creación de sesión automática.
        - Contraseñas hasheadas antes del almacenamiento.
        - Validación de campos únicos (email, usuario).
    """
    if request.method == 'POST':
        form = formularioRegistro(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Usuario "{user.email}" creado exitosamente!')
            return redirect('home')
    else:
        form = formularioRegistro()
    
    return render(request, 'commerce/registro.html', {'form': form})


def login_view(request):
    """
    Vista para autenticación de usuarios existentes.
    Maneja el proceso de login con validación de credenciales.
    Features:
        - Autenticación por email y contraseña.
        - Verificación de usuario activo.
        - Creación de sesión segura.
        - Verificación de contraseña hasheada.
        - Control de usuarios activos únicamente.
    """
    if request.method == 'POST':
        form = formularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.email}!')
                return redirect('home')
            else:
                messages.error(request, 'Credenciales incorrectas. Verifique su email y contraseña.')
    else:
        form = formularioLogin()
    
    return render(request, 'commerce/login.html', {'form': form})


def logout_view(request):
    """
    Vista para cerrar sesión de usuarios.
    Limpia completamente la sesión del usuario y muestra mensaje de despedida.
    Features:
        - Mensaje personalizado de despedida.
        - Redirección segura a la página principal.
        - Eliminación completa de datos de sesión.
        - No exposición de información sensible.
    """
    username = request.user.get_username() if request.user.is_authenticated else 'Usuario'

    request.session.flush()
    
    messages.info(request, f'¡Hasta luego {username}! Has cerrado sesión correctamente.')
    return redirect('home')



class UserAdministrationView(LoginRequiredMixin, UpdateView):
    model = UsuarioSistema
    form_class = UsuarioEditForm
    template_name = 'usuarios/administracion_usuarios.html'
    success_url = reverse_lazy('administracion')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente.')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada.')
        return redirect('home')