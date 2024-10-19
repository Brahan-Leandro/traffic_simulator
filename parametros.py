tamano_mapa = {"x":200, "y":200}
pasos = 100
rapidez_simulacion = 50  # en milisegundos
N_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el norte
S_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el sur
W_densidad = 0.3  		#probabilidad de la cantidad de carros que salen desde el oeste
E_densidad = 0.3		#probabilidad de la cantidad de carros que salen desde el Este

N_E_probabilidad = 0.2   # Probabilidad que un carro que salga del norte se dirija al este
N_W_probabilidad = 0.2   #  Probabilidad que un carro que salga del norte se dirija al oeste
S_E_probabilidad = 0.2   #  Probabilidad que un carro que salga del sur se dirija al este
S_W_probabilidad = 0.2   #  Probabilidad que un carro que salga del norte se dirija al oeste
E_N_probabilidad = 0.2   #  Probabilidad que un carro que salga del este se dirija al norte
E_S_probabilidad = 0.2   #  Probabilidad que un carro que salga del este se dirija al sur
W_N_probabilidad = 0.2   # Probabilidad que un carro que salga del oeste se dirija al norte
W_S_probabilidad = 0.2   #  Probabilidad que un carro que salga del oeste se dirija al sur

N_S_probabilidad = 1-N_E_probabilidad-N_W_probabilidad
S_N_probabilidad = 1-S_E_probabilidad-S_W_probabilidad
E_W_probabilidad = 1-E_S_probabilidad-E_N_probabilidad
W_E_probabilidad = 1- W_N_probabilidad-W_S_probabilidad

tiempo_verde = 60  #20       # Este es el numero de fotogramas que se desea que el semaforo esté en verde
tiempo_amarillo = 4   #3   # numero de fotogramas que se desea que el semaforo este en amarillo 

# la variable modo_semaforos puede tomar dos valores  los cuales son 
# "dos_verde" y "uno_verde" 
# en la opcion dos_verde dos semaforos estaran en verde que era la configuracion del programa de la tesis que se tenia inicialmente
# en la opcion uno_verde solo un semaforo estará en verde y el resto en rojo claramente tiene que irse el semaforo 
# que está en verde seria bueno si algo comentar que apesar de que el flujo es mas bajo en la opcion dos uno verde
# esta opcion no produce atascos y por ello tambien menos posibles accidentes
modo_semaforos = "dos_verde"  
#modo_semaforos = "uno_verde"

p_car_grande = 0.4  # Esta es la probabilidad que un carro cuando se crea sea grande
rapidez_max = 5    # esta es la rapidez maxima que se les permite a los carros
probabilidad_frenar = 0.2  # esta es la probabilidad de frenar en un istante

tamano_car_grande = 2     #esto no se debe cambiar  
medida_de_una_celda = 4.5 # metros
