

_CUPONS = {
    "ALEXANDRIA10": 0.10,
    "LEITOR15": 0.15,
    "BLACKFRIDAY": 0.25,
}


def percentual_do_cupom(codigo):
    
    if not codigo:
        return None
    return _CUPONS.get(codigo.strip().upper())
