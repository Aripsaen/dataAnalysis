import os
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm

plt.style.use('seaborn-v0_8-darkgrid')

# Lista de ciudades a analizar
ciudades = ["london", "birmingham", "leeds", "sheffield", "manchester", "bradford", "bristol", "coventry", "leicester", "nottingham", "stockport", "kingston-upon-hull", "dudley", "newcastle-upon-tyne", "bolton", "walsall", "plymouth", "sunderland", "milton-keynes", "wolverhampton", "rotherham", "southampton", "derby", "northampton", "stoke-on-trent", "oldham", "reading", "luton", "swindon", "york", "portsmouth", "bournemouth", "peterborough", "colchester", "preston", "southend-on-sea", "saint-helens", "norwich", "brighton", "chelmsford", "telford", "huddersfield", "oxford", "middlesbrough", "slough", "poole", "cambridge", "blackpool", "west-bromwich", "exeter", "blackburn", "ipswich", "gloucester", "solihull", "crawley", "basildon", "watford", "eastbourne", "maidstone", "sutton-coldfield", "halifax"]


# Ruta base de los archivos JSON
base_path = "datos/json"

# filepath de salida
output_path = os.path.join("analysis", "auxiliary_files", "propiedades_procesadas.csv")

# Obtener el año actual
current_year = datetime.datetime.now().year

# Lista para almacenar los datos procesados
data_list = []

# Iterar sobre cada ciudad
for ciudad in ciudades:
    ciudad_path = os.path.join(base_path, ciudad, "data.json")

    try:
        with open(ciudad_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extraer datos relevantes de cada propiedad
        for property_item in data:
            property_type = property_item.get('propertyType', None)
            transactions = property_item.get('transactions', [])

            if transactions:
                # Ordenar transacciones por fecha (de más antigua a más reciente)
                transactions_sorted = sorted(transactions, key=lambda x: x['dateSold'])
                
                # Obtener el año de la transacción más antigua
                oldest_year = int(transactions_sorted[0]['dateSold'][-4:])
                property_age = current_year - oldest_year  # Calcular antigüedad

                # Obtener el precio más reciente
                latest_price = transactions_sorted[-1]['displayPrice']
                latest_price = float(latest_price.replace("£", "").replace(",", ""))  # Convertir a número
                
                # Agregar datos a la lista
                data_list.append({
                    "Ciudad": ciudad,
                    "TipoPropiedad": property_type,
                    "Antigüedad": property_age,
                    "PrecioReciente": latest_price
                })

    except FileNotFoundError:
        print(f"Archivo no encontrado para la ciudad: {ciudad}")

# Convertir la lista en un DataFrame de Pandas
# Convertir a DataFrame
df = pd.DataFrame(data_list)

# Guardar en CSV para análisis posterior

# df.to_csv("propiedades_procesadas.csv", index=False)

# df.to_csv("propiedades_procesadas.csv", index=False)
# os.makedirs(os.path.dirname(output_path), exist_ok=True)  # si no existe sw crea
# df.to_csv(output_path, index=False)

# print(f"Archivo guardado en: {output_path}")

# Función para clasificar la relación según el valor de R^2
def interpretar_r2(r2_value):
    if r2_value > 0.7:
        return "Relación fuerte"
    elif 0.5 < r2_value <= 0.7:
        return "Relación moderada"
    elif 0.3 < r2_value <= 0.5:
        return "Relación débil"
    else:
        return "No hay relación significativa"

# Verificar si hay datos suficientes para la regresión
if len(df) > 2:
    # **Regresión General: Antigüedad vs Precio**
    X = df["Antigüedad"]
    Y = df["PrecioReciente"]

    # Agregar constante para la regresión
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    r2_general = model.rsquared  # Obtener el valor de R^2

    # Predicciones para la línea de regresión
    df["PredictedPrice"] = model.predict(X)

    # Graficar dispersión de precios vs antigüedad con la línea de regresión
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Antigüedad"], df["PrecioReciente"], color='blue', alpha=0.5, s=1, label="Precios reales")
    plt.plot(df["Antigüedad"], df["PredictedPrice"], color='red', linewidth=2, label="Línea de regresión")
    
    # Agregar el texto de R^2 en la gráfica
    plt.text(
        min(df["Antigüedad"]) + 2, max(df["PrecioReciente"]) * 0.9,
        f"R² = {r2_general:.3f} ({interpretar_r2(r2_general)})",
        fontsize=12, bbox=dict(facecolor='white', alpha=0.7)
    )
    
    plt.xlabel("Antigüedad de la Propiedad (Años)")
    plt.ylabel("Precio de Venta (£)")
    plt.title("Regresión General: Antigüedad vs Precio de Venta")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Mostrar resumen del modelo de regresión general
    print("### REGRESIÓN GENERAL ###")
    print(model.summary())

# Verificar si hay datos suficientes para la regresión
if len(df) > 2:
    # **Regresiones por tipo de propiedad con límite automático en el eje Y**
    for prop_type in df["TipoPropiedad"].unique():
        df_subset = df[df["TipoPropiedad"] == prop_type]
        
        if len(df_subset) > 2:  # Asegurar datos suficientes para regresión
            X_subset = df_subset["Antigüedad"]
            Y_subset = df_subset["PrecioReciente"]
            
            # Agregar constante
            X_subset = sm.add_constant(X_subset)
            model_subset = sm.OLS(Y_subset, X_subset).fit()
            r2_subset = model_subset.rsquared  # Obtener el valor de R^2

            # Predicciones
            df_subset["PredictedPrice"] = model_subset.predict(X_subset)

            # **Ajustar el eje Y automáticamente usando percentiles**
            y_min = df_subset["PrecioReciente"].min()
            y_max = df_subset["PrecioReciente"].quantile(0.95)  # 95% de los datos
            
            # Graficar
            plt.figure(figsize=(8, 5))
            # plt.scatter(df_subset["Antigüedad"], df_subset["PrecioReciente"], alpha=0.5, label="Precios reales")
            # plt.scatter(df["Antigüedad"], df["PrecioReciente"], alpha=0.3, s=1, label="Precios reales")
            # plt.plot(df_subset["Antigüedad"], df_subset["PredictedPrice"], color='red', linewidth=2, label="Línea de regresión")

            # Agregar el texto de R^2 en la gráfica
            plt.text(
                min(df_subset["Antigüedad"]) + 2, y_max * 0.9,
                f"R² = {r2_subset:.3f} ({interpretar_r2(r2_subset)})",
                fontsize=12, bbox=dict(facecolor='white', alpha=0.7)
            )

            plt.xlabel("Antigüedad de la Propiedad (Años)")
            plt.ylabel("Precio de Venta (£)")
            plt.title(f"Regresión para {prop_type}: Antigüedad vs Precio de Venta")
            plt.legend()
            plt.ylim(y_min, y_max)  # **Límite automático del eje Y**
            plt.grid(True)
            plt.show()

            # Mostrar resumen del modelo de regresión por tipo de propiedad
            print(f"### REGRESIÓN PARA {prop_type.upper()} ###")
            print(model_subset.summary())

else:
    print("No hay suficientes datos para realizar la regresión.")