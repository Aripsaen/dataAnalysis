import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos preprocesados
data = pd.read_csv('dataAnalysis\datos\csv\london-87490\preprocessed_data.csv')

# Gráfico de barras: Precios promedio por tipo de propiedad
avg_price_by_type = data.groupby('Property Type')['Display Price'].mean()
avg_price_by_type.plot(kind='bar', title='Precio promedio por tipo de propiedad')
plt.xlabel('Tipo de propiedad')
plt.ylabel('Precio promedio')
plt.show()

