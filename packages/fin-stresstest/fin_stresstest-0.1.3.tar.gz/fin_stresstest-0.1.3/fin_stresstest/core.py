# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Callable, Any

class ScenarioGenerator:
    """Genera escenarios de estrés para variables financieras."""

    def __init__(self,
                 historical_data: pd.DataFrame,
                 stress_factor: float = 1.5):
        """
        Inicializa el generador de escenarios.

        Args:
            historical_data: DataFrame con datos históricos
            stress_factor: Factor de estrés para amplificar los movimientos
        Raises:
            TypeError: If historical_data is not a pandas DataFrame.
            ValueError: If the DataFrame is empty.
        """
        self.data = historical_data
        self.stress_factor = stress_factor
        self._validate_data()

    def _validate_data(self):
        """Valida que los datos estén en el formato correcto."""
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("historical_data debe ser un pandas DataFrame")
        if self.data.empty:
            raise ValueError("El DataFrame no puede estar vacío")

    def generate_historical_scenarios(self,
                                      num_scenarios: int = 100,
                                      lookback_window: int = 250) -> pd.DataFrame:
        """
        Genera escenarios basados en periodos históricos estresados.

        Args:
            num_scenarios: Número de escenarios a generar
            lookback_window: Tamaño de la ventana de observación

        Returns:
            DataFrame con los escenarios generados
        Raises:
            ValueError: If lookback_window is larger than the data length.
        """
        if lookback_window > len(self.data):
            raise ValueError("lookback_window cannot be larger than the data length.")

        volatility = self.data.pct_change().std() * np.sqrt(252)
        stressed_volatility = volatility * self.stress_factor

        scenarios: List[pd.DataFrame] = []
        for _ in range(num_scenarios):
            start_idx = np.random.randint(0, len(self.data) - lookback_window)
            window = self.data.iloc[start_idx:start_idx + lookback_window]

            # Ajustar la ventana para reflejar mayor volatilidad
            window_returns = window.pct_change().dropna()
            stressed_returns = window_returns * (stressed_volatility / volatility)

            # Reconstruir los precios con los retornos estresados
            base_value = window.iloc[0]
            scenario = base_value * (1 + stressed_returns).cumprod()
            scenarios.append(scenario)

        return pd.concat(scenarios, keys=range(num_scenarios), names=['scenario', 'date'])


class StressTestEngine:
    """Motor principal para ejecutar pruebas de estrés en portafolios o modelos financieros."""

    def __init__(self,
                 portfolio: pd.DataFrame,
                 risk_factors: List[str],
                 confidence_level: float = 0.95):
        """
        Inicializa el motor de pruebas de estrés.

        Args:
            portfolio: DataFrame con posiciones del portafolio
            risk_factors: Lista de factores de riesgo a considerar
            confidence_level: Nivel de confianza para las métricas de riesgo
        Raises:
            TypeError: If portfolio is not a pandas DataFrame.
            ValueError: If confidence_level is not between 0 and 1.
        """
        if not isinstance(portfolio, pd.DataFrame):
            raise TypeError("portfolio debe ser un pandas DataFrame")
        if not 0 < confidence_level < 1:
            raise ValueError("confidence_level debe estar entre 0 y 1")

        self.portfolio = portfolio
        self.risk_factors = risk_factors
        self.confidence_level = confidence_level
        self.scenarios: Optional[pd.DataFrame] = None
        self.results: Optional[pd.Series] = None

    def run_stress_test(self,
                       scenario_generator: ScenarioGenerator,
                       valuation_function: Callable[[pd.DataFrame, pd.Series], float],
                       num_scenarios: int = 1000) -> Dict[str, float]:
        """
        Ejecuta una prueba de estrés completa.

        Args:
            scenario_generator: Generador de escenarios
            valuation_function: Función para valorar el portafolio
            num_scenarios: Número de escenarios a generar

        Returns:
            Diccionario con métricas de riesgo
        Raises:
            TypeError: If valuation_function is not callable.
        """
        if not callable(valuation_function):
            raise TypeError("valuation_function debe ser una función")

        # Generar escenarios
        self.scenarios = scenario_generator.generate_historical_scenarios(num_scenarios)

        # Valorar el portafolio bajo cada escenario
        valuations: List[float] = []
        for scenario_id in range(num_scenarios):
            scenario_data = self.scenarios.loc[scenario_id]
            try:
                portfolio_value = valuation_function(self.portfolio, scenario_data)
            except Exception as e:
                print(f"Error valuing portfolio in scenario {scenario_id}: {e}")
                portfolio_value = np.nan  # Or handle the error differently
            valuations.append(portfolio_value)

        self.results = pd.Series(valuations)

        # Calcular métricas de riesgo
        var = self._calculate_var()
        es = self._calculate_expected_shortfall()
        worst_case = self.results.min()

        return {
            "VaR": var,
            "Expected_Shortfall": es,
            "Worst_Case": worst_case,
            "Mean_Loss": self.results[self.results < 0].mean() if len(self.results[self.results < 0]) > 0 else 0
        }

    def _calculate_var(self) -> float:
        """Calcula el Value at Risk al nivel de confianza especificado."""
        return self.results.quantile(1 - self.confidence_level)

    def _calculate_expected_shortfall(self) -> float:
        """Calcula el Expected Shortfall (CVaR) al nivel de confianza especificado."""
        var = self._calculate_var()
        return self.results[self.results <= var].mean()