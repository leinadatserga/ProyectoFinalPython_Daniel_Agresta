from django.db import models
from django.core.validators import MinValueValidator





class Cliente(models.Model):
    """
    Modelo para gestionar clientes del sistema e-commerce.
    Incluye funcionalidad para determinar estatus VIP basado en edad.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre")
    age = models.PositiveIntegerField(verbose_name="Edad")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']

    def mostrar_datos_cliente(self):
        return f"nombre: {self.name}, edad: {self.age}, correo: {self.email}"
    
    def actualizar_email(self, new_email):
        self.email = new_email
        self.save()
        return f"Correo actualizado correctamente a: {self.email}"
    
    def cliente_vip(self):
        if self.age > 40:
            return f"{self.name} es un cliente VIP."
        else:
            return f"{self.name} aún no es cliente VIP."
        
    def __str__(self):
        return f"{self.name}, es un nuevo cliente."


class Producto(models.Model):
    """
    Modelo para gestionar productos en el catálogo e-commerce.
    Incluye control de stock, precios y estado activo/inactivo.
    """
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Precio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    activo = models.BooleanField(default=True, verbose_name="Producto activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


