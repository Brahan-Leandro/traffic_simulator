from utilidades import *
from time import sleep
class Sistema_Semaforos:
	def __init__(self,tiempo_verde,tiempo_amarillo):
		self.tiempo_verde = tiempo_verde
		self.tiempo_amarillo = tiempo_amarillo
		self.longitud = 4*(tiempo_verde+tiempo_amarillo)
		
		self.face_semaforo_NO = zeros(self.longitud)
		self.face_semaforo_SO = zeros(self.longitud)
		self.face_semaforo_SE = zeros(self.longitud)
		self.face_semaforo_NE = zeros(self.longitud)
		self.llenar_valores_semaforos()
		self.estado = self.actualizar_estado(1)
	def llenar_valores_semaforos(self):
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
		self.estado = [self.face_semaforo_NO[int(N%self.longitud)],
					   self.face_semaforo_SO[int(N%self.longitud)],
					   self.face_semaforo_SE[int(N%self.longitud)],
					   self.face_semaforo_NE[int(N%self.longitud)],
					   ]
		



