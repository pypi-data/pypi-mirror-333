# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Tuple, Optional, Any
import statsmodels.api as sm

class EVTModel:
    """Modelo de Teoría de Valores Extremos para colas de distribución."""

    def __init__(self, threshold_quantile: float = 0.95):
        """
        Inicializa el modelo EVT.

        Args:
            threshold_quantile: Cuantil para definir valores extremos
        """
        self.threshold_quantile = threshold_quantile
        self.fitted_params: Dict[str, Any] = {}

    def fit(self, returns: pd.Series) -> Dict[str, Any]:
        """
        Ajusta un modelo GPD (Generalized Pareto Distribution) a los valores extremos.

        Args:
            returns: Serie de retornos

        Returns:
            Diccionario con parámetros del modelo
        Raises:
            ValueError: If there are insufficient exceedances to fit the model.
        """
        # Identificar valores extremos en la cola negativa
        threshold = returns.quantile(1 - self.threshold_quantile)
        exceedances = -(returns[returns <= threshold] - threshold)

        if len(exceedances) < 10:
            raise ValueError("Insuficientes valores extremos para ajustar el modelo")

        # Ajustar distribución GPD
        shape, loc, scale = stats.genpareto.fit(exceedances)

        self.fitted_params = {
            "shape": shape,
            "location": loc,
            "scale": scale,
            "threshold": threshold,
            "num_exceedances": len(exceedances),
            "exceedance_rate": len(exceedances) / len(returns)
        }

        return self.fitted_params

    def simulate(self, n_samples: int = 1000) -> np.ndarray:
        """
        Simula valores extremos basados en el modelo ajustado.

        Args:
            n_samples: Número de muestras a generar

        Returns:
            Array de valores extremos simulados
        Raises:
            ValueError: If the model has not been fitted first.
        """
        if not self.fitted_params:
            raise ValueError("El modelo debe ser ajustado primero con fit()")

        shape = self.fitted_params["shape"]
        loc = self.fitted_params["location"]
        scale = self.fitted_params["scale"]
        threshold = self.fitted_params["threshold"]

        # Generar excesos sobre umbral usando GPD
        excesses = stats.genpareto.rvs(shape, loc=loc, scale=scale, size=n_samples)

        # Convertir a retornos
        extreme_returns = -(excesses + threshold)

        return extreme_returns


class CopulaModel:
    """Modelo de cópulas para capturar dependencias no lineales."""

    def __init__(self, copula_type: str = 'gaussian'):
        """
        Inicializa el modelo de cópulas.

        Args:
            copula_type: Tipo de cópula ('gaussian', 't', 'clayton', 'gumbel')
        """
        self.copula_type = copula_type
        self.correlation_matrix: Optional[np.ndarray] = None
        self.df: Optional[float] = None  # Grados de libertad para cópula t
        self.marginals: Dict[str, Any] = {}

    def fit(self, data: pd.DataFrame) -> None:
        """
        Ajusta la cópula a los datos multivariados.

        Args:
            data: DataFrame con retornos multivariados
        Raises:
            TypeError: If data is not a pandas DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data debe ser un pandas DataFrame")

        # 1. Transformar a uniformes mediante CDF empírica
        u_data = pd.DataFrame(index=data.index)

        for col in data.columns:
            # Ajustar distribución marginal (kernel density)
            try:
                kde = sm.nonparametric.KDEUnivariate(data[col].dropna())
                kde.fit()
                self.marginals[col] = kde

                # Transformar a uniforme (0,1)
                ecdf = sm.distributions.ECDF(data[col].dropna())
                u_data[col] = ecdf(data[col])
            except Exception as e:
                print(f"Error fitting marginal for column {col}: {e}")
                continue  # Skip this column if there's an error