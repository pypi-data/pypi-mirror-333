# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime as dt
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
from scipy import stats
import statsmodels.api as sm
from functools import wraps
import time
import logging
import yfinance as yf

# Configuración de logging
logger = logging.getLogger(__name__)

def timer_decorator(func: Callable) -> Callable:
    """
    Decorador para medir el tiempo de ejecución de una función.
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Función {func.__name__} ejecutada en {execution_time:.4f} segundos")
        return result
    return wrapper

def cargar_datos_yahoo(simbolos: Union[str, List[str]], 
                       periodo: str = '5y', 
                       intervalo: str = '1d',
                       columna: str = 'Adj Close') -> pd.DataFrame:
    """
    Descarga datos históricos de Yahoo Finance.
    
    Args:
        simbolos: Símbolo o lista de símbolos a descargar
        periodo: Período de tiempo ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max')
        intervalo: Intervalo de tiempo ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        columna: Columna de precios a utilizar ('Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume')
        
    Returns:
        DataFrame con los datos históricos de precios
        
    Raises:
        ValueError: Si no se pueden descargar datos para algún símbolo
    """
    if isinstance(simbolos, str):
        simbolos = [simbolos]
    
    logger.info(f"Descargando datos para {len(simbolos)} símbolos: {', '.join(simbolos)}")
    
    try:
        # Descargar datos para todos los símbolos
        data = yf.download(
            tickers=simbolos,
            period=periodo,
            interval=intervalo,
            group_by='ticker',
            auto_adjust=True,
            prepost=False,
            threads=True
        )
        
        # Si solo hay un símbolo, la estructura es diferente
        if len(simbolos) == 1:
            # Renombrar columnas para un solo símbolo
            if columna in data.columns:
                precios = data[columna].to_frame(name=simbolos[0])
            else:
                raise ValueError(f"Columna {columna} no encontrada en los datos")
        else:
            # Para múltiples símbolos, seleccionar la columna especificada para cada uno
            precios = pd.DataFrame()
            for simbolo in simbolos:
                if (simbolo, columna) in data.columns:
                    precios[simbolo] = data[(simbolo, columna)]
                else:
                    logger.warning(f"Datos para {simbolo} no disponibles o columna {columna} no encontrada")
        
        # Verificar si se obtuvieron datos
        if precios.empty:
            raise ValueError("No se pudieron obtener datos para los símbolos proporcionados")
        
        logger.info(f"Datos descargados exitosamente: {precios.shape[0]} filas, {precios.shape[1]} columnas")
        return precios
    
    except Exception as e:
        logger.error(f"Error al descargar datos de Yahoo Finance: {str(e)}")
        raise ValueError(f"Error al descargar datos: {str(e)}")

def calcular_retornos(precios: pd.DataFrame, 
                      metodo: str = 'log', 
                      periodo: int = 1) -> pd.DataFrame:
    """
    Calcula retornos de series de precios.
    
    Args:
        precios: DataFrame con series de precios
        metodo: Método de cálculo ('log' o 'simple')
        periodo: Período para el cálculo de retornos
        
    Returns:
        DataFrame con retornos calculados
    
    Raises:
        ValueError: Si el método no es 'log' o 'simple'
    """
    if metodo.lower() not in ['log', 'simple']:
        raise ValueError("El método debe ser 'log' o 'simple'")
    
    if metodo.lower() == 'log':
        return np.log(precios / precios.shift(periodo))
    else:  # simple
        return precios.pct_change(periods=periodo)

def calcular_var_historico(retornos: pd.Series, 
                           nivel_confianza: float = 0.95,
                           escala_temporal: int = 1) -> float:
    """
    Calcula el Value at Risk (VaR) utilizando simulación histórica.
    
    Args:
        retornos: Serie de retornos
        nivel_confianza: Nivel de confianza para el VaR (entre 0 y 1)
        escala_temporal: Factor para escalar el VaR (días, meses, etc.)
        
    Returns:
        Valor del VaR histórico
    
    Raises:
        ValueError: Si nivel_confianza no está entre 0 y 1
    """
    if not 0 < nivel_confianza < 1:
        raise ValueError("El nivel de confianza debe estar entre 0 y 1")
    
    var = retornos.quantile(1 - nivel_confianza)
    return var * np.sqrt(escala_temporal)

def calcular_expected_shortfall(retornos: pd.Series, 
                                nivel_confianza: float = 0.95,
                                escala_temporal: int = 1) -> float:
    """
    Calcula el Expected Shortfall (o Conditional VaR).
    
    Args:
        retornos: Serie de retornos
        nivel_confianza: Nivel de confianza (entre 0 y 1)
        escala_temporal: Factor para escalar el ES (días, meses, etc.)
        
    Returns:
        Valor del Expected Shortfall
    """
    var = calcular_var_historico(retornos, nivel_confianza)
    es = retornos[retornos <= var].mean()
    return es * np.sqrt(escala_temporal)

def calcular_matriz_covarianza_ewma(retornos: pd.DataFrame, 
                                    lambda_factor: float = 0.94) -> pd.DataFrame:
    """
    Calcula matriz de covarianza utilizando EWMA (Exponentially Weighted Moving Average).
    
    Args:
        retornos: DataFrame con series de retornos
        lambda_factor: Factor de decaimiento (entre 0 y 1)
        
    Returns:
        DataFrame con matriz de covarianza EWMA
    
    Raises:
        ValueError: Si lambda_factor no está entre 0 y 1
    """
    if not 0 < lambda_factor < 1:
        raise ValueError("lambda_factor debe estar entre 0 y 1")
    
    # Calcular pesos
    n = len(retornos)
    weights = np.array([(1 - lambda_factor) * lambda_factor ** i for i in range(n-1, -1, -1)])
    weights /= np.sum(weights)
    
    # Calcular matriz de covarianza ponderada
    weighted_cov = pd.DataFrame(np.zeros((retornos.shape[1], retornos.shape[1])),
                                index=retornos.columns, columns=retornos.columns)
    
    for i, asset_i in enumerate(retornos.columns):
        for j, asset_j in enumerate(retornos.columns):
            weighted_cov.loc[asset_i, asset_j] = np.sum(
                weights * (retornos[asset_i] - retornos[asset_i].mean()) *
                (retornos[asset_j] - retornos[asset_j].mean())
            )
    
    return weighted_cov

def aplicar_escenario_estres(datos_base: pd.DataFrame,
                             reglas_estres: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Aplica reglas de estrés a datos base.
    
    Args:
        datos_base: DataFrame con datos base
        reglas_estres: Diccionario con reglas de estrés por variable
                       Formato: {'variable': {'shock': valor, 'min': valor, 'max': valor}}
        
    Returns:
        DataFrame con datos estresados
    """
    datos_estres = datos_base.copy()
    
    for variable, reglas in reglas_estres.items():
        if variable in datos_base.columns:
            # Aplicar shock
            if 'shock' in reglas:
                datos_estres[variable] *= (1 + reglas['shock'])
            
            # Aplicar límite inferior
            if 'min' in reglas:
                datos_estres[variable] = datos_estres[variable].clip(lower=reglas['min'])
            
            # Aplicar límite superior
            if 'max' in reglas:
                datos_estres[variable] = datos_estres[variable].clip(upper=reglas['max'])
    
    return datos_estres

def calcular_sensibilidades(portfolio: pd.DataFrame,
                            factores_riesgo: pd.DataFrame,
                            valuation_func: Callable,
                            cambio_porcentual: float = 0.01) -> pd.DataFrame:
    """
    Calcula sensibilidades del portafolio a factores de riesgo.
    
    Args:
        portfolio: DataFrame con posiciones del portafolio
        factores_riesgo: DataFrame con factores de riesgo
        valuation_func: Función de valoración del portafolio
        cambio_porcentual: Tamaño del cambio para calcular sensibilidades
        
    Returns:
        DataFrame con sensibilidades calculadas
    """
    # Valor base del portafolio
    valor_base = valuation_func(portfolio, factores_riesgo)
    
    sensibilidades = {}
    
    # Calcular sensibilidad para cada factor
    for factor in factores_riesgo.columns:
        # Crear copia con el factor aumentado
        factores_up = factores_riesgo.copy()
        factores_up[factor] *= (1 + cambio_porcentual)
        
        # Valorar con el factor aumentado
        valor_up = valuation_func(portfolio, factores_up)
        
        # Calcular sensibilidad como cambio porcentual en el valor
        sensibilidad = (valor_up - valor_base) / valor_base / cambio_porcentual
        sensibilidades[factor] = sensibilidad
    
    return pd.DataFrame({
        'factor': list(sensibilidades.keys()),
        'sensitivity': list(sensibilidades.values())
    }).set_index('factor')