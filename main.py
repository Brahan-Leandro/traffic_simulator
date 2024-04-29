from random import random 
import matplotlib.pyplot as plt 
import matplotlib.animation as an
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np

from carro import Carro
from vacio import Vacio
from semaforos import Sistema_Semaforos
from parametros import *
from generador_carros import generar_carro						   
def main():
	cmap, norm = cmap_norm()
	T=[]
	semaforos = Sistema_Semaforos(tiempo_verde,tiempo_amarillo,modo_semaforos)
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar,semaforos.estado)
	densidad_salida_Norte =[]
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
		densidad_salida_Norte.append(calcular_densidad(matris_plot,"entrada_norte"))
		plt.clf()
		#print(i)
		T.append(i)
		plt.imshow(np.transpose(matris_plot),cmap=cmap,norm=norm)	
		
	fig = plt.figure(200)
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=rapidez_simulacion,repeat=False)
	plt.show()
	fig2 = plt.figure(300)
	#T = [t for t in range(pasos+1)]
	plt.plot(T,densidad_salida_Norte)
	plt.show()

def calcular_densidad(matris,via):
	numero_carros = 0
	if via == "entrada_norte":
		for y in range(int(tamano_mapa["y"]/2)-1):
			if matris[int(tamano_mapa["x"]/2)][y]==1:
				numero_carros +=1
	return numero_carros/(tamano_mapa["y"]/2-1)
def cmap_norm():
	levels = [0,1,7,8, 10, 20, 30,40]
	colors = [[128/255,128/255,128/255], #0-1   Color Vias
		      [252/255,108/255,2/255],   #1-7   Color carros cabina
		      [184/255,170/255,63/255],  # 7-8 Color Areas Comunes
			  [0/255,79/255,215/255],   #8-10  color Carros carroceria
			  [255/255,0,0],			 #10-20
			  [30/255,215/255,0],			 #20-30	
			  [237/255,252/255,2/255]]
	return mpl.colors.from_levels_and_colors(levels, colors)
if __name__=="__main__":
	main()
