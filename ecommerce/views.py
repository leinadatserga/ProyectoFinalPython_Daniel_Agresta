from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import formularioCliente, formularioProductos
from .models import Cliente, Producto
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin




def home(request):
    """
    Vista principal del sistema e-commerce.
    Renderiza la página de inicio con información general del sistema.
    No requiere autenticación.
    """
    return render(request, 'commerce/home.html')

@login_required
def crear_cliente(request):
    """
    Vista para crear nuevos clientes en el sistema.
    Muestra el formulario de creación de clientes con validación.
    Requiere autenticación.
    Features:
        - Validación de email único.
        - Detección automática de clientes VIP.
        - Mensajes informativos de estado.
        - Manejo de errores de duplicación.
    """
    if request.method == 'POST':
        form = formularioCliente(request.POST)
        if form.is_valid():
            # Extraer datos del formulario.
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            
            try:
                # Crear el cliente en la base de datos.
                cliente = Cliente.objects.create(
                    name=name,
                    age=age,
                    email=email
                )
                
                messages.success(request, f'Cliente "{name}" creado exitosamente!')
                
                # Información sobre quién lo creó.
                messages.info(request, f'Cliente registrado por: {request.user.username}')
                
                # Verificar si es VIP y mostrar mensaje adicional.
                if age > 40:
                    messages.info(request, f'¡{name} es un cliente VIP por ser mayor de 40 años!')
                
                # Redirigir para limpiar el formulario.
                return redirect('crear_cliente')
                
            except Exception as e:
                # Manejar errores.
                messages.error(request, 'Error al crear el cliente. Verifique que el email no esté duplicado.')
    else:
        form = formularioCliente()
    
    return render(request, 'commerce/crear_cliente.html', {'form': form})

@login_required
def crear_producto(request):
    """
    Vista para crear nuevos productos en el catálogo.
    Presenta el formulario de creación de productos con validación completa.
    Requiere autenticación.
    Features:
        - Validación de campos obligatorios y formato.
        - Control de stock y precios.
        - Estado activo/inactivo para visibilidad.
        - Mensajes informativos según el estado.
    """
    if request.method == 'POST':
        form = formularioProductos(request.POST)
        if form.is_valid():
            # Extraer los datos del formulario.
            nombre = form.cleaned_data['nombre']
            precio = form.cleaned_data['precio']
            descripcion = form.cleaned_data['descripcion']
            stock = form.cleaned_data['stock']
            activo = form.cleaned_data['activo']
            
            try:
                # Crear el producto en la base de datos.
                producto = Producto.objects.create(
                    nombre=nombre,
                    precio=precio,
                    descripcion=descripcion,
                    stock=stock,
                    activo=activo
                )
                
                messages.success(request, f'Producto "{nombre}" creado exitosamente!')
                
                # Información sobre quién lo creó.
                messages.info(request, f'Producto registrado por: {request.user.username}')
                
                # Mensaje adicional según el estado.
                if activo:
                    messages.info(request, f'El producto está activo y disponible.')
                else:
                    messages.warning(request, f'El producto está inactivo y no será visible.')
                
                # Redirección para limpiar el formulario.
                return redirect('crear_producto')
                
            except Exception as e:
                # Manejo de errores.
                messages.error(request, 'Error al crear el producto. Verifique los datos ingresados.')
    else:
        form = formularioProductos()
    
    return render(request, 'commerce/crear_producto.html', {'form': form})





@login_required
def busqueda(request):
    """
    Vista para búsqueda avanzada de clientes y productos.
    Permite búsqueda flexible por texto libre con filtros por tipo.
    Utiliza Django Q objects para búsquedas complejas e insensibles a mayúsculas.
    Features:
        - Clientes: búsqueda por nombre y email.
        - Productos: búsqueda por nombre y descripción.
        - Búsqueda insensible a mayúsculas/minúsculas.
        - Estadísticas de resultados en tiempo real.
    """
    query = request.GET.get('q', '').strip()
    tipo_busqueda = request.GET.get('tipo', 'todos')
    
    clientes = []
    productos = []
    
    if query:
        if tipo_busqueda == 'clientes' or tipo_busqueda == 'todos':
            # Buscar en clientes por nombre o email.
            clientes = Cliente.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query)
            ).order_by('name')
        
        if tipo_busqueda == 'productos' or tipo_busqueda == 'todos':
            # Buscar en productos por nombre o descripción.
            productos = Producto.objects.filter(
                Q(nombre__icontains=query) | 
                Q(descripcion__icontains=query)
            ).order_by('nombre')
        
        # Mensajes informativos.
        total_resultados = len(clientes) + len(productos)
        if total_resultados > 0:
            messages.success(request, f'Se encontraron {total_resultados} resultado(s) para "{query}"')
        else:
            messages.warning(request, f'No se encontraron resultados para "{query}"')
    
    context = {
        'query': query,
        'tipo_busqueda': tipo_busqueda,
        'clientes': clientes,
        'productos': productos,
        'total_clientes': len(clientes),
        'total_productos': len(productos),
    }
    
    return render(request, 'commerce/busqueda.html', context)

def about(request):
    return render(request, 'commerce/about.html')


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'commerce/listar_clientes.html'
    context_object_name = 'clientes'

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'commerce/detalle_cliente.html'
    context_object_name = 'cliente'

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['name', 'age', 'email']
    template_name = 'commerce/editar_cliente.html'
    success_url = reverse_lazy('listar_clientes')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'commerce/borrar_cliente.html'
    success_url = reverse_lazy('listar_clientes')