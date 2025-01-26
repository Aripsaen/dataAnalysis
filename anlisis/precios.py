import json
from collections import defaultdict
import matplotlib.pyplot as plt
from statistics import mean
from datetime import datetime
import os

# Directorio de datos
path = "datos/json"
cities = os.listdir(path)
cities = [{i: os.path.join(path, i, "data.json")} for i in cities]

# Almacenar los resultados del análisis
city_differences = {}
city_ages = {}
transaction_counts = defaultdict(int)  # Para contar las transacciones por ciudad

# Extraer precios, diferencias, antigüedad promedio y contar ventas/compras por año
for city_dict in cities:
    for city, file_path in city_dict.items():
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Verificar si data es una lista y tomar el primer elemento
            if isinstance(data, list) and data:
                data = data[0]  # Tomar el primer diccionario en la lista
                transactions = data.get("transactions", [])

                # Si hay transacciones, obtener los valores de venta inicial y final
                if transactions:
                    initial_price = float(transactions[0].get("displayPrice", "0").replace("£", "").replace(",", ""))
                    final_price = float(transactions[-1].get("displayPrice", "0").replace("£", "").replace(",", ""))
                    
                    # Calcular la diferencia
                    price_difference = final_price - initial_price

                    # Calcular antigüedad de las propiedades
                    first_transaction_date = datetime.strptime(transactions[-1].get("dateSold", "01 Jan 1900"), "%d %b %Y")
                    last_transaction_date = datetime.strptime(transactions[0].get("dateSold", "01 Jan 1900"), "%d %b %Y")
                    property_age = (last_transaction_date - first_transaction_date).days / 365.25  # Convertir a años
                    
                    # Guardar los resultados por ciudad
                    if city not in city_differences:
                        city_differences[city] = []
                    if city not in city_ages:
                        city_ages[city] = []
                    
                    city_differences[city].append(initial_price)
                    city_differences[city].append(final_price)
                    city_differences[city].append(price_difference)
                    city_ages[city].append(property_age)
                    
                    # Contar transacciones por ciudad (considerando las transacciones por casa)
                    transaction_counts[city] += len(transactions)

# Preparar los datos para graficar
cities_list = []
initial_prices = []
final_prices = []
price_differences = []
average_ages = []

for city, values in city_differences.items():
    cities_list.append(city)
    initial_prices.append(sum(values[::3]) / len(values[::3]))  # Promedio de ventas iniciales
    final_prices.append(sum(values[1::3]) / len(values[1::3]))  # Promedio de ventas finales
    price_differences.append(sum(values[2::3]) / len(values[2::3]))  # Promedio de las diferencias
    average_ages.append(sum(city_ages[city]) / len(city_ages[city]))  # Promedio de antigüedad de las propiedades

# Ordenar las ciudades según la diferencia de precio y seleccionar las 10 más significativas
city_differences_sorted = sorted(zip(cities_list, price_differences), key=lambda x: x[1], reverse=True)
top_10_cities = city_differences_sorted[:10]

# Extraer los datos para las 10 ciudades más significativas
top_10_city_names = [city[0] for city in top_10_cities]
top_10_price_differences = [city[1] for city in top_10_cities]
top_10_initial_prices = [initial_prices[cities_list.index(city[0])] for city in top_10_cities]
top_10_final_prices = [final_prices[cities_list.index(city[0])] for city in top_10_cities]
top_10_average_ages = [average_ages[cities_list.index(city[0])] for city in top_10_cities]

# Crear gráfico de barras con ventas iniciales, finales y diferencias para las 10 ciudades más significativas
fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.25
index = range(len(top_10_city_names))

# Graficar barras de ventas iniciales, finales y diferencias
bar1 = ax.bar(index, top_10_initial_prices, bar_width, label="Venta Inicial", color='blue')
bar2 = ax.bar([i + bar_width for i in index], top_10_final_prices, bar_width, label="Venta Final", color='green')
bar3 = ax.bar([i + 2 * bar_width for i in index], top_10_price_differences, bar_width, label="Diferencia", color='red')

# Etiquetas y título
ax.set_xlabel('Ciudad')
ax.set_ylabel('Precio en £')
ax.set_title('Comparación de Precios de Venta por Ciudad (Top 10)')
ax.set_xticks([i + bar_width for i in index])
ax.set_xticklabels(top_10_city_names, rotation=45, ha="right")

# Agregar leyenda
ax.legend()

# Mostrar el gráfico
plt.tight_layout()
plt.show()

# Crear un gráfico de barras para antigüedad promedio y diferencia de precio con dos ejes y solo para las 10 ciudades más significativas
fig, ax1 = plt.subplots(figsize=(12, 6))

# Graficar barras de antigüedad promedio
bar4 = ax1.bar(index, top_10_average_ages, bar_width, label="Antigüedad Promedio (Años)", color='orange')

# Etiquetas para el primer eje
ax1.set_xlabel('Ciudad')
ax1.set_ylabel('Antigüedad Promedio (Años)', color='orange')
ax1.tick_params(axis='y', labelcolor='orange')

# Crear un segundo eje para la diferencia de precio
ax2 = ax1.twinx()  # Crea un segundo eje
top_10_price_differences_in_thousands = [price / 1000 for price in top_10_price_differences]  # Convertir a miles de £
bar5 = ax2.bar([i + bar_width for i in index], top_10_price_differences_in_thousands, bar_width, label="Diferencia de Precio (£) en Miles", color='purple')

# Etiquetas para el segundo eje
ax2.set_ylabel('Diferencia de Precio (£) en Miles', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

# Etiquetas y título
ax1.set_xticks([i + bar_width for i in index])
ax1.set_xticklabels(top_10_city_names, rotation=45, ha="right")
ax1.set_title('Antigüedad Promedio y Diferencia de Precio por Ciudad (Top 10 Ciudades)')

# Mostrar la leyenda
fig.tight_layout()
plt.show()

# Crear gráfico de barras para el número de transacciones por ciudad (todas las ciudades)
fig, ax = plt.subplots(figsize=(12, 6))

# Graficar las transacciones
ax.bar(transaction_counts.keys(), transaction_counts.values(), color='skyblue')

# Etiquetas y título
ax.set_xlabel('Ciudad')
ax.set_ylabel('Número de Transacciones')
ax.set_title('Número de Transacciones Inmobiliarias por Ciudad (Todas las Ciudades)')

# Rotar etiquetas del eje x para mejor legibilidad
plt.xticks(rotation=45, ha="right")

# Mostrar el gráfico
plt.tight_layout()
plt.show()

print(city_differences)
print(city_ages)
print(transaction_counts)
