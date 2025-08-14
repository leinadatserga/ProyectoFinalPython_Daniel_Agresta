from .models import UsuarioSistema
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.forms.widgets import ClearableFileInput


class formularioRegistro(UserCreationForm):
    """
    Formulario para el registro de nuevos usuarios en el sistema.
    Incluye validación completa de unicidad para email,
    verificación de contraseñas coincidentes y requisitos mínimos
    de seguridad para contraseñas.
    Features:
        - Contraseñas coincidentes.
        - Longitud mínima de contraseña (6 caracteres).
        - Campos de contraseña con widget PasswordInput.
        - Validación de unicidad antes del guardado.
    """
    class Meta:
        model = UsuarioSistema
        fields = ['username', 'email', 'avatar', 'password1', 'password2']

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        avatar = self.cleaned_data.get("avatar")
        user = UsuarioSistema.objects.create_user(
            username=username,
            email=email,
            password=password,
            avatar=avatar
        )
        return user

    username = forms.CharField(
        label='Nombre de usuario',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario'
        })
    )

    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )

    avatar = forms.ImageField(
        label='Avatar',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Sube tu avatar (opcional)'
        })
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña'
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if UsuarioSistema.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        """
        Valida que el email no esté ya registrado en el sistema.
        Features:
            - Verificación de unicidad en la base de datos.
        """
        email = self.cleaned_data['email']
        if UsuarioSistema.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email


    def clean(self):
        """
        Validación global del formulario de registro.
        Verifica que las contraseñas coincidan y cumplan con los
        requisitos mínimos de seguridad.
        Features:
            - Contraseñas coincidentes.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        if password1 and len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        
        return cleaned_data


class formularioLogin(forms.Form):
    """
    Formulario para autenticación de usuarios existentes.
    Proporciona una interfaz simple y segura para el inicio de sesión
    utilizando email y contraseña. Compatible con el sistema de
    autenticación personalizado del proyecto.
    Features:
        - Campo del email con validación automática de formato.
        - Placeholders informativos para mejorar UX.
        - No almacena ni muestra contraseñas en texto plano.
        - Validación del formato del email antes del envío.
    """
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Credenciales incorrectas.')
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = 'Eliminar avatar'

class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = UsuarioSistema
        fields = ['username', 'email', 'avatar']
        widgets = {
            'avatar': CustomClearableFileInput(attrs={
                'placeholder': 'Sube tu avatar (opcional)'
            })
        }

from django.contrib.auth.forms import PasswordChangeForm

class UsuarioPasswordChangeForm(PasswordChangeForm):
    """
    Formulario para que el usuario cambie su contraseña.
    Hereda de PasswordChangeForm y solo personaliza los widgets.
    """
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'})
    )
    new_password2 = forms.CharField(
        label='Repite contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite nueva contraseña'})
    )