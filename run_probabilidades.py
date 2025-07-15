from inferencia_probabilidades import ProbabilidadesGiroTipo

ruta_csv = r"C:\Users\BARANDICA\Desktop\traffic_simulator\insumos\conteo_ciclos.csv"
ip = ProbabilidadesGiroTipo(ruta_csv, usar_por_tipo=True)

ip.cargar_datos()       # lee el CSV
ip.procesar_datos()     # hace toda la inferencia interna
params = ip.get_dict_parametros()   # <-- dict listo para usar

print(params)           # opcional para inspeccionar
