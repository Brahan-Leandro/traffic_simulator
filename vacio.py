from math import sqrt
from random import random
from utilidades import *

"""
Esta Clase se encarga de manejar en si todos los componentes, que involucan
como tal la simulacion, maneja los carros, las reglas, etc. 
El metodo que se encarga en general del manejo de los carros es el llamado calcular_avance
el cual se explica mas adelante
"""
class Vacio:
	def __init__(self,tamano_mapa,rapidez_max,probabilidad_frenar,estado_semaforos):	
		self.rapidez_max=rapidez_max # Este atributo es la maxima rapidez permitidas a los carros 
		self.carros = [] # esta es una lista que contiene todas las intancias (objetos) de la clase carro
						 # aqui se encuentran guardados los carros que se encuentran actualmente en las vias
		self.carros_A = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])] # esta es la matriz que se retorna para plotearla en la funcion main
		self.carros_A_anterior = self.carros_A  # Esta matris es la que contiene la informacion del fotograma anterior 
		self.tamano_mapa = tamano_mapa 
		self.probabilidad_frenar=probabilidad_frenar
		self.colorear_areas()  # Se llama esta funcion para llenar las areas en la que los carros no pueden andar es decir esto es todo menos las vias y los semaforos
		self.estado_semaforos = estado_semaforos # se obtiene el estado de los semaforos para saber como actuar en caso de cada configuracion de los semaforos
		self.suma_v_norte = 0  # Este atributo contiene la suma de los carros que salen desde el norte
		self.suma_v_sur = 0    # Este atributo contiene la suma de los carros que salen desde el sur
		self.suma_v_este = 0   # Este atributo contiene la suma de los carros que salen desde el este
		self.suma_v_oeste = 0    # Este atributo contiene la suma de los carros que salen desde el oeste
		
		self.N_carro_norte = 0   # Este atributo contiene la cantidad de carros que salen desde el norte
		self.N_carro_sur = 0	 # Este atributo contiene la cantidad de carros que salen desde el sur
		self.N_carro_este = 0	 # Este atributo contiene la cantidad de carros que salen desde el este
		self.N_carro_oeste = 0	 # Este atributo contiene la cantidad de carros que salen desde el oeste
		
	def colorear_areas(self,):
		# Se establece los valores parra las areas comunes que son las que en la simulacion aparecen en amarillo
		# En el primer ciclo for se llenan los dos cuadrados izquierdos de la simulacion 

		for i in range(0,int(self.tamano_mapa["x"]/2)): 
			self.carros_A[i][0:int(self.tamano_mapa["y"]/2)]=[7 for z in range(int(self.tamano_mapa["y"]/2))]
			self.carros_A[i][int(self.tamano_mapa["y"]/2)+2:]=[7 for z in range(int(self.tamano_mapa["y"]-(self.tamano_mapa["y"]/2+2)))]
			
		# En el segundo ciclo for se llenan los dos cuadrados derechos de la simulacion 
		for i in range(int(self.tamano_mapa["x"]/2)+2,int(self.tamano_mapa["x"])):
			self.carros_A[i][0:int(self.tamano_mapa["y"]/2)]=[7 for z in range(int(self.tamano_mapa["y"]/2))]
			self.carros_A[i][int(self.tamano_mapa["y"]/2)+2:]=[7 for z in range(int(self.tamano_mapa["y"]-(self.tamano_mapa["y"]/2+2)))]
	def agregar_carro(self,carro):
		# se agrega el carro nuevo que se crea, claro está cada vez que se llame
		# recibiendo como parametro el carro que se le ha dado
		# el condicional se utiliza para mirar si hay un carro ya en la posicion que se lo
		# agregara, caro si hay un carro ya en esa posicion no se puede agregar uno nuevo
		if self.carros_A[carro.posicion[0]][carro.posicion[1]]==0:
			if carro.tamano == 2:
				self.carros.append(carro)
				carro.posicion[0] =carro.posicion[0]+ carro.direccion[0]
				carro.posicion[1]= carro.posicion[1]+carro.direccion[1]
			
			else:
				self.carros.append(carro)
			
			self.carros_A[carro.posicion[0]][carro.posicion[1]]=1
			return True
		else:
			return False
	def calcular_avance(self):
		#Esta funcion Controla en general el avance de los carros 
		# lo primero que se hace es guargar el estado de la matris carro_A
		# lo siguiente es ir revisando carro por carro si puede avanzar 
		self.carros_A_anterior = self.carros_A
		for carro in self.carros: # lo de ir revisando se lo hace en este ciclo
			self.calcular_suma_velocidades(carro)
			#v_x = carro.velocidad[0] 
			#v_y = carro.velocidad[1]
			for m in range(0,carro.rapidez): # Este ciclo avanza el carro las celdas de una en una 
											 # dentro de este ciclo se hacen varias cosas una es
											 # que se revisa si hay algun obstaculo 
											 # adelante o si el posible avance de carro puede producir 
											 # un trancon en el que se bloquee toda la simulacion 
											 # entonces no se avanza, tambien se revisa las si el semaforo esta en
											 #rojo no se podra avanzar los detalles se explican adelante
				if self.condicion_anti_atascos(carro): # Este condicional revisa si un posible avance del carro 
													   # pueda provocar un trancon
													   # el metodo condicion_anti_atascos revisa si habra atasco
													   # y retorna True si se generara atasco y False si no se 
													   # generará atascos
					carro.detenerse() # Aqui se detiene el carro ya que ha habido un atasco
					break  # se rompe el ciclo es decir el ciclo termina ya que no es posible avanzar mas debido 
						   # al posible atasco
				if (self.validar_futura_frontera(carro)): # Se valida si el carro en el proxima avance de la celda saldrá 
														  # del mapa la funcion validar_futura_frontera retorna True si
														  # el carro estará dentro de los limites en el siguiente avance
														  # y False si el carro esta muy cerca de salir de la frontera
					if self.carros_A_anterior[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]] == 0: 
					# En el condicional anterior se revisa si hay algun obstaculo al frente del carro 
					# en el caso de que no se encuentre nada es decir si la siguiente posicion de la matris 
					# carros_A_anterior[proxima_posicion_del_carro_en_x][proxima_posicion_del_carro_en_x] es igual a cero
					#entonces no se encuentra nada procede a avanzar 
						self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=1 # se avanza el carro a la siguiente posicion
						self.carros_A[carro.posicion[0]][carro.posicion[1]]=0 # se elimina la posicion anterior donde ha estado el carro
						if carro.tamano > 1: # Esta condicion evalua si el carro es grande entonces se hace una serie de cambios
							self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=8 # aqui se modifica el 1 que se habia puesto anteriormente 
																									  # ya que el 1 es para carros pequaños y 8 para carros grandes
							self.carros_A[carro.posicion[0]-carro.direccion[0]][carro.posicion[1]-carro.direccion[1]]=0 # Se borra la cola del carro grande
							self.carros_A[carro.posicion[0]][carro.posicion[1]]=8 # Como es carro grande se activa nuevamente la posicion actual pero 
																				  # en este caso esta activacion es para la cola del carro es decir
																				  #en las dos lineas anteriores se adelanta la cola del carro 
							
							if carro.posicion == carro.celda_decision: # Este es un caso particular donde el carro ya ha dado la curva y no se le ha borrado la cola
																	   # debido a que anteriormente el carro corria de manera lineal pero en una curva la cola se 
																	   # debe eliminar considerando de donde viene el carro por ello es nesesario saber de donde salió el carro
																	   # de no estar este fragmento se generaria atascos ya que se quedaria pegada la cola del carro grande
																	   # con los carros pequeños no hay problema
								self.carros_A[carro.posicion[0]-carro.salida[0]][carro.posicion[1]-carro.salida[1]]=0 # como se dijo se elimina la cola
								
						carro.avanzar() # Aqui si sefinitivamente se avanza el carro, los otros avances eran para la matris
								
						self.condiciones_semaforos(carro) # aqui se revisa si el carro esta en zona de semaforo
														  # si es asi el carro debe detenerse
														  # lo cual cambiaria la velodidad y la rapidez a 0
						if carro.rapidez == 0:# si con lo anterior la rapidez es cero debe el carro no puede avanzar mas
											  # por lo que se debe romper el ciclo de abance por eso el break
							break 
						if carro.posicion == carro.celda_decision: # Se evalua si el carro está en la celda 
																   # que debe cambiar la direccion 
																   # si es asi se cambia la direccion del carro
							carro.cambiar_direccion()	
					else:
						#Aqui se detiene el carro debido a que se ha encontrado un obstaculo frente del carro
						carro.detenerse() # la velocidad y rapidez se comvierten en cero y se rompe el ciclo
						break
				else:
					# este es el caso contrario en el que el carro en la siguiente posicion caiga fuera del mapa 
					# en este caso se elimina el carro de la lista y de la matris carros_A que lo hace el metodo eliminar_carro
					self.eliminar_carro(carro)
					break
		# En las siguientes condiciones se tiene en cuenta
		#  la division por cero y ademas se calcula la velocidad promedio para cada segmento
		if self.N_carro_norte !=0:
			v_p_norte = self.suma_v_norte/self.N_carro_norte 	
		else:
			v_p_norte = 0
		if self.N_carro_sur != 0:
			 v_p_sur = self.suma_v_sur/self.N_carro_sur
		else:
			v_p_sur = 0 
		if self.N_carro_este !=0:
			v_p_este = self.suma_v_este/self.N_carro_este 
		else: 
			v_p_este = 0 
		if self.N_carro_oeste != 0:
			v_p_oeste = self.suma_v_oeste/self.N_carro_oeste 
		else: 
			v_p_oeste = 0
			
		# Una vez se ha revisado el avance de cada auto se retorna la matris
		return self.carros_A,v_p_norte,v_p_sur,v_p_este,v_p_oeste

	def eliminar_carro(self,carro):
		# Esta Metodo se encarga de eliminar un carro que en general se elimina si ya se ha salido de la frontera
		# se hace un ciclo ya que si el carro es grande se debe eliminar variac celdas de la matris carros_A
		for k in range(carro.tamano+2):
			self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=0
		self.carros.remove(carro) # se remueve el carro de la lista de carros
		
	def validar_futura_frontera(self,carro):
		# Este Metodo se encarga de validar si el carro esta por dentro de la frontera
		# y mirando que primero que todo la posicion futura del carro esta es menor al limite superior del mapa 
		# Eso se guarda en la variable menor que es una variable booleana que guarda True si el la posision del carro 
		# es menor al limite suerior
		# ahora bien  tambien revisa si el carro esta es mayor al limite inferior que es cero y se guarda
		# en la variable mayor que toma True si la posicion del carro esta adentro y False si ha sobrepasado 
		# El limite inferior ahora si se cumple que el la posicion es mas grande que el limite inferior 
		# pero menor que el limite superior entonces retorna true
		# eso ultimo se considera en la linea return menor and mayor
		menor = carro.proxima_posicion()[0] < self.tamano_mapa["x"] and carro.proxima_posicion()[1] < self.tamano_mapa["y"]
		mayor = carro.proxima_posicion()[0] > 0 and carro.proxima_posicion()[1] > 0
		return menor and mayor
	def condiciones_carros(self):
		# Este metodo se encarga de controlar las condiciones de frenado de los carros 
		# Basicamente recorre la lista de carros y si la velocidad es menor que la rapidez maxima esta aumenta la velocidad en 1
		# Ademas, en la segunda condicion se evalua la probabilidad de reducir la velocidad en 1 
		for carro in self.carros:
			if carro.rapidez<self.rapidez_max:
				velocidad_m = [carro.velocidad[0]+carro.direccion[0],carro.velocidad[1]+carro.direccion[1]]
				repidez = int(sqrt(velocidad_m[0]**2+velocidad_m[1]**2))
				carro.velocidad = velocidad_m
				carro.rapidez = repidez
				self.condiciones_semaforos(carro)
			if random()<self.probabilidad_frenar and carro.rapidez>0:
				velocidad_m = [carro.velocidad[0]-carro.direccion[0],carro.velocidad[1]-carro.direccion[1]]
				repidez = int(sqrt(velocidad_m[0]**2+velocidad_m[1]**2))
				carro.velocidad = velocidad_m
				carro.rapidez = repidez
	def actualizar_semaforo(self,estado_semaforos):
		#Esta funcion es unicamente para actualizar el estado de la matris carros_A
		# que es la que se ploteara y esta debe llevar tambien los semaforos actualizados 
		# por lo que en cada fotograma se llama a esta funcion para que apartir del estado 
		#de los semaforos se establezca los valores correspondientes a cada color 
		self.estado_semaforos = estado_semaforos
		mx2 = int(self.tamano_mapa["x"]/2)
		my2 = int(self.tamano_mapa["y"]/2)
		if estado_semaforos[0] == 0:
			self.carros_A[mx2-1-1][my2-2-1:my2-1] = [10,10]
			self.carros_A[mx2-2-1][my2-2-1:my2-1] = [10,10]
		elif estado_semaforos[0] == 2:
			self.carros_A[mx2-1-1][my2-2-1:my2-1] = [41,41]
			self.carros_A[mx2-2-1][my2-2-1:my2-1] = [41,41]
		else:
			self.carros_A[mx2-1-1][my2-2-1:my2-1] = [20,20]
			self.carros_A[mx2-2-1][my2-2-1:my2-1] = [20,20]
			
		if estado_semaforos[1] == 0:
			self.carros_A[mx2-1-1][my2+2+1:my2+4+1] = [10,10]
			self.carros_A[mx2-2-1][my2+2+1:my2+4+1] = [10,10]
		elif estado_semaforos[1] == 2:
			self.carros_A[mx2-1-1][my2+2+1:my2+4+1] = [41,41]
			self.carros_A[mx2-2-1][my2+2+1:my2+4+1] = [41,41]
		else:
			self.carros_A[mx2-1-1][my2+2+1:my2+4+1] = [20,20]
			self.carros_A[mx2-2-1][my2+2+1:my2+4+1] = [20,20]
		if estado_semaforos[2] == 0:
			self.carros_A[mx2+2+1][my2+2+1:my2+4+1] = [10,10]
			self.carros_A[mx2+2+1+1][my2+2+1:my2+4+1] = [10,10]
		elif estado_semaforos[2] ==2:
			self.carros_A[mx2+2+1][my2+2+1:my2+4+1] = [40,40]
			self.carros_A[mx2+2+1+1][my2+2+1:my2+4+1] = [40,40]
		else:
			self.carros_A[mx2+2+1][my2+2+1:my2+4+1] = [20,20]
			self.carros_A[mx2+2+1+1][my2+2+1:my2+4+1] = [20,20]
		if estado_semaforos[3] == 0:
			self.carros_A[mx2+2+1][my2-2-1:my2-1] = [10,10]
			self.carros_A[mx2+2+1+1][my2-2-1:my2-1] = [10,10]
		elif estado_semaforos[3] == 2:
			self.carros_A[mx2+2+1][my2-2-1:my2-1] = [40,40]
			self.carros_A[mx2+2+1+1][my2-2-1:my2-1] = [40,40]
		else:
			self.carros_A[mx2+2+1][my2-2-1:my2-1] = [20,20]
			self.carros_A[mx2+2+1+1][my2-2-1:my2-1] = [20,20]

	def condiciones_semaforos(self,carro):
		# Esta Funcion es la que para el que le llega por el argumento
		# ello verificando si el carro está en la posicion apropiada y si ademas se tiene el semaforo en verde
		#aqui tambien se maneja la condicion de que los carros que van hacia la derecha no deben parar 
		if carro.posicion[0]==int(self.tamano_mapa["x"]/2) and carro.posicion[1]== int(self.tamano_mapa["y"]/2)-2 and (self.estado_semaforos[0]==0 or self.estado_semaforos[0]==2 ): # Condicion Carros que entran por la parte Norte
			if carro.destino != [-1,0]:	 # Aqui se ve que si la direccion no es hacia la derecha entonces el carro se debe detener
				carro.detenerse()
		if carro.posicion[0]==int(self.tamano_mapa["x"]/2)-2 and carro.posicion[1]== int(self.tamano_mapa["y"]/2)+1 and (self.estado_semaforos[1]==0 or self.estado_semaforos[1]==2 ): # Condicion Carros que entran por la parte Oeste 
			if carro.destino != [0,1]:
				carro.detenerse()
		if carro.posicion[0]==int(self.tamano_mapa["x"]/2)+1 and carro.posicion[1]== int(self.tamano_mapa["y"]/2)+3 and (self.estado_semaforos[2]==0 or self.estado_semaforos[2]==2  ): # Condicion Carros que entran por la parte Sur 
			if carro.destino != [1,0]:
				carro.detenerse()
		if carro.posicion[0]==int(self.tamano_mapa["x"]/2)+3 and carro.posicion[1]== int(self.tamano_mapa["y"]/2) and (self.estado_semaforos[3]==0 or self.estado_semaforos[3]==2 ): # Condicion Carros que entran por la parte Este
			if carro.destino != [0,-1]:
				carro.detenerse()
	def condicion_anti_atascos(self,carro):
		# Esta condicion se emplea para que no se produzcan atascos en el caso en que 
		#un carro este ocupando el carril de destino en el cruce este caso se muestra en la imagen (atascos)
		#que se adjunta para los carros que vienen desde el norte y se dirigen al este en ese caso se presenta
		# en ese caso se muestra que el si el carro que viene desde el este va hacia el sur o sigue recto 
		# bloquea al carro que va desde el sur pero este atasco aun es manejable si el carro que viene el carro 
		# que viene desde el norte  y de dirije al este no se mete al cruce, por que si se mete  se bloqeuan todos
		
		x_2 = int(self.tamano_mapa["x"]/2)
		y_2 = int(self.tamano_mapa["y"]/2)
		## Condicion para carros que salen desde el norte
		if carro.posicion == [x_2,y_2-1] and carro.destino==[1,0] and (self.carros_A[x_2+1][y_2] != 0 or self.carros_A[x_2+1][y_2+1]!=0):  
			for carro_cruce in self.carros:
				if carro_cruce.posicion==[x_2+1,y_2] or carro_cruce.posicion == [x_2+1,y_2+1] and carro_cruce.destino==[-1,0]:
					return True
		## Condicion para carros que salen desde el sur
		elif carro.posicion == [x_2+1,y_2+2] and carro.destino==[-1,0] and (self.carros_A[x_2][y_2+1] != 0 or self.carros_A[x_2][y_2] !=0):  
			for carro_cruce in self.carros:
				if carro_cruce.posicion==[x_2,y_2] or carro_cruce.posicion == [x_2,y_2+1] and carro_cruce.destino==[1,0]:
					return True
		## Condicion para carros que salen desde el este
		elif carro.posicion == [x_2+2,y_2] and carro.destino==[0,1] and (self.carros_A[x_2+1][y_2+1] != 0 or self.carros_A[x_2][y_2+1]!=0):  
			for carro_cruce in self.carros:
				if carro_cruce.posicion==[x_2+1,y_2+1] or carro_cruce.posicion == [x_2,y_2+1] and carro_cruce.destino==[0,-1]:
					return True
		## Condicion para carros que salen desde el oeste			
		elif carro.posicion == [x_2-1,y_2+1] and carro.destino==[0,-1] and (self.carros_A[x_2][y_2] != 0 or self.carros_A[x_2+1][y_2]!=0):  
			for carro_cruce in self.carros:
				if carro_cruce.posicion==[x_2,y_2] or carro_cruce.posicion == [x_2+1,y_2] and carro_cruce.destino==[0,1]:
					return True
		
		else:
			return False	
	def calcular_suma_velocidades(self,carro):
		# esta funcion se encarga se sumar las velocidades de carros 
		# para luego poder sacar el promedio de la velocidad y con ello el flujo de vehiculos
		# esta funcion tambien ceenta si el carro pasa por cierta  direccion
		# hay que tener en cuenta que los carros que se consideran son solo los 
		# que aun no han cambiado su direccion
		if carro.salida == [0,1] and carro.salida ==carro.direccion:    #Salida desde el norte
			self.suma_v_norte += carro.rapidez
			self.N_carro_norte += 1
		elif carro.salida == [0,-1] and carro.salida ==carro.direccion :  #Salida desde Sur
			self.suma_v_sur += carro.rapidez
			self.N_carro_sur += 1
		elif carro.salida == [1,0] and carro.salida ==carro.direccion : #Salida Oeste
			self.suma_v_oeste += carro.rapidez
			self.N_carro_oeste += 1
		elif carro.salida ==carro.direccion:
			self.suma_v_este += carro.rapidez
			self.N_carro_este += 1
	def reset_velocidad(self):
		# Este metodo pone todas las velocidades en 0 y el numero de carros en 0
		# esto con el fin de en el nuevo instante calcular nuevamente el flujo
		self.suma_v_norte = 0
		self.suma_v_sur = 0
		self.suma_v_oeste = 0
		self.suma_v_este = 0
		
		self.N_carro_este = 0
		self.N_carro_oeste = 0
		self.N_carro_sur = 0
		self.N_carro_norte = 0
