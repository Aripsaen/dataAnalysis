import pandas as pd

# Cargar datos
data = pd.read_csv('dataAnalysis/datos/csv/london-87490/data.csv')

# Eliminar duplicados
data = data.drop_duplicates()

# Manejar valores nulos
data = data.fillna({"Bedrooms": 0, "Display Price": "Unknown"})

# Limpieza de 'Display Price' para que no salga el simbolo de libra
data['Display Price'] = (
    data['Display Price']
    .replace('[^\\d.]', '', regex=True)  
    .replace('', '0')                   
    .astype(float)                      
)

# Convertir columnas, por ejemplo, fechas
data['Date Sold'] = pd.to_datetime(data['Date Sold'], errors='coerce')

# Guardar los datos preprocesados
data.to_csv('dataAnalysis/datos/csv/london-87490/preprocessed_data.csv', index=False)

print("Preprocesamiento completado.")


# Calcular dias en el mercado

def calculate_days_on_market(file_path):
    # Cargar datos
    data = pd.read_csv(file_path)

    # Convertir fechas a formato datetime
    data['Date Sold'] = pd.to_datetime(data['Date Sold'], errors='coerce')
    data['Date Published'] = pd.to_datetime(data['Date Published'], errors='coerce')

    # Calcular días en el mercado
    data['Days on Market'] = (data['Date Sold'] - data['Date Published']).dt.days

    # Guardar datos actualizados
    data.to_csv(file_path, index=False)
    print("Días en el mercado calculados y guardados.")

    pass


# Aumento/disminucion de precios

def calculate_price_changes(file_path):
    # Cargar datos
    data = pd.read_csv(file_path)

    # Calcular cambios de precios
    data['Price Change'] = data['Display Price'].diff()

    # Guardar datos actualizados
    data.to_csv(file_path, index=False)
    print("Cambios de precios calculados y guardados.")

    pass

# Precio promedio por zona 

def plot_avg_price_by_zone(file_path):
    # Cargar datos
    data = pd.read_csv(file_path)

    # Agrupar y calcular precio promedio
    avg_price_by_zone = data.groupby('Zone')['Display Price'].mean()

    print("Precio promedio por zona:")
    print(avg_price_by_zone)
