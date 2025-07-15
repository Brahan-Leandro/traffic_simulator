import pandas as pd
import numpy as np

class ProbabilidadesGiroTipo:
    """
    Calcula la inferencia bayesiana de las probabilidades de giro
    para cada entrada del cruce (Norte, Sur, Este, Oeste) y, de forma
    opcional, diferenciando por tipo de vehículo (Pequeño/Grande).

    Uso típico::
        ip = ProbabilidadesGiroTipo("conteo.csv", usar_por_tipo=True)
        ip.cargar_datos()
        ip.procesar_datos()
        params = ip.get_dict_parametros()  # -> dict listo para la simulación
    """

    # Orden fija de columnas en el CSV
    DIRECCIONES = ("Izquierda", "Recto", "Derecha")

    # Mapea cada combinación (Entrada, Dirección) al nombre de variable
    # usado dentro de la simulación.  El orden interno es (Izq, Recto, Der).
    MAPEOS = {
        "Norte": ("N_W_probabilidad", "N_S_probabilidad", "N_E_probabilidad"),
        "Sur": ("S_E_probabilidad", "S_N_probabilidad", "S_W_probabilidad"),
        "Este": ("E_N_probabilidad", "E_W_probabilidad", "E_S_probabilidad"),
        "Oeste": ("W_S_probabilidad", "W_E_probabilidad", "W_N_probabilidad"),
    }

    def __init__(self, ruta_archivo: str, usar_por_tipo: bool = True) -> None:
        self.ruta = ruta_archivo
        self.usar_por_tipo = usar_por_tipo
        self.datos: pd.DataFrame | None = None
        # Dict[Tuple[Entrada, Tipo] | str, np.ndarray]
        self.resultados: dict = {}

    # ---------------------------------------------------------------------
    # ETL
    # ---------------------------------------------------------------------
    def cargar_datos(self) -> None:
        """Carga el CSV de conteo en memoria."""
        self.datos = pd.read_csv(self.ruta, delimiter=";")

    # ---------------------------------------------------------------------
    # Inferencia
    # ---------------------------------------------------------------------
    def _inferir_probabilidades(self, df_ciclos: pd.DataFrame) -> np.ndarray:
        """Devuelve la media posterior Dirichlet para (Izq, Recto, Der)."""
        alpha_prior = np.ones(3)  # prior uniforme
        conteos = df_ciclos[list(self.DIRECCIONES)].sum().values
        alpha_post = alpha_prior + conteos
        return alpha_post / alpha_post.sum()

    def procesar_datos(self) -> None:
        """Agrupa los datos y rellena ``self.resultados`` con medias."""
        if self.datos is None:
            raise RuntimeError("Debe llamar cargar_datos() primero.")

        agrupadores = ["Entrada", "Tipo"] if self.usar_por_tipo else ["Entrada"]

        for clave, grupo in self.datos.groupby(agrupadores):
            media = self._inferir_probabilidades(grupo)
            self.resultados[clave] = media

    # ---------------------------------------------------------------------
    # API pública
    # ---------------------------------------------------------------------
    def get_dict_parametros(self) -> dict:
        """Devuelve un dict llano para la simulación.

        *Si ``usar_por_tipo`` es ``True``* las claves terminan en
        ``_peq`` o ``_gran``.
        """
        if not self.resultados:
            raise RuntimeError("Debe llamar procesar_datos() primero.")

        plano: dict[str, float] = {}
        for clave, media in self.resultados.items():
            # Desempaca Entrada y Tipo (si aplica)
            if self.usar_por_tipo:
                entrada, tipo = clave
                sufijo = "_peq" if tipo.lower() == "pequeño" else "_gran"
            else:
                entrada = clave  # type: ignore[assignment]
                sufijo = ""

            izq_name, recto_name, der_name = self.MAPEOS[entrada]

            plano[f"{izq_name}{sufijo}"] = float(media[0])
            plano[f"{recto_name}{sufijo}"] = float(media[1])
            plano[f"{der_name}{sufijo}"] = float(media[2])

        return plano
