from core.mmlog import get_logger

log = get_logger('__name__')

def convert_to_bytes(valor_con_unidad):
    valor, unidad = valor_con_unidad[:-2], valor_con_unidad[-2:].lower()
    
    try:
        valor = float(valor)
    except ValueError as e:
        log.error('An error occurred converting to bytes %s: %s',valor_con_unidad, str(e))
        raise ValueError("Valor no válido para la memoria.")

    if unidad == 'gi':
        return int(valor * (1024 ** 3))
    elif unidad == 'mi':
        return int(valor * (1024 ** 2))
    else:
        log.error('Invalid unit, Gi or Mi should be used')
        raise ValueError("Unidad no válida. Utiliza 'Gi' para gigabytes o 'Mi' para megabytes.")
    
