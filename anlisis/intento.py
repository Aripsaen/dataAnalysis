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
transaction_counts = defaultdict(int)

# Extraer precios, diferencias, antigüedad promedio y contar ventas/compras por año
for city_dict in cities:
    for city, file_path in city_dict.items():
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list) and data:
                for item in data:
                    transactions = item.get("transactions", [])

                    if transactions:
                        initial_price = float(transactions[0].get("displayPrice", "0").replace("\u00a3", "").replace(",", ""))
                        final_price = float(transactions[-1].get("displayPrice", "0").replace("\u00a3", "").replace(",", ""))

                        price_difference = final_price - initial_price

                        first_transaction_date = datetime.strptime(transactions[-1].get("dateSold", "01 Jan 1900"), "%d %b %Y")
                        last_transaction_date = datetime.strptime(transactions[0].get("dateSold", "01 Jan 1900"), "%d %b %Y")
                        property_age = (last_transaction_date - first_transaction_date).days / 365.25

                        if city not in city_differences:
                            city_differences[city] = []
                        if city not in city_ages:
                            city_ages[city] = []

                        city_differences[city].append(initial_price)
                        city_differences[city].append(final_price)
                        city_differences[city].append(price_difference)
                        city_ages[city].append(property_age)

                        transaction_counts[city] += len(transactions)

# Preparar los datos para graficar
cities_list = []
initial_prices = []
final_prices = []
price_differences = []
average_ages = []

for city, values in city_differences.items():
    cities_list.append(city)
    initial_prices.append(sum(values[::3]) / len(values[::3]))
    final_prices.append(sum(values[1::3]) / len(values[1::3]))
    price_differences.append(sum(values[2::3]) / len(values[2::3]))
    average_ages.append(sum(city_ages[city]) / len(city_ages[city]))

city_differences_sorted = sorted(zip(cities_list, price_differences), key=lambda x: x[1], reverse=True)
top_10_cities = city_differences_sorted[:10]

top_10_city_names = [city[0] for city in top_10_cities]
top_10_price_differences = [city[1] for city in top_10_cities]
top_10_initial_prices = [initial_prices[cities_list.index(city[0])] for city in top_10_cities]
top_10_final_prices = [final_prices[cities_list.index(city[0])] for city in top_10_cities]
top_10_average_ages = [average_ages[cities_list.index(city[0])] for city in top_10_cities]

fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.25
index = range(len(top_10_city_names))

bar1 = ax.bar(index, top_10_initial_prices, bar_width, label="Venta Inicial", color='blue')
bar2 = ax.bar([i + bar_width for i in index], top_10_final_prices, bar_width, label="Venta Final", color='green')
bar3 = ax.bar([i + 2 * bar_width for i in index], top_10_price_differences, bar_width, label="Diferencia", color='red')

ax.set_xlabel('Ciudad')
ax.set_ylabel('Precio en £')
ax.set_title('Comparación de Precios de Venta por Ciudad (Top 10)')
ax.set_xticks([i + bar_width for i in index])
ax.set_xticklabels(top_10_city_names, rotation=45, ha="right")
ax.legend()
plt.tight_layout()
plt.show()

fig, ax1 = plt.subplots(figsize=(12, 6))
bar4 = ax1.bar(index, top_10_average_ages, bar_width, label="Antigüedad Promedio (Años)", color='orange')
ax1.set_xlabel('Ciudad')
ax1.set_ylabel('Antigüedad Promedio (Años)', color='orange')
ax1.tick_params(axis='y', labelcolor='orange')

ax2 = ax1.twinx()
top_10_price_differences_in_thousands = [price / 1000 for price in top_10_price_differences]
bar5 = ax2.bar([i + bar_width for i in index], top_10_price_differences_in_thousands, bar_width, label="Diferencia de Precio (£) en Miles", color='purple')
ax2.set_ylabel('Diferencia de Precio (£) en Miles', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')
ax1.set_xticks([i + bar_width for i in index])
ax1.set_xticklabels(top_10_city_names, rotation=45, ha="right")
ax1.set_title('Antigüedad Promedio y Diferencia de Precio por Ciudad (Top 10 Ciudades)')
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(12, 6))
top_10_transaction_counts = [transaction_counts[city] for city in top_10_city_names]
ax.bar(top_10_city_names, top_10_transaction_counts, color='skyblue')
ax.set_xlabel('Ciudad')
ax.set_ylabel('Número de Transacciones')
ax.set_title('Número de Transacciones Inmobiliarias por Ciudad (Top 10)')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
