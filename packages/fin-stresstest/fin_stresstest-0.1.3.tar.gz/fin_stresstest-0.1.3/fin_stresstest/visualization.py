# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import matplotlib.dates as mdates
from matplotlib.figure import Figure

def plot_stress_results(results: pd.Series, 
                        confidence_level: float = 0.95,
                        title: str = "Distribución de Resultados del Stress Test",
                        figsize: Tuple[int, int] = (10, 6)) -> Figure:
    """
    Visualiza los resultados de un stress test.
    
    Args:
        results: Serie con los resultados de valoración bajo diferentes escenarios
        confidence_level: Nivel de confianza para cálculo de VaR
        title: Título del gráfico
        figsize: Tamaño de la figura
        
    Returns:
        Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Histograma de resultados
    sns.histplot(results, kde=True, ax=ax, color='skyblue', edgecolor='black')
    
    # Calcular VaR y Expected Shortfall
    var = results.quantile(1 - confidence_level)
    es = results[results <= var].mean()
    
    # Añadir líneas verticales
    ax.axvline(var, color='r', linestyle='--', linewidth=2,
               label=f'VaR {confidence_level*100:.0f}%: {var:.2f}')
    ax.axvline(es, color='darkred', linestyle='-', linewidth=2,
               label=f'Expected Shortfall: {es:.2f}')
    
    # Añadir línea de valor cero para referencia
    ax.axvline(0, color='black', linestyle='-', alpha=0.3)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("Pérdidas y Ganancias", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.legend(frameon=True, fontsize=10)
    
    # Añadir estadísticas en un cuadro de texto
    stats_text = (
        f"Estadísticas:\n"
        f"Media: {results.mean():.2f}\n"
        f"Mediana: {results.median():.2f}\n"
        f"Desv. Estándar: {results.std():.2f}\n"
        f"Mínimo: {results.min():.2f}\n"
        f"Máximo: {results.max():.2f}"
    )
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    plt.tight_layout()
    return fig

def plot_risk_heatmap(risk_factors: pd.DataFrame,
                      correlation: Optional[pd.DataFrame] = None,
                      figsize: Tuple[int, int] = (12, 10),
                      method: str = 'pearson',
                      title: str = "Correlaciones entre Factores de Riesgo") -> Figure:
    """
    Genera un mapa de calor para visualizar correlaciones entre factores de riesgo.
    
    Args:
        risk_factors: DataFrame con factores de riesgo
        correlation: Matriz de correlación opcional. Si es None, se calcula
        figsize: Tamaño de la figura
        method: Método de correlación ('pearson', 'spearman', 'kendall')
        title: Título del gráfico
        
    Returns:
        Figura de matplotlib
    """
    if correlation is None:
        correlation = risk_factors.pct_change().dropna().corr(method=method)
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=figsize)
    
    # Generar el mapa de calor
    mask = np.triu(np.ones_like(correlation, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(correlation, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                annot=True, fmt=".2f", square=True, linewidths=.5, ax=ax, 
                cbar_kws={"shrink": .8})
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Ajustar etiquetas para mejor visibilidad
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    return fig

def plot_scenario_comparison(base_scenario: pd.DataFrame, 
                             stress_scenarios: pd.DataFrame,
                             variable: str,
                             num_scenarios: int = 5,
                             lookback_days: int = 120,
                             title: Optional[str] = None,
                             figsize: Tuple[int, int] = (12, 6)) -> Figure:
    """
    Compara escenarios de estrés con un escenario base para una variable específica.
    
    Args:
        base_scenario: DataFrame con escenario base
        stress_scenarios: DataFrame con escenarios de estrés
        variable: Nombre de la variable a graficar
        num_scenarios: Número de escenarios de estrés a mostrar
        lookback_days: Días de historia para mostrar antes de los escenarios
        title: Título del gráfico (opcional)
        figsize: Tamaño de la figura
        
    Returns:
        Figura de matplotlib
    """
    if variable not in base_scenario.columns or variable not in stress_scenarios.columns:
        raise ValueError(f"Variable '{variable}' no encontrada en los datos")
    
    # Preparar datos
    if lookback_days > len(base_scenario):
        lookback_days = len(base_scenario)
    
    base_data = base_scenario[variable].iloc[-lookback_days:]
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=figsize)
    
    # Graficar escenario base
    ax.plot(base_data.index, base_data.values, 'k-', linewidth=2, label='Escenario Base')
    
    # Seleccionar escenarios aleatorios
    scenario_ids = np.random.choice(stress_scenarios.index.get_level_values(0).unique(), 
                                    min(num_scenarios, len(stress_scenarios.index.get_level_values(0).unique())), 
                                    replace=False)
    
    # Graficar escenarios seleccionados
    for scenario_id in scenario_ids:
        scenario_data = stress_scenarios.loc[scenario_id, variable]
        ax.plot(scenario_data.index, scenario_data.values, 
                linestyle='--', alpha=0.7, 
                label=f'Escenario {scenario_id}')
    
    # Configurar el gráfico
    if title is None:
        title = f'Comparación de Escenarios para {variable}'
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel(variable, fontsize=12)
    
    # Formato de fecha en el eje x
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    ax.legend(loc='best', frameon=True)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_factor_sensitivity(sensitivities: pd.DataFrame,
                            figsize: Tuple[int, int] = (12, 6),
                            title: str = "Sensibilidad a Factores de Riesgo") -> Figure:
    """
    Visualiza la sensibilidad del portafolio a distintos factores de riesgo.
    
    Args:
        sensitivities: DataFrame con factores de riesgo y sus sensibilidades
        figsize: Tamaño de la figura
        title: Título del gráfico
        
    Returns:
        Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Ordenar factores por magnitud de sensibilidad
    sensitivities = sensitivities.sort_values(by='sensitivity', ascending=False)
    
    # Definir colores basados en el valor
    colors = ['green' if x >= 0 else 'red' for x in sensitivities['sensitivity']]
    
    # Crear gráfico de barras horizontales
    bars = ax.barh(sensitivities.index, sensitivities['sensitivity'], color=colors, alpha=0.7)
    
    # Añadir etiquetas de valor
    for bar in bars:
        width = bar.get_width()
        label_x = width + (0.01 * abs(width)) if width < 0 else width - (0.05 * abs(width))
        ax.text(label_x, bar.get_y() + bar.get_height()/2, 
                f'{width:.4f}', va='center', ha='center', 
                color='white' if abs(width) > 0.1 else 'black', fontsize=9)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Sensibilidad (% cambio en valor por 1% cambio en factor)', fontsize=10)
    
    # Añadir línea vertical en cero
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # Añadir grid vertical para facilitar lectura
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig