from random import random 
from parametros import *
from carro import Carro
def generar_carro(salida):
	# Esta lo que hace es crear un carro es decir Entrega un objeto carro 
	# esta funcion le pone la direccion a la que se dirigirá de
	# manera aleatoria, tambien le pone la velucidad de manera aleatoria
	# al considerar la rapidez maxima permitida en el programa
	"""
	Valores posibles de la variable destino
	[0,1]  	Sur
	[0,-1] 	Norte - 
	[1,0] 	Este
	[-1,0] 	Oeste
	"""
	rn = random()
	destino = [None,None]
	if salida=="Norte": # Este caso es en el que el carro se dirige hacia el Sur pero sale desde el norte
		x = int(tamano_mapa["x"]/2)  # Posicion en x desde la que sale el  carro
		y = 0						 # Posicion en y desde la que sale el carro
		v_x = 0						 # Velocidad con la que sale el carro en la componente en x
		v_y = round(rapidez_max*random()) # Velocidad con la que sale el carro en la componente en x
		d_x = 0							  # Direcion a la que se dirige el carro en el eje x 
		d_y = 1							  # Direcion a la que se dirige el carro en el eje y en este caso hacia el sur
		# las condicionales siguientes se emplean para determinar probablisticamte hacia donde se dirigirá el carro 
		if rn < N_E_probabilidad:  # Caso Este ( esto es probabilistico ya que rn es un numero aleatorio entre 0 y 1)
			# ejemplo suponer que N_E_probabilidad=0.2 como rn es un numero aleatorio entre 0 y 1 con distribucion uniforme
			# entonces la probabilidad que rn sea menor a N_E_probabilidad=0.2 es del 20% 
			destino = [1,0]
		elif rn> N_E_probabilidad and rn< N_W_probabilidad+N_E_probabilidad: # Caso en que el carro se vaya a dirigir al Oeste 
			# en este caso el rango en el que caerá el numero rn cambia 
			destino = [-1,0]
		else: # Caso recto hacia el sur
			destino = [0,1]
	if salida=="Sur":
		x = int(tamano_mapa["x"]/2+1)
		y = tamano_mapa["y"]-1
		v_x = 0
		v_y = -round(rapidez_max*random())
		d_x = 0
		d_y = -1
		if rn < S_E_probabilidad:
			destino = [1,0]
		elif rn> S_E_probabilidad and rn< S_W_probabilidad+S_E_probabilidad:
			destino = [-1,0]
		else:
			destino = [0,-1]
	if salida=="Oeste":
		x = 0
		y = int(tamano_mapa["y"]/2+1)
		v_x = round(rapidez_max*random())
		v_y = 0
		d_x = 1
		d_y = 0
		if rn < W_N_probabilidad:
			destino = [0,-1]
		elif rn> W_N_probabilidad and rn< W_S_probabilidad+W_N_probabilidad:
			destino = [0,1]
		else:
			destino = [1,0]
	if salida=="Este":
		x = int(tamano_mapa["x"])-1
		y = int(tamano_mapa["y"]/2)
		v_x = -round(rapidez_max*random())
		v_y = 0
		d_x = -1
		d_y = 0
		if rn < E_N_probabilidad:
			destino = [0,-1]
		elif rn> E_N_probabilidad and rn< E_S_probabilidad+E_N_probabilidad:
			destino = [0,1]
		else:
			destino = [-1,0]
	if random()<p_car_grande: # aqui se determina si el carro es grande o pequeño tambien con una probabilidad p_car_grande
		tamano = tamano_car_grande
	else:
		tamano = 1
	

	carro = Carro([x,y],[v_x,v_y],tamano,destino,[d_x,d_y],tamano_mapa) # Se intancia el carro con los datos generados anteriormente
	return carro
