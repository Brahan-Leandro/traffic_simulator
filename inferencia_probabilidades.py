import pandas as pd
import numpy as np
from typing import Dict, Tuple

class ProbabilidadesGiroTipo:
    """Inferencia bayesiana de probabilidades de giro (opcionalmente diferenciadas
    por tipo de vehículo) **y** cálculo de las probabilidades de llegada (densidad)
    por entrada a partir de un archivo CSV de conteo.

    El CSV debe contener, como mínimo, las columnas:
        Entrada  |  Ciclo  |  Tipo  |  Izquierda  |  Recto  |  Derecha

    * ``Entrada``  ∈ {"Norte", "Sur", "Este", "Oeste"}
    * ``Ciclo``    identifica el periodo de observación (se usa para contar ciclos)
    * ``Tipo``     (Pequeño / Grande) – se ignora si *usar_por_tipo* es *False*

    Uso típico
    ----------
    ```python
    ip = ProbabilidadesGiroTipo("conteo_ciclos.csv", usar_por_tipo=True)
    ip.cargar_datos()
    ip.procesar_datos()          # calcula probabilidades de giro

    dict_giros      = ip.get_dict_parametros()           # 24 claves *_probabilidad_*
    dict_densidades = ip.get_dict_densidades(60)         # 4 claves *_densidad
    ```
    """

    def __init__(self, ruta_archivo: str, usar_por_tipo: bool = True):
        self.ruta = ruta_archivo
        self.usar_por_tipo = usar_por_tipo
        self.datos: pd.DataFrame | None = None
        # Probabilidades de giro – se llenan en procesar_datos()
        self.resultados: Dict[Tuple[str, str] | str, Dict[str, object]] = {}

    # ---------------------------------------------------------------------
    # Carga y pre‑procesamiento de datos
    # ---------------------------------------------------------------------
    def cargar_datos(self) -> None:
        """Lee el CSV y lo deja en ``self.datos``."""
        self.datos = pd.read_csv(self.ruta, delimiter=";")

    # ---------------------------------------------------------------------
    # ---  Probabilidades de giro  ----------------------------------------
    # ---------------------------------------------------------------------
    def _inferir_probabilidades(self, df_ciclos: pd.DataFrame) -> Tuple[np.ndarray, Dict[str, Tuple[float, float]]]:
        """Devuelve (media, intervalos) del Dirichlet posterior para un subconjunto."""
        alpha_prior = np.array([1.0, 1.0, 1.0])  # dirichlet(1,1,1) = uniforme
        conteos = df_ciclos[["Izquierda", "Recto", "Derecha"]].sum().values
        alpha_post = alpha_prior + conteos
        media = alpha_post / alpha_post.sum()

        # IC 95 % solo si se necesita para depurar
        muestras = np.random.dirichlet(alpha_post, size=5000)
        intervalos = {
            dir_: (np.percentile(muestras[:, i], 2.5), np.percentile(muestras[:, i], 97.5))
            for i, dir_ in enumerate(["Izquierda", "Recto", "Derecha"])
        }
        return media, intervalos

    def procesar_datos(self) -> None:
        """Agrupa datos y calcula medias posteriores de giro."""
        if self.datos is None:
            raise RuntimeError("Debe llamar a cargar_datos() primero")

        # Elegir columnas de agrupamiento
        if self.usar_por_tipo:
            agrupamiento = ["Entrada", "Tipo"]
        else:
            agrupamiento = ["Entrada"]
            if "Tipo" in self.datos.columns:
                self.datos = self.datos.drop(columns=["Tipo"])

        for clave, grupo in self.datos.groupby(agrupamiento):
            media, intervalos = self._inferir_probabilidades(grupo)
            self.resultados[clave] = {"Media": media, "Intervalos": intervalos}

    def get_dict_parametros(self) -> Dict[str, float]:
        """Devuelve un ``dict`` con las medias de giro, listo para *globals().update()*."""
        plano: Dict[str, float] = {}
        for clave, datos in self.resultados.items():
            if self.usar_por_tipo:
                entrada, tipo = clave
                tag = "peq" if tipo.lower() == "pequeño" else "gran"
            else:
                entrada = clave if isinstance(clave, str) else clave[0]
                tag = ""

            media = datos["Media"]  # [Izq, Recto, Der]

            def set_prob(prefix: str, values: Tuple[float, float, float]):
                izquierda, recto, derecha = values
                if tag:
                    plano[f"{prefix}_W_probabilidad_{tag}"] = izquierda  # Izq
                    plano[f"{prefix}_S_probabilidad_{tag}"] = recto      # Recto (frente)
                    plano[f"{prefix}_E_probabilidad_{tag}"] = derecha    # Der (a la derecha)
                else:
                    plano[f"{prefix}_W_probabilidad"] = izquierda
                    plano[f"{prefix}_S_probabilidad"] = recto
                    plano[f"{prefix}_E_probabilidad"] = derecha

            if entrada == "Norte":
                set_prob("N", (media[0], media[1], media[2]))
            elif entrada == "Sur":
                if tag:
                    plano[f"S_E_probabilidad_{tag}"] = media[0]   # Izquierda → Este
                    plano[f"S_N_probabilidad_{tag}"] = media[1]   # Recto → Norte
                    plano[f"S_W_probabilidad_{tag}"] = media[2]   # Derecha → Oeste
                else:
                    plano["S_E_probabilidad"] = media[0]
                    plano["S_N_probabilidad"] = media[1]
                    plano["S_W_probabilidad"] = media[2]
            elif entrada == "Este":
                # Desde Este: Izq = hacia Norte, Der = hacia Sur
                if tag:
                    plano[f"E_N_probabilidad_{tag}"] = media[0]
                    plano[f"E_W_probabilidad_{tag}"] = media[1]
                    plano[f"E_S_probabilidad_{tag}"] = media[2]
                else:
                    plano[f"E_N_probabilidad"] = media[0]
                    plano[f"E_W_probabilidad"] = media[1]
                    plano[f"E_S_probabilidad"] = media[2]
            elif entrada == "Oeste":
                if tag:
                    plano[f"W_S_probabilidad_{tag}"] = media[0]
                    plano[f"W_E_probabilidad_{tag}"] = media[1]
                    plano[f"W_N_probabilidad_{tag}"] = media[2]
                else:
                    plano[f"W_S_probabilidad"] = media[0]
                    plano[f"W_E_probabilidad"] = media[1]
                    plano[f"W_N_probabilidad"] = media[2]
        return plano

    # ---------------------------------------------------------------------
    # ---  Densidades de llegada  -----------------------------------------
    # ---------------------------------------------------------------------
    def get_dict_densidades(self, T_ciclo_real: float) -> Dict[str, float]:
        """Calcula y devuelve las probabilidades de llegada por tick (1 s) para
        cada entrada.

        Parámetros
        ----------
        T_ciclo_real : float
            Duración en segundos del intervalo que denominaste «ciclo» en el CSV
            (en tu caso, 60 s = duración del verde).
        """
        if self.datos is None:
            raise RuntimeError("Debe cargar los datos primero")
        if "Entrada" not in self.datos.columns:
            raise ValueError("El CSV debe contener la columna 'Entrada'")
        if "Ciclo" not in self.datos.columns:
            raise ValueError("El CSV debe contener la columna 'Ciclo'")

        n_ciclos = self.datos["Ciclo"].nunique()
        if n_ciclos == 0:
            raise ValueError("No se hallaron ciclos en los datos")
        T_obs = n_ciclos * T_ciclo_real  # segundos reales cubiertos por el CSV

        # Total vehículos por entrada (sin discriminar tipo)
        self.datos["Total"] = self.datos[["Izquierda", "Recto", "Derecha"]].sum(axis=1)
        totales = self.datos.groupby("Entrada")["Total"].sum()

        factor = 1.0 / T_obs  #   1 / 540  en tu caso
        densidades = {
            "N_densidad": float(min(1.0, totales.get("Norte", 0) * factor)),
            "S_densidad": float(min(1.0, totales.get("Sur",   0) * factor)),
            "E_densidad": float(min(1.0, totales.get("Este",  0) * factor)),
            "W_densidad": float(min(1.0, totales.get("Oeste", 0) * factor)),
        }
        return densidades
