import json
from collections import defaultdict
import matplotlib.pyplot as plt
from statistics import mean
from datetime import datetime

# Cargar datos desde el primer archivo JSON (primera ciudad)
with open('datos/json/london-87490/data.json', 'r') as file:
    data1 = json.load(file)

# Cargar datos desde el segundo archivo JSON (segunda ciudad)
with open('datos/json/southwark-85215/data.json', 'r') as file:
    data2 = json.load(file)

# Combinar los datos en un defaultdict
area_data = defaultdict(list)

# Función para procesar las propiedades y agregar los datos
def process_properties(data):
    for prop in data:
        area = prop["address"].split()[-1][:2]  # Asumiendo que el área está al final de la dirección
        transactions = prop["transactions"]
        
        # Ordenar las transacciones por fecha (más antigua primero)
        transactions.sort(key=lambda t: t["dateSold"])

        # Asegúrate de que haya transacciones antes de proceder
        if transactions:
            # Analizar las fechas con el formato correcto
            date_sold_first = datetime.strptime(transactions[0]["dateSold"], "%d %b %Y")  # Cambiar formato aquí
            date_sold_last = datetime.strptime(transactions[-1]["dateSold"], "%d %b %Y")  # Cambiar formato aquí
            
            # Calcular la antigüedad de la propiedad en años
            property_age = (date_sold_last - date_sold_first).days / 365.25  # Convertir a años
            
            initial_price = int(transactions[0]["displayPrice"].replace("£", "").replace(",", ""))
            final_price = int(transactions[-1]["displayPrice"].replace("£", "").replace(",", ""))
            
            # Agregar al defaultdict
            area_data[area].append({
                "address": prop["address"],
                "initial_price": initial_price,
                "final_price": final_price,
                "price_change": final_price - initial_price,
                "property_age": property_age  # Añadir la antigüedad de la propiedad
            })

# Procesar ambos conjuntos de datos
process_properties(data1)
process_properties(data2)

# Mostrar los resultados    
print(json.dumps(area_data, indent=4))

# Función para calcular estadísticas (promedio, precio más alto, precio más bajo)
def calculate_statistics(area_data):
    area_prices = {}  # Diccionario para almacenar las estadísticas por área

    for area, properties in area_data.items():
        initial_prices = [prop["initial_price"] for prop in properties]
        final_prices = [prop["final_price"] for prop in properties]
        property_ages = [prop["property_age"] for prop in properties]  # Lista de antigüedades de las propiedades

        # Cálculo de las métricas
        avg_initial = mean(initial_prices)
        avg_final = mean(final_prices)
        avg_age = mean(property_ages)  # Promedio de antigüedad
        high_initial = max(initial_prices)
        low_initial = min(initial_prices)
        high_final = max(final_prices)
        low_final = min(final_prices)

        # Guardamos las métricas
        area_prices[area] = {
            "avg_initial": avg_initial,
            "avg_final": avg_final,
            "avg_age": avg_age,  # Guardar el promedio de antigüedad
            "high_initial": high_initial,
            "low_initial": low_initial,
            "high_final": high_final,
            "low_final": low_final
        }

    return area_prices

# Calcular las estadísticas
area_prices = calculate_statistics(area_data)

# Imprimir los resultados en consola
for area, stats in area_prices.items():
    print(f"Área: {area}")
    print(f"Promedio de precio inicial: £{stats['avg_initial']:.2f}")
    print(f"Promedio de precio final: £{stats['avg_final']:.2f}")
    print(f"Promedio de antigüedad de la propiedad: {stats['avg_age']:.2f} años")
    print(f"Precio más alto inicial: £{stats['high_initial']:.2f}")
    print(f"Precio más bajo inicial: £{stats['low_initial']:.2f}")
    print(f"Precio más alto final: £{stats['high_final']:.2f}")
    print(f"Precio más bajo final: £{stats['low_final']:.2f}")
    print("="*50)

# Gráfico de resultados
def plot_statistics(area_prices):
    areas = list(area_prices.keys())
    avg_initial_prices = [area_prices[area]["avg_initial"] for area in areas]
    avg_final_prices = [area_prices[area]["avg_final"] for area in areas]
    avg_ages = [area_prices[area]["avg_age"] for area in areas]  # Promedio de antigüedad

    # Crear la gráfica
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Graficar los precios promedio inicial y final
    ax1.bar(areas, avg_initial_prices, label='Promedio Precio Inicial', alpha=0.6, color='b')
    ax1.bar(areas, avg_final_prices, label='Promedio Precio Final', alpha=0.6, color='g')

    ax1.set_xlabel('Área')
    ax1.set_ylabel('Precio (£)')
    ax1.set_title('Precios de Venta Promedio por Área')

    # Crear un segundo eje y para la antigüedad
    ax2 = ax1.twinx()
    ax2.plot(areas, avg_ages, label='Promedio de Antigüedad', color='r', marker='o', linestyle='--')
    ax2.set_ylabel('Antigüedad Promedio (Años)')

    # Añadir la leyenda
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Mostrar la gráfica
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Mostrar el gráfico
plot_statistics(area_prices)
