from math import sqrt
from random import random
from utilidades import *
class Vacio:
	def __init__(self,tamano_mapa,rapidez_max,probabilidad_frenar,estado_semaforos):
		self.rapidez_max=rapidez_max
		self.carros = []
		self.celdas = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])]
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
	def agregar_celda(self, celda):
		self.celdas[celda.posicion[0]][celda.posicion[1]]=celda
	def calcular_avance(self):
		for carro in self.carros:
			v_x = carro.velocidad[0]
			v_y = carro.velocidad[1]
			a_borrar = []
			carro_eliminado = False
			for m in range(0,carro.rapidez):
				if (self.validar_futura_frontera(carro)):
					if self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]] == 0:
						
						self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=1
						self.carros_A[carro.posicion[0]][carro.posicion[1]]=0
						if carro.tamano > 1:
							a_borrar.append([carro.posicion[0]-carro.direccion[0],carro.posicion[1]-carro.direccion[1]])
							if carro.posicion == carro.celda_decision:
								a_borrar.append([carro.posicion[0]-carro.salida[0],carro.posicion[1]-carro.salida[1]])

						carro.avanzar()
						self.condiciones_semaforos()
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
				
		return self.carros_A
	def eliminar_carro(self,carro):
		for k in range(carro.tamano+2):
			self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=0
		self.carros.remove(carro) 
		
	def validar_futura_frontera(self,carro):
		menor = carro.proxima_posicion()[0] < self.tamano_mapa["x"] and carro.proxima_posicion()[1] < self.tamano_mapa["y"]
		mayor = carro.proxima_posicion()[0] > 0 and carro.proxima_posicion()[1] > 0
		return menor and mayor
	def condiciones_carros(self):
		for carro in self.carros:
			if carro.rapidez<self.rapidez_max:
				velocidad_m = [carro.velocidad[0]+carro.direccion[0],carro.velocidad[1]+carro.direccion[1]]
				repidez = int(sqrt(velocidad_m[0]**2+velocidad_m[1]**2))
				carro.velocidad = velocidad_m
				carro.rapidez = repidez
			if random()<self.probabilidad_frenar and carro.rapidez>0:
				velocidad_m = [carro.velocidad[0]-carro.direccion[0],carro.velocidad[1]-carro.direccion[1]]
				repidez = int(sqrt(velocidad_m[0]**2+velocidad_m[1]**2))
				carro.velocidad = velocidad_m
				carro.rapidez = repidez
	def actualizar_semaforo(self,estado_semaforos):
		self.estado_semaforos = estado_semaforos
	def condiciones_semaforos(self):
		print(self.estado_semaforos)
		for carro in self.carros:
			if carro.posicion[0]==int(self.tamano_mapa["x"]/2) and carro.posicion[1]== int(self.tamano_mapa["y"]/2)-1 and (self.estado_semaforos[0]==0 or self.estado_semaforos[0]==0):
				carro.detenerse()
			if carro.posicion[0]==int(self.tamano_mapa["x"]/2)-1 and carro.posicion[1]== int(self.tamano_mapa["y"]/2)+1 and (self.estado_semaforos[1]==0 or self.estado_semaforos[1]==0):
				carro.detenerse()
			if carro.posicion[0]==int(self.tamano_mapa["x"]/2)+1 and carro.posicion[1]== int(self.tamano_mapa["y"]/2)+2 and (self.estado_semaforos[2]==0 or self.estado_semaforos[2]==0):
				carro.detenerse()
			if carro.posicion[0]==int(self.tamano_mapa["x"]/2)+2 and carro.posicion[1]== int(self.tamano_mapa["y"]/2) and (self.estado_semaforos[3]==0 or self.estado_semaforos[3]==0):
				carro.detenerse()
			 
