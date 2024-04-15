from math import sqrt
from random import random
class Vacio:
	def __init__(self,tamano_mapa,rapidez_max,probabilidad_frenar):
		self.rapidez_max=rapidez_max
		self.carros = []
		self.celdas = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])]
		self.carros_A = [[0 for y in range(tamano_mapa["y"])] for x in range(tamano_mapa["x"])]
		self.tamano_mapa = tamano_mapa
		self.probabilidad_frenar=probabilidad_frenar
	def calcular_distancia(self,carro_1,carro_2):
		pass
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

			for m in range(0,carro.rapidez):
				if (self.validar_futura_frontera(carro)):
					if self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]] == 0:
						self.carros_A[carro.proxima_posicion()[0]][carro.proxima_posicion()[1]]=1
						self.carros_A[carro.posicion[0]][carro.posicion[1]]=0
						carro.avanzar()
						
						try:
							for k in range(1,carro.tamano):
								self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=2
								if k+1 == carro.tamano:
									self.carros_A[carro.posicion[0]-(k+1)*carro.direccion[0]][carro.posicion[1]-(k+1)*carro.direccion[1]]=0
						except:
							pass
					else:
						break
				else:
					self.carros_A[carro.posicion[0]][carro.posicion[1]]=0
					for k in range(1,carro.tamano):
							self.carros_A[carro.posicion[0]-k*carro.direccion[0]][carro.posicion[1]-k*carro.direccion[1]]=0
					self.eliminar_carro(carro)
					break
			
				
		return self.carros_A
	def eliminar_carro(self,carro):
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
