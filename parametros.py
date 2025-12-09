tamano_mapa = {"x":200, "y":200}
pasos = 500
rapidez_simulacion = 80  # en milisegundos
medida_de_una_celda = 2 # metros
"""
N_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el norte
S_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el sur
W_densidad = 0.3  		#probabilidad de la cantidad de carros que salen desde el oeste
E_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el Este

N_E_probabilidad = 0.2   # Probabilidad que un carro que salga del norte se dirija al este
N_W_probabilidad = 0.2   #  Probabilidad que un carro que salga del norte se dirija al oeste
S_E_probabilidad = 0.2   #  Probabilidad que un carro que salga del sur se dirija al este
S_W_probabilidad = 0.2   #  Probabilidad que un carro que salga del norte se dirija al oeste
E_N_probabilidad = 0.2   #  Probabilidad que un carro que salga del este se dirija al norte
E_S_probabilidad = 0.2   #  Probabilidad que un carro que salga del este se dirija al sur
W_N_probabilidad = 0.2   # Probabilidad que un carro que salga del oeste se dirija al norte
W_S_probabilidad = 0.2   #  Probabilidad que un carro que salga del oeste se dirija al sur

N_S_probabilidad = 1-N_E_probabilidad-N_W_probabilidad
S_N_probabilidad = 1-S_E_probabilidad-S_W_probabilidad
E_W_probabilidad = 1-E_S_probabilidad-E_N_probabilidad
W_E_probabilidad = 1- W_N_probabilidad-W_S_probabilidad
"""

tiempo_verde = 60  #20       # Este es el numero de fotogramas que se desea que el semaforo esté en verde
tiempo_amarillo = 4   #3   # numero de fotogramas que se desea que el semaforo este en amarillo 

# la variable modo_semaforos puede tomar dos valores  los cuales son 
# "dos_verde" y "uno_verde" 
# en la opcion dos_verde dos semaforos estaran en verde que era la configuracion del programa de la tesis que se tenia inicialmente
# en la opcion uno_verde solo un semaforo estará en verde y el resto en rojo claramente tiene que irse el semaforo 
# que está en verde seria bueno si algo comentar que apesar de que el flujo es mas bajo en la opcion dos uno verde
# esta opcion no produce atascos y por ello tambien menos posibles accidentes
#modo_semaforos = "dos_verde"  
modo_semaforos = "uno_verde"

p_car_grande = 0.4  # Esta es la probabilidad que un carro cuando se crea sea grande
rapidez_max = 5    # esta es la rapidez maxima que se les permite a los carros
probabilidad_frenar = 0.2  # esta es la probabilidad de frenar en un istante

tamano_car_grande = 2     #esto no se debe cambiar  


# =======================
# Autocarga de probabilidades y densidades desde CSV
# (migrado de run_probabilidades.py)
# =======================

# Configuración (ajusta a tu entorno)
HABILITAR_INFERENCIA = True         # Desactívalo si quieres ignorar el CSV
USAR_PROB_POR_TIPO = True           # True => genera *_peq / *_gran además de mezclas sin sufijo
T_CICLO_REAL = 60                   # segundos de ciclo real (verde) observados en el conteo
RUTA_CSV_CONTEO = r"C:\Users\BARANDICA\Desktop\traffic_simulator\insumos\conteo_ciclos.csv"

# Contenedores para exponer también los diccionarios crudos
PROB_GIRO = {}      # dict completo tal como lo entrega inferencia_probabilidades (claves *_peq/_gran si aplica)
DENSIDADES = {}     # {'N_densidad': x, 'S_densidad': y, 'E_densidad': z, 'W_densidad': w}

def _mezcla(peq, gra, p_gran):
    """Mezcla por tamaño para obtener la versión 'sin sufijo'."""
    return (1.0 - p_gran) * peq + p_gran * gra

def _cargar_probabilidades_y_densidades():
    """
    Llama a inferencia_probabilidades.ProbabilidadesGiroTipo y
    vuelca:
      - DENSIDADES  -> N_/S_/E_/W_densidad
      - PROB_GIRO   -> dict con claves por tipo (si USAR_PROB_POR_TIPO=True)
      - Variables sueltas SIN sufijo (*_probabilidad) como mezcla
      - Variables POR TIPO con sufijo *_peq / *_gran (si USAR_PROB_POR_TIPO=True)
    """
    from inferencia_probabilidades import ProbabilidadesGiroTipo
    global PROB_GIRO, DENSIDADES
    ip = ProbabilidadesGiroTipo(RUTA_CSV_CONTEO, usar_por_tipo=USAR_PROB_POR_TIPO)
    ip.cargar_datos()
    ip.procesar_datos()

    # 1) Densidades
    DENSIDADES = ip.get_dict_densidades(T_CICLO_REAL)
    globals().update(DENSIDADES)  # publica N_densidad, S_densidad, E_densidad, W_densidad

    # 2) Probabilidades de giro (dict crudo)
    PROB_GIRO = ip.get_dict_parametros()

    # 3) Publicar variables: con y sin sufijo (si aplica)
    if USAR_PROB_POR_TIPO:
        # NORTE: izq=W, recto=S, der=E
        globals()["N_W_probabilidad_peq"] = PROB_GIRO["N_W_probabilidad_peq"]
        globals()["N_S_probabilidad_peq"] = PROB_GIRO["N_S_probabilidad_peq"]
        globals()["N_E_probabilidad_peq"] = PROB_GIRO["N_E_probabilidad_peq"]

        globals()["N_W_probabilidad_gran"] = PROB_GIRO["N_W_probabilidad_gran"]
        globals()["N_S_probabilidad_gran"] = PROB_GIRO["N_S_probabilidad_gran"]
        globals()["N_E_probabilidad_gran"] = PROB_GIRO["N_E_probabilidad_gran"]

        globals()["N_W_probabilidad"] = _mezcla(globals()["N_W_probabilidad_peq"], globals()["N_W_probabilidad_gran"], p_car_grande)
        globals()["N_S_probabilidad"] = _mezcla(globals()["N_S_probabilidad_peq"], globals()["N_S_probabilidad_gran"], p_car_grande)
        globals()["N_E_probabilidad"] = _mezcla(globals()["N_E_probabilidad_peq"], globals()["N_E_probabilidad_gran"], p_car_grande)

        # SUR: izq=E, recto=N, der=W
        globals()["S_E_probabilidad_peq"] = PROB_GIRO["S_E_probabilidad_peq"]
        globals()["S_N_probabilidad_peq"] = PROB_GIRO["S_N_probabilidad_peq"]
        globals()["S_W_probabilidad_peq"] = PROB_GIRO["S_W_probabilidad_peq"]

        globals()["S_E_probabilidad_gran"] = PROB_GIRO["S_E_probabilidad_gran"]
        globals()["S_N_probabilidad_gran"] = PROB_GIRO["S_N_probabilidad_gran"]
        globals()["S_W_probabilidad_gran"] = PROB_GIRO["S_W_probabilidad_gran"]

        globals()["S_E_probabilidad"] = _mezcla(globals()["S_E_probabilidad_peq"], globals()["S_E_probabilidad_gran"], p_car_grande)
        globals()["S_N_probabilidad"] = _mezcla(globals()["S_N_probabilidad_peq"], globals()["S_N_probabilidad_gran"], p_car_grande)
        globals()["S_W_probabilidad"] = _mezcla(globals()["S_W_probabilidad_peq"], globals()["S_W_probabilidad_gran"], p_car_grande)

        # ESTE: izq=N, recto=W, der=S
        globals()["E_N_probabilidad_peq"] = PROB_GIRO["E_N_probabilidad_peq"]
        globals()["E_W_probabilidad_peq"] = PROB_GIRO["E_W_probabilidad_peq"]
        globals()["E_S_probabilidad_peq"] = PROB_GIRO["E_S_probabilidad_peq"]

        globals()["E_N_probabilidad_gran"] = PROB_GIRO["E_N_probabilidad_gran"]
        globals()["E_W_probabilidad_gran"] = PROB_GIRO["E_W_probabilidad_gran"]
        globals()["E_S_probabilidad_gran"] = PROB_GIRO["E_S_probabilidad_gran"]

        globals()["E_N_probabilidad"] = _mezcla(globals()["E_N_probabilidad_peq"], globals()["E_N_probabilidad_gran"], p_car_grande)
        globals()["E_W_probabilidad"] = _mezcla(globals()["E_W_probabilidad_peq"], globals()["E_W_probabilidad_gran"], p_car_grande)
        globals()["E_S_probabilidad"] = _mezcla(globals()["E_S_probabilidad_peq"], globals()["E_S_probabilidad_gran"], p_car_grande)

        # OESTE: izq=S, recto=E, der=N
        globals()["W_S_probabilidad_peq"] = PROB_GIRO["W_S_probabilidad_peq"]
        globals()["W_E_probabilidad_peq"] = PROB_GIRO["W_E_probabilidad_peq"]
        globals()["W_N_probabilidad_peq"] = PROB_GIRO["W_N_probabilidad_peq"]

        globals()["W_S_probabilidad_gran"] = PROB_GIRO["W_S_probabilidad_gran"]
        globals()["W_E_probabilidad_gran"] = PROB_GIRO["W_E_probabilidad_gran"]
        globals()["W_N_probabilidad_gran"] = PROB_GIRO["W_N_probabilidad_gran"]

        globals()["W_S_probabilidad"] = _mezcla(globals()["W_S_probabilidad_peq"], globals()["W_S_probabilidad_gran"], p_car_grande)
        globals()["W_E_probabilidad"] = _mezcla(globals()["W_E_probabilidad_peq"], globals()["W_E_probabilidad_gran"], p_car_grande)
        globals()["W_N_probabilidad"] = _mezcla(globals()["W_N_probabilidad_peq"], globals()["W_N_probabilidad_gran"], p_car_grande)
    else:
        # Si no se usa por tipo, simplemente exponemos las claves sin sufijo
        for k, v in PROB_GIRO.items():
            globals()[k] = v  # p.ej., N_W_probabilidad, N_S_probabilidad, ...

# Ejecutar la carga automáticamente al importar parametros (con fallback silencioso)
if HABILITAR_INFERENCIA:
    try:
        _cargar_probabilidades_y_densidades()
    except Exception as _err:
        raise RuntimeError(f"[ERROR] No se cargaron datos desde CSV: {_err}")


