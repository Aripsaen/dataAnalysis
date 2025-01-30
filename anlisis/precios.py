import json
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

# Directorio de datos
path = os.path.join("datos", "json")
cities = os.listdir(path)
cities = [{i: os.path.join(path, i, "data.json")} for i in cities]

# Almacenar los resultados del análisis
city_differences = {}
city_ages = {}
transaction_counts = defaultdict(int)

def clean_price(price):
    """Limpia el precio eliminando caracteres no numéricos y manejando errores."""
    if not isinstance(price, str):
        return 0.0
    cleaned_price = re.sub(r"[^\d.]", "", price)  # Elimina cualquier carácter que no sea número o punto decimal
    return float(cleaned_price) if cleaned_price else 0.0

# Extraer precios, diferencias, antigüedad promedio y contar ventas/compras por año
for city_dict in cities:
    for city, file_path in city_dict.items():
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and data:
                for item in data:
                    transactions = item.get("transactions", [])

                    if transactions:
                        initial_price = clean_price(transactions[0].get("displayPrice", "0"))
                        # initial_price = float(transactions[0].get("displayPrice", "0").replace("\u00a3", "").replace(",", ""))
                        final_price = clean_price(transactions[-1].get("displayPrice", "0"))
                        # final_price = float(transactions[-1].get("displayPrice", "0").replace("\u00a3", "").replace(",", ""))
                        

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
"""
# Ordenar ciudades por diferencia de precio
city_differences_sorted = sorted(zip(cities_list, price_differences), key=lambda x: x[1], reverse=True)

# Solicitar la cantidad de ciudades a mostrar
n = int(input(f"Ingrese la cantidad de ciudades a mostrar (1-{len(cities_list)}): "))
n = max(1, min(n, len(cities_list)))  # Asegurar que esté dentro del rango permitido

# Seleccionar las ciudades top N
top_n_cities = city_differences_sorted[:n]
top_n_city_names = [city[0] for city in top_n_cities]
top_n_price_differences = [city[1] for city in top_n_cities]
top_n_initial_prices = [initial_prices[cities_list.index(city[0])] for city in top_n_cities]
top_n_final_prices = [final_prices[cities_list.index(city[0])] for city in top_n_cities]
top_n_average_ages = [average_ages[cities_list.index(city[0])] for city in top_n_cities]
top_n_transaction_counts = [transaction_counts[city] for city in top_n_city_names]

# Comparación de Precios de Venta por Ciudad (Top N)
fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.25
index = range(len(top_n_city_names))

bar1 = ax.bar(index, top_n_initial_prices, bar_width, label="Venta Inicial", color='blue')
bar2 = ax.bar([i + bar_width for i in index], top_n_final_prices, bar_width, label="Venta Final", color='green')
bar3 = ax.bar([i + 2 * bar_width for i in index], top_n_price_differences, bar_width, label="Diferencia", color='red')

ax.set_xlabel('Ciudad')
ax.set_ylabel('Precio en £')
ax.set_title(f'Comparación de Precios de Venta por Ciudad (Top {n})')
ax.set_xticks([i + bar_width for i in index])
ax.set_xticklabels(top_n_city_names, rotation=45, ha="right")
ax.legend()
plt.tight_layout()
plt.show()

# Antigüedad Promedio (Años)
fig, ax1 = plt.subplots(figsize=(12, 6))
bar4 = ax1.bar(index, top_n_average_ages, bar_width, label="Antigüedad Promedio (Años)", color='orange')
ax1.set_xlabel('Ciudad')
ax1.set_ylabel('Antigüedad Promedio (Años)', color='orange')
ax1.tick_params(axis='y', labelcolor='orange')

ax2 = ax1.twinx()
top_n_price_differences_in_thousands = [price / 1000 for price in top_n_price_differences]
bar5 = ax2.bar([i + bar_width for i in index], top_n_price_differences_in_thousands, bar_width, label="Diferencia de Precio (£) en Miles", color='purple')
ax2.set_ylabel('Diferencia de Precio (£) en Miles', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')
ax1.set_xticks([i + bar_width for i in index])
ax1.set_xticklabels(top_n_city_names, rotation=45, ha="right")
ax1.set_title(f'Antigüedad Promedio y Diferencia de Precio por Ciudad (Top {n})')
plt.tight_layout()
plt.show()

# Número de Transacciones Inmobiliarias por Ciudad (Top N)
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(top_n_city_names, top_n_transaction_counts, color='skyblue')
ax.set_xlabel('Ciudad')
ax.set_ylabel('Número de Transacciones')
ax.set_title(f'Número de Transacciones Inmobiliarias por Ciudad (Top {n})')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
"""
def obtener_datos():
    # Directorio de datos
    path = os.path.join("datos", "json")
    cities = os.listdir(path)
    cities = [{i: os.path.join(path, i, "data.json")} for i in cities]

    # Almacenar los resultados del análisis
    city_differences = {}
    city_ages = {}
    transaction_counts = defaultdict(int)

    # Extraer datos
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
    cities_list = list(city_differences.keys())
    initial_prices = [sum(values[::3]) / len(values[::3]) for values in city_differences.values()]
    final_prices = [sum(values[1::3]) / len(values[1::3]) for values in city_differences.values()]
    price_differences = [sum(values[2::3]) / len(values[2::3]) for values in city_differences.values()]
    average_ages = [sum(city_ages[city]) / len(city_ages[city]) for city in city_ages]

    # Ordenar ciudades
    city_differences_sorted = sorted(zip(cities_list, price_differences), key=lambda x: x[1], reverse=True)

    return city_differences, city_ages, transaction_counts, cities_list, initial_prices, final_prices, price_differences, average_ages, city_differences_sorted
