import pandas as pd
import numpy as np
from scipy.stats import dirichlet

class ProbabilidadesGiroTipo:
    """
    Clase para calcular la inferencia bayesiana de las probabilidades de giro,
    diferenciadas por tipo de vehículo (Pequeño, Grande) o no diferenciadas.
    """

    def __init__(self, ruta_archivo, usar_por_tipo=True):
        """
        Inicializa la clase con la ruta del archivo CSV de conteo.
        """
        self.ruta = ruta_archivo
        self.usar_por_tipo = usar_por_tipo
        self.datos = None
        self.resultados = {}

    def cargar_datos(self):
        """
        Carga los datos del archivo CSV.
        """
        try:
            self.datos = pd.read_csv(self.ruta, delimiter=';')
            print(f"Datos cargados correctamente desde {self.ruta}")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")

    def inferir_probabilidades(self, df_ciclos):
        """
        Realiza inferencia bayesiana para un subconjunto de datos de ciclos.
        """
        alpha_prior = np.array([1, 1, 1])
        conteos = df_ciclos[["Izquierda", "Recto", "Derecha"]].sum().values
        alpha_post = alpha_prior + conteos

        muestras = np.random.dirichlet(alpha_post, size=5000)
        media = alpha_post / np.sum(alpha_post)

        intervalos = {}
        for i, direccion in enumerate(["Izquierda", "Recto", "Derecha"]):
            lower = np.percentile(muestras[:, i], 2.5)
            upper = np.percentile(muestras[:, i], 97.5)
            intervalos[direccion] = (lower, upper)

        return media, intervalos

    def procesar_datos(self):
        """
        Procesa los datos y calcula las probabilidades por entrada y tipo de vehículo.
        """
        if self.datos is None:
            print("Datos no cargados.")
            return

        if self.usar_por_tipo:
            agrupamiento = ["Entrada", "Tipo"]
        else:
            # Eliminar columna Tipo para no afectar agrupamiento
            if "Tipo" in self.datos.columns:
                self.datos = self.datos.drop(columns=["Tipo"])
            agrupamiento = ["Entrada"]

        for clave, grupo in self.datos.groupby(agrupamiento):
            media, intervalos = self.inferir_probabilidades(grupo)
            self.resultados[clave] = {
                "Media": media,
                "Intervalos": intervalos
            }

    def mostrar_resultados(self):
        """
        Muestra los resultados de la inferencia.
        """
        for clave, datos in self.resultados.items():
            if self.usar_por_tipo:
                entrada, tipo = clave
                print(f"\nEntrada: {entrada} | Tipo: {tipo}")
            else:
                entrada = clave[0] if isinstance(clave, tuple) else clave
                print(f"\nEntrada: {entrada}")

            print(f"Media posterior:")
            print(f"Izquierda: {datos['Media'][0]:.3f}")
            print(f"Recto: {datos['Media'][1]:.3f}")
            print(f"Derecha: {datos['Media'][2]:.3f}")
            print("Intervalos de credibilidad al 95%:")
            for direccion, (lower, upper) in datos["Intervalos"].items():
                print(f"{direccion}: [{lower:.3f}, {upper:.3f}]")

    def generar_bloque_parametros(self):
        """
        Genera el bloque de código para pegar en parametros.py
        """
        print("\n# Bloque para parametros.py\n")
        for clave, datos in self.resultados.items():
            if self.usar_por_tipo:
                entrada, tipo = clave
                tipo_tag = "peq" if tipo.lower() == "pequeño" else "gran"
            else:
                entrada = clave[0] if isinstance(clave, tuple) else clave
                tipo_tag = None

            media = datos['Media']

            print(f"# Entrada: {entrada}")
            if entrada == "Norte":
                if tipo_tag:
                    print(f"N_W_probabilidad_{tipo_tag} = {media[0]:.3f}")
                    print(f"N_E_probabilidad_{tipo_tag} = {media[2]:.3f}")
                    print(f"N_S_probabilidad_{tipo_tag} = {media[1]:.3f}\n")
                else:
                    print(f"N_W_probabilidad = {media[0]:.3f}")
                    print(f"N_E_probabilidad = {media[2]:.3f}")
                    print(f"N_S_probabilidad = {media[1]:.3f}\n")
            elif entrada == "Sur":
                if tipo_tag:
                    print(f"S_E_probabilidad_{tipo_tag} = {media[0]:.3f}")
                    print(f"S_W_probabilidad_{tipo_tag} = {media[2]:.3f}")
                    print(f"S_N_probabilidad_{tipo_tag} = {media[1]:.3f}\n")
                else:
                    print(f"S_E_probabilidad = {media[0]:.3f}")
                    print(f"S_W_probabilidad = {media[2]:.3f}")
                    print(f"S_N_probabilidad = {media[1]:.3f}\n")
            elif entrada == "Este":
                if tipo_tag:
                    print(f"E_N_probabilidad_{tipo_tag} = {media[0]:.3f}")
                    print(f"E_S_probabilidad_{tipo_tag} = {media[2]:.3f}")
                    print(f"E_W_probabilidad_{tipo_tag} = {media[1]:.3f}\n")
                else:
                    print(f"E_N_probabilidad = {media[0]:.3f}")
                    print(f"E_S_probabilidad = {media[2]:.3f}")
                    print(f"E_W_probabilidad = {media[1]:.3f}\n")
            elif entrada == "Oeste":
                if tipo_tag:
                    print(f"W_S_probabilidad_{tipo_tag} = {media[0]:.3f}")
                    print(f"W_N_probabilidad_{tipo_tag} = {media[2]:.3f}")
                    print(f"W_E_probabilidad_{tipo_tag} = {media[1]:.3f}\n")
                else:
                    print(f"W_S_probabilidad = {media[0]:.3f}")
                    print(f"W_N_probabilidad = {media[2]:.3f}")
                    print(f"W_E_probabilidad = {media[1]:.3f}\n")
