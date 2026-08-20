from .models import CotacaoBitcoin

def btc_context(request):
    """Injeta a última cotação do Bitcoin globalmente em todos os templates"""
    registro_cotacao = CotacaoBitcoin.objects.last()
    return {
        'btc_preco': registro_cotacao.preco_brl if registro_cotacao else 0
    }