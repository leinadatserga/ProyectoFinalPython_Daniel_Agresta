from django import forms

class formularioCliente(forms.Form):
    """
    Formulario para la creación de nuevos clientes en el sistema.
    Incluye validación de campos obligatorios y formateo de entrada.
    Features:
        - Validación automática de formato de email.
        - Límites de edad realistas.
        - Placeholders informativos para UX.
    """
    name = forms.CharField(
        max_length=100,
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre completo del cliente'
        })
    )
    
    age = forms.IntegerField(
        label='Edad',
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ingrese la edad'
        })
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )


class formularioProductos(forms.Form):
    """
    Formulario para la creación y edición de productos en el catálogo.
    Permite definir todos los aspectos de un producto incluyendo precio,
    stock y estado de visibilidad. Incluye validaciones para datos críticos
    como precios negativos y límites de stock.
    Features:
        - Validación de precios no negativos.
        - Campo de descripción opcional con textarea.
        - Control de stock con validación mínima.
        - Estado activo por defecto para nuevos productos.
    """
    nombre = forms.CharField(
        max_length=200,
        label='Nombre del producto',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre del producto'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label='Precio',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ingrese el precio (en USD)',
            'step': '0.01'
        })
    )
    
    descripcion = forms.CharField(
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={
            'placeholder': 'Descripción del producto',
            'rows': 4
        })
    )
    
    stock = forms.IntegerField(
        min_value=0,
        initial=0,
        label='Stock disponible',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Cantidad en stock'
        })
    )
    
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label='Producto activo',
        widget=forms.CheckboxInput()
    )





