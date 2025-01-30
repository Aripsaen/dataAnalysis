import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import random as rd

plt.style.use('seaborn-v0_8-darkgrid')

# Cómo han evolucionado los precios de las propiedades a lo largo del tiempo y cuáles son las tendencias clave observadas en los últimos años?

# Lista de ciudades
ciudades = ["london", "birmingham", "leeds", "sheffield", "manchester", "bradford", "bristol", "coventry", "leicester", "nottingham", "stockport", "kingston-upon-hull", "dudley", "newcastle-upon-tyne", "bolton", "walsall", "plymouth", "sunderland", "milton-keynes", "wolverhampton", "rotherham", "southampton", "derby", "northampton", "stoke-on-trent", "oldham", "reading", "luton", "swindon", "york",
            "portsmouth", "bournemouth", "peterborough", "colchester", "preston", "southend-on-sea", "saint-helens", "norwich", "brighton", "chelmsford", "telford", "huddersfield", "oxford", "middlesbrough", "slough", "poole", "cambridge", "blackpool", "west-bromwich", "exeter", "blackburn", "ipswich", "gloucester", "solihull", "crawley", "basildon", "watford", "eastbourne", "maidstone", "sutton-coldfield", "halifax"]

# Ciudad a analizar (sale una random, luego se puede agregar que un usuario escoja)
ciudad = rd.choice(ciudades)

# Ruta base y archivo de la ciudad
base_path = "datos/json"
city_path = os.path.join(base_path, ciudad, "data.json")

# Ruta para guardar tendencias
save_path = os.path.join("analysis/auxiliary_files/tendencias")
os.makedirs(save_path, exist_ok=True)  # Crear carpeta si no existe

# Cargar datos de la ciudad
try:
    with open(city_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Consolidar transacciones en un DataFrame
    all_data = []
    for property_item in data:
        for transaction in property_item.get('transactions', []):
            all_data.append({
                "dateSold": transaction.get("dateSold"),
                "displayPrice": transaction.get("displayPrice")
            })

    df = pd.DataFrame(all_data)

    # Limpieza de datos
    df['dateSold'] = pd.to_datetime(
        df['dateSold'])  # Convertir a formato fecha
    df['yearSold'] = df['dateSold'].dt.year         # Extraer el año
    df['displayPrice'] = df['displayPrice'].str.replace(
        '£', '').str.replace(',', '').astype(float)  # Limpiar precios

    # Agrupar datos por año y calcular precios promedio
    grouped_data = df.groupby('yearSold')['displayPrice'].mean().reset_index()
    
    # **Guardar los datos en CSV**
    save_file = os.path.join(save_path, f"tendencias_{ciudad}.csv")
    grouped_data.to_csv(save_file, index=False)
    print(f"Datos guardados en: {save_file}")

    # Crear gráfico para la ciudad seleccionada
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_data['yearSold'], grouped_data['displayPrice'],
             marker='o', linestyle='-', color='b')

    # Personalizar el gráfico
    plt.title(f"Evolución de Precios en {ciudad.capitalize()}", fontsize=14)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Precio Promedio (£)", fontsize=12)
    plt.grid()
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

except FileNotFoundError:
    print(f"Archivo no encontrado para la ciudad: {ciudad}")
except Exception as e:
    print(f"Error al procesar los datos: {e}")
