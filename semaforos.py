from utilidades import *
from time import sleep
class Sistema_Semaforos:
	def __init__(self,tiempo_verde,tiempo_amarillo,modo_semaforos):
		self.tiempo_verde = tiempo_verde
		self.tiempo_amarillo = tiempo_amarillo
		#m = 4 if modo_semaforos == "uno_verde" else 2
		m = 2
		self.tiempo_muerto = 0
		self.longitud = m*(tiempo_verde+self.tiempo_muerto+tiempo_amarillo)
		
		self.face_semaforo_NO = zeros(self.longitud)
		self.face_semaforo_SO = zeros(self.longitud)
		self.face_semaforo_SE = zeros(self.longitud)
		self.face_semaforo_NE = zeros(self.longitud)
		self.modo_semaforos = modo_semaforos
		self.llenar_valores_semaforos()
		self.estado = self.actualizar_estado(1)
		
	def llenar_valores_semaforos(self):
		if self.modo_semaforos == "dos_verde":
			#llenar verde
			self.face_semaforo_NO[0:self.tiempo_verde] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NO[self.tiempo_verde:self.tiempo_verde+self.tiempo_amarillo] = twos(self.tiempo_amarillo)
		
			#llenar Verde 
			self.face_semaforo_SE[0:self.tiempo_verde] = ones(self.tiempo_verde) 
			# llenar Amarillo
			self.face_semaforo_SE[self.tiempo_verde:self.tiempo_verde+self.tiempo_amarillo] = twos(self.tiempo_amarillo)
			
			#llenar verde
			self.face_semaforo_SO[self.tiempo_verde+self.tiempo_amarillo+self.tiempo_muerto:2*self.tiempo_verde+self.tiempo_muerto+self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_SO[2*self.tiempo_verde+self.tiempo_muerto+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_muerto+2*self.tiempo_amarillo] = twos(self.tiempo_amarillo)
			
			#llenar Verde
			self.face_semaforo_NE[self.tiempo_verde+self.tiempo_muerto+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_muerto+self.tiempo_amarillo] = ones(self.tiempo_verde)
			#llenar amarillo
			self.face_semaforo_NE[2*self.tiempo_verde+self.tiempo_muerto+self.tiempo_amarillo:2*self.tiempo_verde+self.tiempo_muerto+2*self.tiempo_amarillo] = twos(self.tiempo_amarillo)

	def actualizar_estado(self,N):
		self.estado = [self.face_semaforo_NO[int(N%self.longitud)],
					   self.face_semaforo_SO[int(N%self.longitud)],
					   self.face_semaforo_SE[int(N%self.longitud)],
					   self.face_semaforo_NE[int(N%self.longitud)],
					   ]
		

if __name__=="__main__":
	S = Sistema_Semaforos(10,7,"dos_verde")
	print(S.face_semaforo_NO)
	print(S.face_semaforo_NE)



