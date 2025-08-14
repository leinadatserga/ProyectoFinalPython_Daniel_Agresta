from django.contrib import admin
from .models import UsuarioSistema






@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avatar', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email', 'created_at', 'username')
    readonly_fields = ('created_at', 'is_active')
    ordering = ('-created_at',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" style="height:40px; border-radius:4px;" />'
        return "-"
    avatar_preview.allow_tags = True
    avatar_preview.short_description = "Avatar"
    
    fieldsets = (
        ('Información básica', {
            'fields': ('username', 'email', 'avatar', 'is_active')
        }),
        ('Seguridad', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
