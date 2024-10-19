from math import sqrt

"""
Este archivo contiene la clase Carro la cual se encarga de manejar la parte de carros
es decir aqui se enuncia lo que tendra cada uno de los carros, los atributos (carateristicas de cada carro)
son:
* posicion: esta es la posicion del carro, la cual se va modificando por la clase Vacio, a medida que evoluciona el programa 
* velocidad: esta es la velocidad del carro, que tambien se modifica a medida que evoluciona el programa
			 Esta velocida tiene dos componentes una para velocidad en x y otra para velocidad en y 
			 ejemplo si un carro va hacia el sur solo se mueve en el eje 'y' y la velocidad toma el valor [0,-a]
			 en este ejemplo la velocidad en x seria cero es decir no se mueve en el eje x, sin embargo la componente
			 en y es -a por lo que se mueve hacia el sur 
* rapidez: esta es la magnitud de la velocidad
* tamano: contiene el tamaño del carro que en este caso es dos 
* direccion y destino: estos atributos guardan la direccion hacia donde se esta dirigiendo el carro en el instante 
					   y destino es la direccion que tomará una vez se llega al cruce 
		               por ejempo si un carro sale desde el norte y de dirije hacia el oeste la direccion con la que sale es [0,-1] 
		               pero la direccion es [-1,0] por lo que una vez se llega a la celda de desicion la direccion cambia y seria igual al destino 
* salida este simplemente contiene la direccion de donde sale el carro esta nunca cambia y solo es para saber 
		 de donde ha salido un carro una vez ha cambiado la direccion
* tamano_mapa guarda que tan grande es el mapa y aqui se utiliza para calcular la celda de decision 
* celda_decision esta es la celda en la que el carro cambiará de direccion ya que todos los carros cambian 
				 de direccion en diferentes celdas esa se calcula con el método calcular_celda_decision
"""

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
		#Cambia la posicion y lo hace tomand como referencia la posicion alcual
		self.posicion[0] = self.posicion[0]+self.direccion[0]
		self.posicion[1] = self.posicion[1]+self.direccion[1]
	def detenerse(self):
		# Hace que el carro ponga su velocidad en cero
		self.velocidad = [0,0]
		self.rapidez = 0
	def proxima_posicion(self):
		# Retorna la proxima posicion del carro pero sin cambiar la posicion
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
	
   
