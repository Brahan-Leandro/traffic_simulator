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
	cmap, norm = cmap_norm()    # cmap y norm se utilizan para determinar el color para cada numero en la matriz
								# a plotear y la funcion cmap_norm esta creada manu
	cmap2, norm2 = cmap_norm2() # lo mismo que el anterior solo que se emplea para determinar los colores para plotear
								# la matris de ocupacion 
	T=[]     # Lista que contiene el numeros que indican el fotograma ejemplo [1,2,3,4] en este caso la lista tiene 4 fotogramas
	ocupacion_norte_sur = np.zeros((tamano_mapa['y'],pasos)) # matris que contiene la ocupacion en el eje x va el espacio y el 'y' la evolucion temporal
	ocupacion_sur_norte = np.zeros((tamano_mapa['y'],pasos))
	ocupacion_este_oeste = np.zeros((tamano_mapa['y'],pasos))	
	ocupacion_oeste_este = np.zeros((tamano_mapa['y'],pasos))	
	semaforos = Sistema_Semaforos(tiempo_verde,tiempo_amarillo,modo_semaforos) # Instancia para los semaforos
	espacio = Vacio(tamano_mapa,rapidez_max,probabilidad_frenar,semaforos.estado) # Instancia para los Espacio
	# Se emplea  para graficar la densidad de de carros  por cada tramo
	densidad_entrada_Norte =[]  
	densidad_entrada_Sur =[]
	densidad_entrada_Este =[]
	densidad_entrada_Oeste =[]
	
	flujo_entrada_Norte =[]
	flujo_entrada_Sur =[]
	flujo_entrada_Este =[]
	flujo_entrada_Oeste =[]
	
	def update(i): 
		# Esta funcion se es la que se encarga de controlar el ciclo general del programa
		# se llama en cada instante y las operaciones que hace son en el siguiente orden
		espacio.reset_velocidad()
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
			
		matris_plot,v_p_norte,v_p_sur,v_p_este,v_p_oeste = espacio.calcular_avance() #El espacio calcula la matris siguiente a plotear 
		############## Se extrae la ocupacion de los carros para las 4 vias  en el instante i
		ocupacion_norte_sur[:,i]=matris_plot[int(tamano_mapa["x"]/2)]
		ocupacion_sur_norte[:,i]=list(np.array(matris_plot)[int(tamano_mapa["x"]/2)+1,0:int(tamano_mapa["x"])])
		ocupacion_este_oeste[:,i]=list(np.array(matris_plot)[0:int(tamano_mapa["x"]),int(tamano_mapa["y"]/2)])
		ocupacion_oeste_este[:,i]=list(np.array(matris_plot)[0:int(tamano_mapa["x"]),int(tamano_mapa["y"]/2)+1])
		##############
		
		############## Se determina la densidad en el instante i para cada una de las vias
		densidad_entrada_Norte.append(calcular_densidad(matris_plot,"entrada_norte"))
		densidad_entrada_Sur.append(calcular_densidad(matris_plot,"entrada_sur"))
		densidad_entrada_Este.append(calcular_densidad(matris_plot,"entrada_este"))
		densidad_entrada_Oeste.append(calcular_densidad(matris_plot,"entrada_oeste"))
		#############
		
		##############
		# para el calculo se hace un cambio de unidades ya que v_p_norte,v_p_sur,v_p_este,v_p_oeste
		# estan en originalmente en unidades de celdas/segundo para cambiarlo a metros 
		# se tiene en cuenta que una celda mide 4.5 metros que se puso en el archivo parametros
		# por ello se multiplica por medida_de_una_celda la densidad 
		flujo_entrada_Norte.append(densidad_entrada_Norte[-1]*v_p_norte*medida_de_una_celda)
		flujo_entrada_Sur.append(densidad_entrada_Sur[-1]*v_p_sur*medida_de_una_celda)
		flujo_entrada_Este.append(densidad_entrada_Este[-1]*v_p_este*medida_de_una_celda)
		flujo_entrada_Oeste.append(densidad_entrada_Oeste[-1]*v_p_oeste*medida_de_una_celda)
		##############
		
		plt.clf() # Se limpia la pantalla que se va a plotear, es decir para generar la animacion se
				  # debe plotear el fotograma anterior y se plotea la nueva matris
		#print(i)
		T.append(i/3600)# Se guarda el numero de fotograma i  que hace de las veces de tiempo 
						# el 3600 es importante ya que si se considera que cada fotograma es un 
						# segundo entonces al dividir i entre 3600 se estaria pasando el tiempo a horas
		#T.append(i) 
		#plt.imshow(np.transpose(matris_plot),cmap=cmap,norm=norm)	
		
		# Se plotea la matris matris_plot que contiene todos los 
		# carros, los semaforos, las vias y la area comun 
		# cada elemento (carro, semaforos... etc) tiene un numero correspondiente
		# dentro de la matris se muestra un ejemplo de matris 5x5 
		"""
		-  -  -  --  --  -  -  -  -  --  --  -
		7  7  7   7   7  7  0  0  7   7   7  7
		7  7  7   7   7  7  0  0  7   7   7  7
		7  7  7   7   7  7  0  0  7   7   7  7
		7  7  7  20  20  7  0  0  7  10  10  7
		7  7  7  20  20  7  0  0  7  10  10  7
		7  7  7   7   7  7  0  0  7   7   7  7
		0  0  0   0   0  0  0  0  0   1   0  0
		1  8  8   8   8  0  0  0  0   0   0  0
		7  7  7   7   7  7  0  0  7   7   7  7
		7  7  7  10  10  7  0  0  7  20  20  7
		7  7  7  10  10  7  0  0  7  20  20  7
		7  7  7   7   7  7  0  0  7   7   7  7
		-  -  -  --  --  -  -  -  -  --  --  -
		"""
		# An la matris ejemplo cada una de los numeros corresponde a algun objeto es decir estan codificados asi:
		#  0  ->  Via  en la grafica  Gris
		#  1  ->  Carro pequeño que en la grafica se mira Naranja 
		#  8  ->  Carro Grande que en la grafica se mira Azul
		#  7  ->  Areas Comunes que en la grafica se miran Amarillo Napoles
		#  10 ->  Semaforo En Verde 
		#  20 ->  Semaforo Rojo
		plt.pcolormesh(np.rot90(matris_plot),cmap=cmap,norm=norm)	 # Se plotea la matris matris_plot
		plt.gca().set_aspect('equal', adjustable='box')  # Se utiliza para que cada celda
		plt.axis('off')

														 # de la matriz tengan el mismo ancho y alto
	######### Se emplea para crear la animacion a la funcion FuncAnimation se le tiene que pasar la 
	######### la funcion update, los frames, que son el numero de fotograms  
	######### y el interval que es el tiempo que transcurre en cada fotograma 
	#########  repeat = False es para que una vez finalicen los fotogramas no se repita nuevamente la simulacion
	fig = plt.figure(200) 
	ani = an.FuncAnimation(fig,update,frames=pasos,interval=rapidez_simulacion,repeat=False) 
	plt.show()
	#########
	
	######### Se plotea Las graficas como densidad o ocupacion
	fig2 = plt.figure("Densidad Norte Sur Dos Semaforos")
	plt.plot(T,densidad_entrada_Norte,label="Entrada norte")
	plt.plot(T,densidad_entrada_Sur,label="Entrada sur")
	plt.xlabel('tiempo en horas')
	plt.ylabel('Densidad en carros/metro')
	plt.legend(loc='upper left')
	
	fig3 = plt.figure("Densidad Este oeste Dos Semaforos")
	plt.plot(T,densidad_entrada_Este,label="Entrada Este")
	plt.plot(T,densidad_entrada_Oeste,label="Entrada Oeste")
	plt.xlabel('tiempo en horas')
	plt.ylabel('Densidad en carros/metro')
	plt.legend(loc='upper left')
	
	fig4, axs = plt.subplots(1, 4)
	fig4.suptitle('Ocupacion')
	axs[0].pcolormesh(np.transpose(ocupacion_norte_sur),cmap=cmap2,norm=norm2)
	axs[0].set_title("Norte Sur")
	axs[1].pcolormesh(np.transpose(ocupacion_sur_norte),cmap=cmap2,norm=norm2)
	axs[1].set_title("Sur  Norte")
	axs[2].pcolormesh(np.transpose(ocupacion_este_oeste),cmap=cmap2,norm=norm2)
	axs[2].set_title("Este Oeste")
	axs[3].pcolormesh(np.transpose(ocupacion_oeste_este),cmap=cmap2,norm=norm2)
	axs[3].set_title("Oeste Este")
	plt.gca().set_aspect('equal', adjustable='box')
	axs[0].set(xlabel='Posicion', ylabel='Tiempo')
	
	fig5 = plt.figure("Flujo Este Oeste")
	plt.plot(T,flujo_entrada_Este,label="Entrada Este")
	plt.plot(T,flujo_entrada_Oeste,label="Entrada Oeste")
	plt.xlabel('tiempo en horas')
	plt.ylabel('Flujo  en carros/segundos')
	plt.legend(loc='upper right')	
	
	fig6 = plt.figure("Flujo Norte Sur")
	plt.plot(T,flujo_entrada_Norte,label="Entrada Norte")
	plt.plot(T,flujo_entrada_Sur,label="Entrada Sur")
	plt.xlabel('tiempo en horas')
	plt.ylabel('Flujo  en carros/segundos')
	plt.legend(loc='upper right')
	
	plt.show()

def calcular_densidad(matris,via):
	# Esta Funcion lo que hace es contar el numero de carros en cada via 
	# y retorna los la cantidad de carros dividida el tamaño de la via lo que se le llama densidad
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
	return numero_carros/(tamano*medida_de_una_celda)
def cmap_norm():
	# Se crea el mapa de colores para plotear la matris de los carros (matris_plot)
	# La variable levels contiene los rangos que se tomaran en cuenta 
	# por ejemplo el rango 0-1 que incluye el 0, son las vias que se pintaran de gris 
	# luego sigue el rango de 1-7 que incluye el 1,2,3,4,5,6 pinta el color de los carros pequeños
	# y asi hasta llegar a 40 
	# por otro lado la variable colors contiene una matris que los colores codificados en 
	# RGB por ejemplo la primer fila -> [128/255,128/255,128/255] tiene 128 de rojo 128 de Verde y 128 de Azul 
	# que mezclados constituyen el Gris  ahora se lo divide entre 255 ya que matplotlib solo recibe numeros entre
	# el rango [0, 1] 
	levels = [0,1,7,8, 10, 20, 30,40]
	colors = [[128/255,128/255,128/255], #0-1   Color Vias
		      [252/255,108/255,2/255],   #1-7   Color carros cabina
		      [184/255,170/255,63/255],  # 7-8 Color Areas Comunes
			  [0/255,79/255,215/255],   #8-10  color Carros carroceria
			  [255/255,0,0],			 #10-20
			  [30/255,215/255,0],			 #20-30	
			  [237/255,252/255,2/255]]
	return mpl.colors.from_levels_and_colors(levels, colors)
def cmap_norm2():
	# Esta funcion retorna el mapa de colores para plotear la matris de ocupacion
	# Que es la que se implime solo blanco y negro
	levels = [0,1,7,8,10]
	colors = [[1,1,1],   #0-1   Color Vias 
		      [0,0,0],   #1-7   Color carros pequeños
		      [0,0,0],    #7-8 Color Areas Comunes
			  [0,0,0],      #8-10  color Carros Grandes

			  ]
	return mpl.colors.from_levels_and_colors(levels, colors)

if __name__=="__main__":
	main()
