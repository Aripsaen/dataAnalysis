import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# ¿Cuáles son las diferencias en los precios promedio de las propiedades entre las diferentes zonas o barrios?

# Lista de ciudades (misma que en el script de ruby)
ciudades = ["london", "birmingham", "leeds", "sheffield", "manchester", "bradford", "bristol", "coventry", "leicester", "nottingham", "stockport", "kingston-upon-hull", "dudley", "newcastle-upon-tyne", "bolton", "walsall", "plymouth", "sunderland", "milton-keynes", "wolverhampton", "rotherham", "southampton", "derby", "northampton", "stoke-on-trent", "oldham", "reading", "luton", "swindon", "york", "portsmouth", "bournemouth", "peterborough", "colchester", "preston", "southend-on-sea", "saint-helens", "norwich", "brighton", "chelmsford", "telford", "huddersfield", "oxford", "middlesbrough", "slough", "poole", "cambridge", "blackpool", "west-bromwich", "exeter", "blackburn", "ipswich", "gloucester", "solihull", "crawley", "basildon", "watford", "eastbourne", "maidstone", "sutton-coldfield", "halifax"]

# filepath base
base_path = "dataAnalysis/datos/json"

# filepath de salida
output_path = os.path.join("dataAnalysis", "analysis","auxiliary_files", "promedios-por-ciudad.csv")

# Diccionario para almacenar los promedios por ciudad
promedios_por_ciudad = {}


# Iterar sobre cada ciudad
for ciudad in ciudades:
    ciudad_path = os.path.join(base_path, ciudad, "data.json")
    
    try:
        with open(ciudad_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extraer precios para la ciudad
        precios = []
        for property_item in data:
            transactions = property_item.get('transactions', [])
            if transactions and len(transactions) > 0:
                display_price = transactions[0].get('displayPrice', None)
                if display_price:
                    # Limpiar el precio
                    cleaned_price = display_price.replace('£', '').replace(',', '')
                    precios.append(float(cleaned_price))
        
        # Calcular el promedio
        promedio = sum(precios) / len(precios) if precios else 0
        promedios_por_ciudad[ciudad] = promedio
    
    except FileNotFoundError:
        # Manejar el caso de que no exista el archivo para la ciudad
        promedios_por_ciudad[ciudad] = None

# Convertir resultados a un DataFrame y mostrar
df_promedios = pd.DataFrame(list(promedios_por_ciudad.items()), columns=['Ciudad', 'Promedio (£)'])
print(df_promedios)

# Realmente no es necesario guardar ningun archivo
# df_promedios.to_csv("promedios-por-ciudad.csv", index=False)
# os.makedirs(os.path.dirname(output_path), exist_ok=True)  # si no existe sw crea
# df_promedios.to_csv(output_path, index=False)

# print(f"Archivo guardado en: {output_path}")

# Ordenar el DataFrame por el promedio (de mayor a menor)
df_promedios_sorted = df_promedios.sort_values(by="Promedio (£)", ascending=False)

# Seleccionar las 10 ciudades más caras porque si estan todas no entra
top_10_ciudades = df_promedios_sorted.head(10)

# Crear el gráfico de barras
plt.figure(figsize=(12, 8))
plt.barh(top_10_ciudades['Ciudad'], top_10_ciudades['Promedio (£)'], color='skyblue')

# Personalizar el gráfico
plt.xlabel("Precio Promedio (£)", fontsize=12)
plt.ylabel("Ciudad", fontsize=12)
plt.title("Promedio de Precios de Propiedades por Ciudad", fontsize=14)
plt.gca().invert_yaxis()  # Invertir el eje para que la ciudad con mayor promedio esté arriba
plt.tight_layout()

# Mostrar el gráfico
plt.show()