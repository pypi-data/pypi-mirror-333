
from functools import cache
@cache
def levenstein(cadenaOrigen :str , cadenaDestino : str) -> int:
    """
    Explicación del algoritmo: https://es.wikipedia.org/wiki/Distancia_de_Levenshtein
    """
    if cadenaOrigen == cadenaDestino: return 0 
    if len(cadenaOrigen) == 0 : return len(cadenaDestino)
    if len(cadenaDestino) == 0 : return len(cadenaOrigen)
    if cadenaOrigen[-1] == cadenaDestino[-1]:
        return levenstein(cadenaOrigen[:-1], cadenaDestino[:-1])       # ignorar
    return min\
    (
        levenstein(cadenaOrigen[:-1], cadenaDestino)        + 2,       # sacar caracter
        levenstein(cadenaOrigen, cadenaDestino[:-1])        + 2,       # agregar caracter
        levenstein(cadenaOrigen[:-1], cadenaDestino[:-1])   + 1        # reemplazar caracter
    )
