tamano_mapa = {"x":100, "y":100}
pasos = 1000
rapidez_simulacion = 150  # en milisegundos
N_densidad = 0.15		#probabilidad de la cantidad de carros que salen desde el norte
S_densidad = 0.15		#probabilidad de la cantidad de carros que salen desde el sur
W_densidad = 0.0  		#probabilidad de la cantidad de carros que salen desde el oeste
E_densidad = 0.0		#probabilidad de la cantidad de carros que salen desde el Este

N_E_probabilidad = 1   
N_W_probabilidad = 0.0
S_E_probabilidad = 0.0
S_W_probabilidad = 1
E_N_probabilidad = 0.0
E_S_probabilidad = 0.0
W_N_probabilidad = 0.0
W_S_probabilidad = 0.0

N_S_probabilidad = 1-N_E_probabilidad-N_W_probabilidad
S_N_probabilidad = 1-S_E_probabilidad-S_W_probabilidad
E_W_probabilidad = 1-E_S_probabilidad-E_N_probabilidad
W_E_probabilidad = 1- W_N_probabilidad-W_S_probabilidad

tiempo_verde = 10
tiempo_amarillo = 2
modo_semaforos = "dos_verde"    # dos_verde

p_car_grande = 0.5
rapidez_max = 2
probabilidad_frenar = 0.2
tamano_car_grande = 2
