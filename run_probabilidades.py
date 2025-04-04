from inferencia_probabilidades import ProbabilidadesGiroTipo

# Cambia aquí la flag según lo que quieras probar
usar_prob_por_tipo = True

ruta = r"C:\Users\BARANDICA\Desktop\traffic_simulator\insumos\conteo_ciclos.csv"

prob = ProbabilidadesGiroTipo(ruta, usar_por_tipo=usar_prob_por_tipo)
prob.cargar_datos()
prob.procesar_datos()
prob.mostrar_resultados()
prob.generar_bloque_parametros()

