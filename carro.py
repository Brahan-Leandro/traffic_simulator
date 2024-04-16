from math import sqrt
class Carro:
	def __init__(self,
				 posicion,
				 velocidad,
				 tamano,
				 destino,
				 direccion,
				 tamano_mapa
				 ):
		self.posicion = posicion
		self.velocidad = velocidad
		self.rapidez = int(sqrt(velocidad[0]**2+velocidad[1]**2))
		self.tamano = tamano 
		self.direccion = direccion
		self.salida = direccion
		self.destino = destino
		self.tamano_mapa = tamano_mapa
		self.celda_decision = self.calcular_celda_decision()
		#self.posicion_ante_desvio = [None,None] 
	def avanzar(self): 
		self.posicion[0] = self.posicion[0]+self.direccion[0]
		self.posicion[1] = self.posicion[1]+self.direccion[1]
	def detenerse(self):
		self.velocidad = [0,0]
		self.rapidez = 0
	def proxima_posicion(self):
		return (self.posicion[0]+self.direccion[0],self.posicion[1]+self.direccion[1])
	def cambiar_direccion(self):
		self.direccion = self.destino
	def calcular_celda_decision(self):
		if self.direccion ==[0,1]: # carros del norte
			if self.destino ==[1,0]: # destino Este
				return [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
				
			elif self.destino==[-1,0]:# destino oeste
				return [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)]
			else:
				self.celda_decision = self.celda_decision = [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
		if self.direccion ==[0,-1]: # carros del sur
			if self.destino ==[1,0]: # destino Este
				return [int(self.tamano_mapa["x"]/2)+1,int(self.tamano_mapa["y"]/2)+1]
			elif self.destino==[-1,0]:# destino oeste
				return [int(self.tamano_mapa["x"]/2)+1,int(self.tamano_mapa["y"]/2)]
			else:
				self.celda_decision = self.celda_decision = [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
		if self.direccion ==[-1,0]: # carros del Este
			if self.destino ==[0,-1]: # destino Norte
				return [int(self.tamano_mapa["x"]/2)+1,int(self.tamano_mapa["y"]/2)]
			elif self.destino==[0,1]:# destino Sur
				return [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)]
			else:
				self.celda_decision = self.celda_decision = [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
		if self.direccion ==[1,0]: # carros del Oeste
			if self.destino ==[0,-1]: # destino Norte
				return [int(self.tamano_mapa["x"]/2)+1,int(self.tamano_mapa["y"]/2)+1]
			elif self.destino==[0,1]:# destino Sur
				return [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
			else:
				self.celda_decision = self.celda_decision = [int(self.tamano_mapa["x"]/2),int(self.tamano_mapa["y"]/2)+1]
	
   
