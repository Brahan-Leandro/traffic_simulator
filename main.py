from random import random 
import matplotlib.pyplot as plt 
import matplotlib.animation as an
import numpy as np

from carro import Carro
from vacio import Vacio
from celda import Celda
from semaforos import Sistema_Semaforos
tamano_mapa = {"x":100, "y":100}
pasos = 1000
N_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el norte
S_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el sur
W_densidad = 0.1  		#probabilidad de la cantidad de carros que salen desde el oeste
E_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el Este

N_E_probabilidad = 0.3
N_W_probabilidad = 0.3
S_E_probabilidad = 0.2
S_W_probabilidad = 0.2
E_N_probabilidad = 0.2
E_S_probabilidad = 0.2
W_N_probabilidad = 0.2
W_S_probabilidad = 0.2

N_S_probabilidad = 1-N_E_probabilidad-N_W_probabilidad
S_N_probabilidad = 1-S_E_probabilidad-S_W_probabilidad
E_W_probabilidad = 1-E_S_probabilidad-E_N_probabilidad
W_E_probabilidad = 1- W_N_probabilidad-W_S_probabilidad

tiempo_verde = 30
tiempo_amarillo = 10

p_car_grande = 0.5
rapidez_max = 2
probabilidad_frenar = 0.2
tamano_car_grande = 2



def generar_carro(salida):
	global tamano_mapa
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
						   
def main():
	semaforos = Sistema_Semaforos(tiempo_verde,tiempo_verde)
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar,semaforos.estado)

	def update(i):
		semaforos.actualizar_estado(i)
		espacio.actualizar_semaforo(semaforos.estado)
		espacio.condiciones_carros()
		espacio.condiciones_semaforos()
		if random()<N_densidad:
			espacio.agregar_carro(generar_carro("Norte"))
		if random()<S_densidad:
			espacio.agregar_carro(generar_carro("Sur"))
		if random()<W_densidad:
			espacio.agregar_carro(generar_carro("Oeste"))
		if random()<E_densidad:
			espacio.agregar_carro(generar_carro("Este"))
		matris_plot = espacio.calcular_avance()	
		plt.clf()
		plt.imshow(np.transpose(matris_plot),cmap="tab10")	
	fig = plt.figure()
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=500,repeat=False)
	plt.show()

if __name__=="__main__":
	main()
