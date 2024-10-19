from utilidades import *
from time import sleep
"""
# Esta clase controla el sistema de semaforos y funciona independientemente es decir se encarga de calcular 
# como debe funcionar cada semaforos pero lo hace internamente lo unico que cambia el estado a de los semaforos 
# es el metodo actualizar estado 

"""
class Sistema_Semaforos:
	def __init__(self,tiempo_verde,tiempo_amarillo,modo_semaforos):
		self.tiempo_verde = tiempo_verde # este atributo es la cantidad de tiempo en que cada semaforo estará en verde
		self.tiempo_amarillo = tiempo_amarillo # cantidad de tiempo en que el semaforo estará en amarillo
		#m = 2  # Cantida de semaforos infependientes, son 4 semaforos, pero en realidad son 2 que actuande forma independiene
		m = 4 if modo_semaforos == "uno_verde" else 2
		self.longitud = m*(tiempo_verde+tiempo_amarillo) # Esta es la longitud del estado de los semaforos
		self.modo_semaforos=modo_semaforos
		# Las siguientes listas guardan el estado en el que pueden estar los semaforos
		self.face_semaforo_NO = zeros(self.longitud) # semaforo que se encuentra en el noroeste del punto medio del mapa
		self.face_semaforo_SO = zeros(self.longitud) # semaforo que se encuentra en el suroeste del punto medio del mapa
		self.face_semaforo_SE = zeros(self.longitud) # semaforo que se encuentra en el sureste  del punto medio del mapa
		self.face_semaforo_NE = zeros(self.longitud) # semaforo que se encuentra en el nor este del punto medio del mapa
		
		
		self.llenar_valores_semaforos() # sellama a este metodo que llena como estarán configurado los nemaforos
		self.estado = self.actualizar_estado(1) # el atributo estado contiene el estado actual de los semaforos en una lista
		                                        # por ejemplo [1,0,1,0] 
		                                        # en este caso el semaforo del NorOeste está en verde
		                                        # el semaforo del surOeste está en rojo
		                                        # el semaforo del surEste está en Verde
		                                        # el semaforo del norEste está en rojo
		
	def llenar_valores_semaforos(self):
		
		
		if self.modo_semaforos == "dos_verde":
			# Se toma las listas de los semaforos y se las llena por ejempo supongamos que el tiempo verde son 
			# 3 y amarillo son 2  entonces la longitud es 10 y las listas estan llenas de la siguiente forma
			# ello considerando que 0 es rojo 1 es verde  y 2 es amarillo 
			"""
			face_semaforo_NO = [1,1,1,2,2,0,0,0,0,0] 
			face_semaforo_SE = [1,1,1,2,2,0,0,0,0,0]
			face_semaforo_SO = [0,0,0,0,0,1,1,1,2,2]
			face_semaforo_NE = [0,0,0,0,0,1,1,1,2,2]
			"""
			
			#llenar verde
			self.face_semaforo_NO[0:self.tiempo_verde] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NO[self.tiempo_verde:self.tiempo_verde+self.tiempo_amarillo] = twos(self.tiempo_amarillo)
			
			#llenar Verde 
			self.face_semaforo_SE[0:self.tiempo_verde] = ones(self.tiempo_verde) 
			# llenar Amarillo
			self.face_semaforo_SE[self.tiempo_verde:self.tiempo_verde+self.tiempo_amarillo] = twos(self.tiempo_amarillo)
				
			#llenar verde
			self.face_semaforo_SO[self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_SO[2*self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+2*self.tiempo_amarillo] = twos(self.tiempo_amarillo)
				
			#llenar Verde
			self.face_semaforo_NE[self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NE[2*self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+2*self.tiempo_amarillo] = twos(self.tiempo_amarillo)
		if self.modo_semaforos == "uno_verde":
			#llenar verde
			self.face_semaforo_NO[0:self.tiempo_verde] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NO[self.tiempo_verde:self.tiempo_verde+self.tiempo_amarillo] = twos(self.tiempo_amarillo)
			
			#llenar verde
			self.face_semaforo_SO[self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_SO[2*self.tiempo_verde+self.tiempo_amarillo:2*self.tiempo_verde+2*self.tiempo_amarillo] = twos(self.tiempo_amarillo)

			#llenar Verde 
			self.face_semaforo_SE[2*self.tiempo_verde+2*self.tiempo_amarillo:3*self.tiempo_verde+2*self.tiempo_amarillo] = ones(self.tiempo_verde)
			# llenar Amarillo
			self.face_semaforo_SE[3*self.tiempo_verde+2*self.tiempo_amarillo:3*self.tiempo_verde+3*self.tiempo_amarillo] = twos(self.tiempo_amarillo)

			#llenar Verde
			self.face_semaforo_NE[3*self.tiempo_verde+3*self.tiempo_amarillo:4*self.tiempo_verde+3*self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NE[4*self.tiempo_verde+3*self.tiempo_amarillo:4*self.tiempo_verde+4*self.tiempo_amarillo] = twos(self.tiempo_amarillo)

	def actualizar_estado(self,N):
		# Se actualiza el estado de los semaforos pero se hace de una manera particular 
		# para eso hay que entender la operacion %  que se llama modulo que basicamente lo que hace es retornar el resto 
		# de una division por ejemplo 4%2 es 0 ya que 3/2 es 2 y lo que resta es cero  
		# otro ejemplo 5%2 es 1 ya que 5/2 es 2 y lo que resta es 1
		# ahora bien supongamos que tenemos una serie fotogramas del 1 al 10 
		# pero debemos estar rotando el estado de los semaforos  pero supongamos que la longitud de
		# de los posibles estados es 5 entonces no se puede poner simplemente el numero de fotograma
		# para extraer el estado del semaforo por que una vez se llegue a 6 ese estado no está disponible
		# ahora bien para solucionar este problema se considera que la operacion % (modulo) genera numeros de la siguiente forma
		# si el numero N de fotogramas es 10 entonces y si se considera la operacion modulo para una longitud de 3 es
		# lo que producira la operacion 1%3, 2%3,3%3, 4%3, 5%3,6%3 ... 10%3 es
		# [1, 2, 0, 1, 2, 0, 1, 2, 0]
		#por lo que ahora si se está generando numeros que se repiten cada cierto ciclo y se pueden utilizar para extraer 
		# los estados de los semaforos
		self.estado = [self.face_semaforo_NO[int(N%self.longitud)],
					   self.face_semaforo_SO[int(N%self.longitud)],
					   self.face_semaforo_SE[int(N%self.longitud)],
					   self.face_semaforo_NE[int(N%self.longitud)],
					   ]
		




