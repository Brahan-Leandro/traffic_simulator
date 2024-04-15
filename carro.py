from math import sqrt
class Carro:
	def __init__(self,
				 posicion,
				 velocidad,
				 tamano,
				 destino,
				 direccion
				 ):
		self.posicion = posicion
		self.velocidad = velocidad
		self.rapidez = int(sqrt(velocidad[0]**2+velocidad[1]**2))
		self.tamano = tamano 
		self.direccion =direccion
		self.destino = destino
	def avanzar(self): 
		self.posicion[0] = self.posicion[0]+self.direccion[0]
		self.posicion[1] = self.posicion[1]+self.direccion[1]
	def detenerse(self):
		self.velocidad = [0,0]
	def proxima_posicion(self):
		return (self.posicion[0]+self.direccion[0],self.posicion[1]+self.direccion[1])
	def __str__(self):
		return f"1" 
   
