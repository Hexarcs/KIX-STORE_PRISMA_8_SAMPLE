from .models import CotacaoBitcoin
from .models import SiteConfig

def btc_context(request):
    """Injeta a última cotação do Bitcoin globalmente em todos os templates"""
    registro_cotacao = CotacaoBitcoin.objects.last()
    return {
        'btc_preco': registro_cotacao.preco_brl if registro_cotacao else 0
    }
    


def site_config_processor(request):
    return {
        'site_config': SiteConfig.get_solo()
    }    