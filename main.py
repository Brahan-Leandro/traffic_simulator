from random import random 
import matplotlib.pyplot as plt 
import matplotlib.animation as an
import numpy as np

from carro import Carro
from vacio import Vacio
from celda import Celda
tamano_mapa = {"x":100, "y":100}
pasos = 1000
N_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el norte
S_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el sur
W_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el oeste
E_densidad = 0.1		#probabilidad de la cantidad de carros que salen desde el Este
p_car_grande = 0.5
rapidez_max = 2
probabilidad_frenar = 0.2
tamano_car_grande = 3
def cargar_celdas():
	global tamano_mapa
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar)
	for y in range(tamano_mapa["y"]):
		posicion = (int(tamano_mapa["y"]/2),y)
		espacio.agregar_celda(Celda("via",posicion))
	return espacio
def generar_carro(salida):
	global tamano_mapa
	if salida=="Norte":
		x = int(tamano_mapa["x"]/2)
		y = 0
		v_x = 0
		v_y = round(rapidez_max*random())
		d_x = 0
		d_y = 1
	if salida=="Sur":
		x = int(tamano_mapa["x"]/2+1)
		y = tamano_mapa["y"]-1
		v_x = 0
		v_y = -round(rapidez_max*random())
		d_x = 0
		d_y = -1
	if salida=="Oeste":
		x = 0
		y = int(tamano_mapa["y"]/2+1)
		v_x = round(rapidez_max*random())
		v_y = 0
		d_x = 1
		d_y = 0
	if salida=="Este":
		x = int(tamano_mapa["x"])-1
		y = int(tamano_mapa["y"]/2)
		v_x = -round(rapidez_max*random())
		v_y = 0
		d_x = -1
		d_y = 0
	if random()<p_car_grande:
		tamano = tamano_car_grande
	else:
		tamano = 1
	carro = Carro([x,y],[v_x,v_y],tamano,[1,1],[d_x,d_y])
	return carro
						   
def main():
	espacio = cargar_celdas()
	
	def update(i):
		espacio.condiciones_carros()
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
		plt.imshow(np.transpose(matris_plot),cmap="viridis")	
	fig = plt.figure()
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=200,repeat=False)
	plt.show()

if __name__=="__main__":
	main()
