from random import random 
from parametros import *
from carro import Carro
def generar_carro(salida):
	"""
	Valores posibles de la variable destino
	[0,1]  	Sur
	[0,-1] 	Norte - 
	[1,0] 	Este
	[-1,0] 	Oeste
	"""
	rn = random()
	destino = [None,None]
	if salida=="Norte":
		x = int(tamano_mapa["x"]/2)
		y = 0
		v_x = 0
		v_y = round(rapidez_max*random())
		d_x = 0
		d_y = 1
		if rn < N_E_probabilidad:
			destino = [1,0]
		elif rn> N_E_probabilidad and rn< N_W_probabilidad+N_E_probabilidad:
			destino = [-1,0]
		else:
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
	if random()<p_car_grande:
		tamano = tamano_car_grande
	else:
		tamano = 1
	

	carro = Carro([x,y],[v_x,v_y],tamano,destino,[d_x,d_y],tamano_mapa)
	return carro
