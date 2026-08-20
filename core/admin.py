from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Produto, Categoria, CotacaoBitcoin, Profile # Importe o Profile aqui
from .models import HomeConfig

# 1. Define o Inline para o Profile aparecer dentro do User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Informações Adicionais (Entrega/Contato)'

# 2. Desregistra o User padrão e registra o customizado
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Seus modelos originais permanecem aqui:
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'icone', 'categoria', 'preco_sats', 'exibir_preco_brl', 'is_promo')
    list_editable = ('is_promo', 'categoria')
    search_fields = ('nome', 'sku')
    list_filter = ('is_promo', 'categoria')

    def exibir_preco_brl(self, obj):
        return f"R$ {obj.preco_brl}"
    exibir_preco_brl.short_description = 'Preço Estimado (R$)'

@admin.register(CotacaoBitcoin)
class CotacaoBitcoinAdmin(admin.ModelAdmin):
    list_display = ('preco_brl', 'ultima_atualizacao')
    
    
@admin.register(HomeConfig)
class HomeConfigAdmin(admin.ModelAdmin):
    list_display = ('titulo_hero', 'ativo')    