"""
Este archivo contiene la funcion principal donde se empieza a correr el programa
Dentro de la funcion main hay otra funcion llamada update, aquella funcion es 
la que actualizará el estado general de la simulacion, es decir la funcion update
es la que estara llamando cada instante para calcular el estado posterior de la simulacion.
Esta funcion NO esta dentro de un ciclo ya que se aprovecha que la libreria de matplotlib
(utilizada para plotear la grafica) llama a esta funcion update en cada instante, lo anterior 
está en la linea que contiene an.FuncAnimation, se logra ver que el segundo argumento de la 
funcion FuncAnimation es la funcion update, en general ese es funcionamiento  en los siguientes 
comentarios se especifica cada variable 
"""
# Importando librerias para plotear y generar los numeros aleatorios
from random import random 
import matplotlib.pyplot as plt 
import matplotlib.animation as an
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np
# Importando las Clases que se utilizan para la simulacion
from carro import Carro # clase  especifica un carro  que tiene  velocidad, direccion,posicion... etc
from vacio import Vacio # Clase especifica el espacio, el cual contiene 
#los carros y ademas se encarga de calcular  la logica del estado posterior mediante la funcion calcular_avance
from semaforos import Sistema_Semaforos # Clase que controla el estado de los semaforos
from parametros import *   # Contiene todos los parametros que especifican las caracteristicas de la simulacion 
from generador_carros import generar_carro # Se es una duncion que encarga de intanciar nuevos carros						   
def main():
	cmap, norm = cmap_norm()
	T=[]     # Lista que contiene el numeros que indican el fotograma ejemplo [1,2,3,4] en este caso la lista tiene 4 fotogramas
	semaforos = Sistema_Semaforos(tiempo_verde,tiempo_amarillo,modo_semaforos) # Instancia para los semaforos
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar,semaforos.estado) # Instancia para los Espacio
	# Se emplea  para graficar la densidad de de carros  por cada tramo
	densidad_entrada_Norte =[] 
	densidad_entrada_Sur =[]
	densidad_entrada_Este =[]
	densidad_entrada_Oeste =[]
	# Se emplea  para graficar la intensidad de de carros  por cada tramo
	intensidad_norte=[]
	intensidad_sur=[]
	intensidad_este=[]
	intensidad_oeste=[]
	
	def update(i): 
		# Esta funcion se es la que se encarga de controlar el ciclo general del programa
		# se llama en cada instante y las operaciones que hace son en el siguiente orden
		
		semaforos.actualizar_estado(i) # Actualizar el estado de los semaforos es decir en cada instante el objeto semaforos 
									   # va a cambiar segun vaya avanzando la simulacion 
		espacio.actualizar_semaforo(semaforos.estado) # Se le da informacion al manejador general (Espacio) del estado del semaforo
		espacio.condiciones_carros()  # Se revisa las condiciones de frenado
		
		# las siguientes condiciones que determinan si se debe agregar un nuevo carro a la salida Norte, Sur, Oeste, Este respectivamente 
		# al considerar la probabilidad N_densidad,S_densidad, W_densidad,E_densidad
		if random()<N_densidad:
			espacio.agregar_carro(generar_carro("Norte"))
		if random()<S_densidad:
			espacio.agregar_carro(generar_carro("Sur"))
		if random()<W_densidad:
			espacio.agregar_carro(generar_carro("Oeste"))
		if random()<E_densidad:
			espacio.agregar_carro(generar_carro("Este"))
			
		matris_plot,i_norte,i_sur,i_este,i_oeste = espacio.calcular_avance() # Se calcula el 
		
		intensidad_norte.append(i_norte)
		intensidad_sur.append(i_sur)
		intensidad_este.append(i_este)
		intensidad_oeste.append(i_oeste)
			
		densidad_entrada_Norte.append(calcular_densidad(matris_plot,"entrada_norte"))
		densidad_entrada_Sur.append(calcular_densidad(matris_plot,"entrada_sur"))
		densidad_entrada_Este.append(calcular_densidad(matris_plot,"entrada_este"))
		densidad_entrada_Oeste.append(calcular_densidad(matris_plot,"entrada_oeste"))
		plt.clf()
		#print(i)
		T.append(i)
		plt.imshow(np.transpose(matris_plot),cmap=cmap,norm=norm)	
		
	fig = plt.figure(200)
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=rapidez_simulacion,repeat=False)
	plt.show()
	fig2 = plt.figure("Densidad Norte Sur Dos Semaforos")
	plt.plot(T,densidad_entrada_Norte,label="Entrada norte")
	plt.plot(T,densidad_entrada_Sur,label="Entrada sur")
	plt.legend(loc='upper right')
	
	fig3 = plt.figure("Densidad Este oeste Dos Semaforos")
	plt.plot(T,densidad_entrada_Este,label="Entrada Este")
	plt.plot(T,densidad_entrada_Oeste,label="Entrada Oeste")
	plt.legend(loc='upper right')
		
	fig4 = plt.figure("Intensidad Norte Sur")
	plt.plot(T,intensidad_norte,label="Entrada Norte")
	plt.plot(T,intensidad_sur,label="Entrada Sur")
	plt.legend(loc='upper right')
	
	fig4 = plt.figure("Intensidad Este Oeste")
	plt.plot(T,intensidad_este,label="Entrada Este")
	plt.plot(T,intensidad_oeste,label="Entrada Oeste")
	plt.legend(loc='upper right')
	plt.show()

def calcular_densidad(matris,via):
	numero_carros = 0
	tamano = 0
	if via == "entrada_norte":
		for y in range(int(tamano_mapa["y"]/2)-1):
			tamano+=1
			if matris[int(tamano_mapa["x"]/2)][y]==1 or matris[int(tamano_mapa["x"]/2)][y]==8:
				numero_carros +=1
				#return numero_carros/(tamano_mapa["y"]/2-1)
	if via == "entrada_sur":
		for y in range(int(tamano_mapa["y"]/2)+2,tamano_mapa["y"]):
			tamano+=1
			if matris[int(tamano_mapa["x"]/2)+1][y]==1 or matris[int(tamano_mapa["x"]/2)+1][y]==8:
				numero_carros +=1
	if via == "entrada_este":
		for x in range(int(tamano_mapa["x"]/2)+2,tamano_mapa["x"]):
			tamano+=1
			if matris[x][int(tamano_mapa["y"]/2)]==1 or  matris[x][int(tamano_mapa["y"]/2)]==8:
				numero_carros +=1
	if via == "entrada_oeste":
		for x in range(int(tamano_mapa["x"]/2)-1):
			tamano+=1
			if matris[x][int(tamano_mapa["y"]/2+1)]==1 or matris[x][int(tamano_mapa["y"]/2+1)]==8:
				numero_carros +=1
	return numero_carros/(tamano)
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
