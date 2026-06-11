

_CUPONS = {
    "ALEXANDRIA10": 0.10,
    "LEITOR15": 0.15,
    "BLACKFRIDAY": 0.25,
}


def percentual_do_cupom(codigo):
    """Retorna o percentual (0..1) do cupom ou None se invalido."""
    if not codigo:
        return None
    return _CUPONS.get(codigo.strip().upper())
