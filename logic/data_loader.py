"""
Módulo: Data Loader
Responsabilidad: Cargar y validar el CSV de clientes
"""
import pandas as pd
import os


class DataLoader:
    def __init__(self, csv_path="data/clientes.csv"):
        self.csv_path = csv_path
        self.df = None
        
    def cargar_clientes(self):
        """Carga el CSV y valida columnas requeridas"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV no encontrado en {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        
        # Validar columnas obligatorias
        columnas_requeridas = ['ID', 'Nombre', 'Sector', 'Historial_Compras', 
                               'Gasto_Promedio', 'Riesgo_Abandono']
        
        for col in columnas_requeridas:
            if col not in self.df.columns:
                raise ValueError(f"Columna requerida no encontrada: {col}")
        
        return self.df
    
    def obtener_cliente_por_id(self, cliente_id):
        """Retorna un diccionario con los datos del cliente"""
        if self.df is None:
            self.cargar_clientes()
        
        cliente = self.df[self.df['ID'] == cliente_id]
        
        if cliente.empty:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")
        
        return cliente.iloc[0].to_dict()
    
    def obtener_cliente_por_nombre(self, nombre):
        """Retorna un diccionario con los datos del cliente por nombre"""
        if self.df is None:
            self.cargar_clientes()
        
        cliente = self.df[self.df['Nombre'] == nombre]
        
        if cliente.empty:
            raise ValueError(f"Cliente {nombre} no encontrado")
        
        return cliente.iloc[0].to_dict()
    
    def listar_nombres(self):
        """Retorna lista de nombres para la UI"""
        if self.df is None:
            self.cargar_clientes()
        return self.df['Nombre'].tolist()


# Ejemplo de uso
if __name__ == "__main__":
    loader = DataLoader()
    df = loader.cargar_clientes()
    print("Clientes cargados:", len(df))
    print(loader.obtener_cliente_por_nombre("Carlos Ruiz"))