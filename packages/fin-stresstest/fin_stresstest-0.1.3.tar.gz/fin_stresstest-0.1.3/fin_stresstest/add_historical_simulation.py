# -*- coding: utf-8 -*-

# add_historical_simulation.py
import os
import sys

# Ruta al archivo models.py
models_file = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'fin_stresstest', 'models.py')

# Código para la clase HistoricalSimulation
historical_simulation_code = """

class HistoricalSimulation:
    \"\"\"Modelo de simulación histórica para generación de escenarios.\"\"\"
    
    def __init__(self, returns: pd.DataFrame, window_size: int = 252):
        \"\"\"
        Inicializa el modelo de simulación histórica.
        
        Args:
            returns: DataFrame con retornos históricos
            window_size: Tamaño de la ventana de observación
        \"\"\"
        self.returns = returns
        self.window_size = window_size
        
    def simulate(self, n_scenarios: int = 1000) -> pd.DataFrame:
        \"\"\"
        Genera escenarios basados en remuestreo histórico.
        
        Args:
            n_scenarios: Número de escenarios a generar
            
        Returns:
            DataFrame con escenarios simulados
        \"\"\"
        if len(self.returns) < self.window_size:
            raise ValueError("No hay suficientes datos históricos para la ventana especificada")
            
        scenarios = []
        
        for _ in range(n_scenarios):
            # Seleccionar un índice de inicio aleatorio
            start_idx = np.random.randint(0, len(self.returns) - self.window_size + 1)
            # Extraer la ventana de retornos
            scenario = self.returns.iloc[start_idx:start_idx + self.window_size]
            scenarios.append(scenario)
            
        return pd.concat(scenarios, keys=range(n_scenarios), names=["scenario", "date"])
"""

# Comprobar si existe
if os.path.exists(models_file):
    # Leer el contenido
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Añadir la clase al final
    with open(models_file, 'a') as f:
        f.write(historical_simulation_code)
    
    print("Clase HistoricalSimulation añadida exitosamente a models.py")
else:
    print(f"No se encontró el archivo: {models_file}")