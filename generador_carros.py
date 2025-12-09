from random import random 
from parametros import *
from carro import Carro

# --- NUEVO: helpers para elegir probabilidades según tamaño/origen ---
def _prob_keys_por_origen(salida):
    """
    Devuelve las claves (izquierda, recto, derecha) con el convenio del simulador.
    """
    if salida == "Norte":  # izq=W, recto=S, der=E
        return ("N_W_probabilidad", "N_S_probabilidad", "N_E_probabilidad")
    if salida == "Sur":    # izq=E, recto=N, der=W
        return ("S_E_probabilidad", "S_N_probabilidad", "S_W_probabilidad")
    if salida == "Este":   # izq=N, recto=W, der=S
        return ("E_N_probabilidad", "E_W_probabilidad", "E_S_probabilidad")
    if salida == "Oeste":  # izq=S, recto=E, der=N
        return ("W_S_probabilidad", "W_E_probabilidad", "W_N_probabilidad")
    raise ValueError(f"Salida desconocida: {salida}")

def _get_probs(salida, es_grande):
    """
    Intenta usar *_peq / *_gran según tamaño. Si no existen, cae a las variables sin sufijo.
    Retorna tupla (p_izq, p_recto, p_der) que suman ≈ 1.
    """
    base_izq, base_recto, base_der = _prob_keys_por_origen(salida)

    # Construye nombres por tipo
    suf = "_gran" if es_grande else "_peq"
    izq_t = base_izq + suf
    recto_t = base_recto + suf
    der_t = base_der + suf

    # Disponibles en parametros.py si USAR_PROB_POR_TIPO=True
    p_izq  = globals().get(izq_t)
    p_rect = globals().get(recto_t)
    p_der  = globals().get(der_t)

    if p_izq is None or p_rect is None or p_der is None:
        # Fallback a las mezcladas (sin sufijo)
        p_izq  = globals()[base_izq]
        p_rect = globals()[base_recto]
        p_der  = globals()[base_der]

    # Seguridad: normaliza suavemente si hay pequeñas desviaciones numéricas
    s = p_izq + p_rect + p_der
    if s > 0:
        p_izq, p_rect, p_der = p_izq/s, p_rect/s, p_der/s
    return p_izq, p_rect, p_der

def generar_carro(salida):
    # Crea un carro con dirección, velocidad y tamaño
    """
    Valores posibles de la variable destino
    [0,1]  	Sur
    [0,-1] 	Norte
    [1,0] 	Este
    [-1,0] 	Oeste
    """
    rn = random()
    destino = [None, None]

    if salida=="Norte":  # el carro entra por el norte y apunta hacia el sur
        x = int(tamano_mapa["x"]/2)
        y = 0
        v_x = 0
        v_y = round(rapidez_max*random())
        d_x = 0
        d_y = 1
        # tamaño primero, para elegir la terna por tipo
        es_grande = (random() < p_car_grande)
        p_izq, p_rect, p_der = _get_probs(salida, es_grande)  # izq=W, rect=S, der=E

        # muestreo direccional con tu mismo esquema de umbrales
        if rn < p_der:
            destino = [1,0]      # Este
        elif rn < p_der + p_izq:
            destino = [-1,0]     # Oeste
        else:
            destino = [0,1]      # Sur

    elif salida=="Sur":
        x = int(tamano_mapa["x"]/2+1)
        y = tamano_mapa["y"]-1
        v_x = 0
        v_y = -round(rapidez_max*random())
        d_x = 0
        d_y = -1
        es_grande = (random() < p_car_grande)
        p_izq, p_rect, p_der = _get_probs(salida, es_grande)  # izq=E, rect=N, der=W
        if rn < p_izq:
            destino = [1,0]      # Este
        elif rn < p_izq + p_der:
            destino = [-1,0]     # Oeste
        else:
            destino = [0,-1]     # Norte

    elif salida=="Oeste":
        x = 0
        y = int(tamano_mapa["y"]/2+1)
        v_x = round(rapidez_max*random())
        v_y = 0
        d_x = 1
        d_y = 0
        es_grande = (random() < p_car_grande)
        p_izq, p_rect, p_der = _get_probs(salida, es_grande)  # izq=S, rect=E, der=N
        if rn < p_der:
            destino = [0,-1]     # Norte
        elif rn < p_der + p_izq:
            destino = [0,1]      # Sur
        else:
            destino = [1,0]      # Este

    elif salida=="Este":
        x = int(tamano_mapa["x"])-1
        y = int(tamano_mapa["y"]/2)
        v_x = -round(rapidez_max*random())
        v_y = 0
        d_x = -1
        d_y = 0
        es_grande = (random() < p_car_grande)
        p_izq, p_rect, p_der = _get_probs(salida, es_grande)  # izq=N, rect=W, der=S
        if rn < p_izq:
            destino = [0,-1]     # Norte
        elif rn < p_izq + p_der:
            destino = [0,1]      # Sur
        else:
            destino = [-1,0]     # Oeste

    else:
        raise ValueError(f"Salida desconocida: {salida}")

    # tamaño ya decidido arriba (es_grande)
    tamano = tamano_car_grande if es_grande else 1

    carro = Carro([x,y],[v_x,v_y],tamano,destino,[d_x,d_y],tamano_mapa)
    return carro
