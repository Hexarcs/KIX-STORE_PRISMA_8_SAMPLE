import decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Categoria(models.Model):
    """Define as categorias da loja."""
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Ex: frescos, mercearia, higiene, limpeza")

    def __str__(self):
        return self.nome


class MacroCategoria(models.Model):
    """Define as macro categorias exibidas na vitrine principal."""
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Macro Categoria"
        verbose_name_plural = "Macro Categorias"
        ordering = ['ordem']

    def __str__(self):
        return self.nome


class CotacaoBitcoin(models.Model):
    """Armazena a última cotação do Bitcoin obtida via API."""
    preco_brl = models.DecimalField(max_digits=12, decimal_places=2)
    ultima_atualizacao = models.DateTimeField()

    def __str__(self):
        return f"BTC: R$ {self.preco_brl} em {self.ultima_atualizacao}"


class Produto(models.Model):
    sku = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="Identificador único para o JS. Ex: prod_cafe_500"
    )
    nome = models.CharField(max_length=255)
    
    # Ligação com a Categoria
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='produtos'
    )

    icone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Insira um Emoji correspondente (ex: ☕, 🥫)",
    )

    preco_sats = models.IntegerField(verbose_name="Preço em Satoshis (Sats)")

    imagem = models.ImageField(
        upload_to="produtos/",
        blank=True,
        null=True,
        verbose_name="Foto do Produto (Quadrada)",
    )

    is_promo = models.BooleanField(
        default=False, verbose_name="Exibir em Ofertas Rápidas (Máx 4)"
    )

    def __str__(self):
        return self.nome

    @property
    def preco_brl(self):
        ultima_cotacao = CotacaoBitcoin.objects.last()
        if ultima_cotacao and ultima_cotacao.preco_brl > 0:
            valor_sat_em_brl = ultima_cotacao.preco_brl / decimal.Decimal("100000000")
            preco_calculado = decimal.Decimal(self.preco_sats) * valor_sat_em_brl
        else:
            fallback_sat_em_brl = decimal.Decimal("0.005")
            preco_calculado = decimal.Decimal(self.preco_sats) * fallback_sat_em_brl

        return preco_calculado.quantize(decimal.Decimal("0.01"))

    @property
    def preco_pix_estatal(self):
        valor_inflacionado = self.preco_brl * decimal.Decimal("1.1")
        return valor_inflacionado.quantize(decimal.Decimal("0.01"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    endereco = models.TextField(verbose_name="Endereço Completo", blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


# =========================================================================
# SIGNALS: Garante a existência do Profile de forma segura contra falhas
# =========================================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria o Profile automaticamente ao registrar um novo User."""
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Garante que o perfil exista e seja salvo ao atualizar o User."""
    profile, _ = Profile.objects.get_or_create(user=instance)
    profile.save()
    
    
# =========================================================================
# CONFIGURAÇÃO DO HERO (HOME)
# =========================================================================    

class HomeConfig(models.Model):
    titulo_hero = models.CharField(max_length=200, default="Bem-vindo ao Supermercado Kix", verbose_name="Título do Hero")
    subtitulo_hero = models.TextField(blank=True, null=True, verbose_name="Subtítulo do Hero")
    imagem_hero = models.ImageField(upload_to='hero/', verbose_name="Imagem do Hero")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Configuração do Hero (Home)"
        verbose_name_plural = "Configurações do Hero (Home)"

    def __str__(self):
        return "Banner Hero da Home"

#==============================bagde e nome do site===================

#from django.db import models

class SiteConfig(models.Model):
    nome_loja = models.CharField(max_length=100, default="Supermercado Itatingax")
    badge_ecossistema = models.CharField(max_length=100, default="Membro do Ecossistema KIX")

    def save(self, *args, **kwargs):
        # Garante que sempre haverá apenas uma linha de configuração (Singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configurações do Site"        