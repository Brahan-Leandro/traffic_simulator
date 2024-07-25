from math import sqrt
from random import random
from utilidades import *
class Vacio:
	def __init__(self,tamano_mapa,rapidez_max,probabilidad_frenar,estado_semaforos):
		self.rapidez_max=rapidez_max
		self.carros = []
		#self.celdas = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])]
		self.carros_A = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])]
		self.tamano_mapa = tamano_mapa
		self.probabilidad_frenar=probabilidad_frenar
		self.colorear_areas()
		self.estado_semaforos = estado_semaforos
	def colorear_areas(self,):
		for i in range(0,int(self.tamano_mapa["x"]/2)):
			self.carros_A[i][0:int(self.tamano_mapa["y"]/2)]=[7 for z in range(int(self.tamano_mapa["y"]/2))]
			self.carros_A[i][int(self.tamano_mapa["y"]/2)+2:]=[7 for z in range(int(self.tamano_mapa["y"]-(self.tamano_mapa["y"]/2+2)))]
		for i in range(int(self.tamano_mapa["x"]/2)+2,int(self.tamano_mapa["x"])):
			self.carros_A[i][0:int(self.tamano_mapa["y"]/2)]=[7 for z in range(int(self.tamano_mapa["y"]/2))]
			self.carros_A[i][int(self.tamano_mapa["y"]/2)+2:]=[7 for z in range(int(self.tamano_mapa["y"]-(self.tamano_mapa["y"]/2+2)))]
	def agregar_carro(self,carro):
		if self.carros_A[carro.posicion[0]][carro.posicion[1]]==0:
			self.carros.append(carro)
			self.carros_A[carro.posicion[0]][carro.posicion[1]]=1
			return True
		else:
			return False
	#def agregar_celda(self, celda):
	#	self.celdas[celda.posicion[0]][celda.posicion[1]]=celda
	def calcular_avance(self):
		intensidad_norte = 0
		intensidad_sur = 0
		intensidad_este = 0
		intensidad_oeste = 0
		for carro in self.carros:
			v_x = carro.velocidad[0]
			v_y = carro.velocidad[1]
			a_borrar = []
			carro_eliminado = False
			for m in range(0,carro.rapidez):
				# ~ print(self.carros_A[int(self.tamano_mapa["x"]/2+1)][int(self.tamano_mapa["y"]/2)])
				if self.condicion_anti_atascos(carro):
					carro.detenerse()
					break
				if (self.validar_futura_frontera(carro)):
					if self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]] == 0:
						self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=1
						self.carros_A[carro.posicion[0]][carro.posicion[1]]=0
						if carro.tamano > 1:
							self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=8
							a_borrar.append([carro.posicion[0]-carro.direccion[0],carro.posicion[1]-carro.direccion[1]])
							if carro.posicion == carro.celda_decision:
								a_borrar.append([carro.posicion[0]-carro.salida[0],carro.posicion[1]-carro.salida[1]])
						intensidad_norte += self.contar_intensidad(carro,"Norte")
						intensidad_sur += self.contar_intensidad(carro,"Sur")
						intensidad_este += self.contar_intensidad(carro,"Este")
						intensidad_oeste += self.contar_intensidad(carro,"Oeste")
						carro.avanzar()				
						
		
						self.condiciones_semaforos(carro)
						if carro.rapidez == 0:
							break 
						if carro.posicion == carro.celda_decision:
							carro.cambiar_direccion()	
					else:
						break
				else:
					self.eliminar_carro(carro)
					carro_eliminado = True
					break
			try:
				if carro_eliminado != True :
					if carro.posicion == carro.celda_decision:
						for k in range(1,carro.tamano):
							self.carros_A[carro.posicion[0]-k*carro.salida[0]][carro.posicion[1]-k*carro.salida[1]]=8
					else:
						for k in range(1,carro.tamano):
							self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=8
				for borrar in a_borrar:
					self.carros_A[borrar[0]][borrar[1]]=0
			except:
				pass
				
		return self.carros_A,intensidad_norte,intensidad_sur,intensidad_este,intensidad_oeste

	def eliminar_carro(self,carro):
		for k in range(carro.tamano+2):
			self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=0
		self.carros.remove(carro) 
		
	def validar_futura_frontera(self,carro):
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

		# ~ print(estado_semaforos)
	def condiciones_semaforos(self,carro):

		if carro.posicion[0]==int(self.tamano_mapa["x"]/2) and carro.posicion[1]== int(self.tamano_mapa["y"]/2)-2 and (self.estado_semaforos[0]==0 or self.estado_semaforos[0]==2 ): # Condicion Carros que entran por la parte Norte
			if carro.destino != [-1,0]:	
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
	def contar_intensidad(self,carro,proviene):
		x_2 = int(self.tamano_mapa["x"]/2)
		y_2 = int(self.tamano_mapa["y"]/2)
		if proviene == "Norte" and  carro.posicion == [x_2,y_2-3]:
			return 1
		elif proviene == "Sur" and carro.posicion == [x_2+1,y_2+4]:
			return 1
		elif  proviene == "Este" and carro.posicion == [x_2+4,y_2]:
			return 1
		elif  proviene == "Oeste" and carro.posicion == [x_2-3,y_2+1]:
			return 1
			
		return 0
