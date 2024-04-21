from random import random 
import matplotlib.pyplot as plt 
import matplotlib.animation as an
import numpy as np

from carro import Carro
from vacio import Vacio
from semaforos import Sistema_Semaforos
from parametros import *
from generador_carros import generar_carro						   
def main():
	semaforos = Sistema_Semaforos(tiempo_verde,tiempo_verde)
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar,semaforos.estado)
	def update(i):
		semaforos.actualizar_estado(i)
		espacio.actualizar_semaforo(semaforos.estado)
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
		print(i)
		plt.clf()
		plt.imshow(np.transpose(matris_plot),cmap="tab10")	
	fig = plt.figure()
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=rapidez_simulacion,repeat=False)
	plt.show()

if __name__=="__main__":
	main()
