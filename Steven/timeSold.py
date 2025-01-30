import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import re
import pandas as pd
import numpy as np

# Función para redondear años a partir de días
def calcular_anios(dias):
    return round(dias / 365)

# Función para limpiar precios
def limpiar_precio(precio):
    precio_limpio = re.sub(r'[^\d.]', '', precio)  # Remover caracteres no numéricos
    try:
        return float(precio_limpio)
    except ValueError:
        return None

# Función genérica para procesar ciudades
def procesar_ciudades(ciudades, directorio_datos, callback):
    resultados_por_ciudad = {}

    for ciudad in ciudades:
        archivo_json = os.path.join(directorio_datos, ciudad, 'data.json')
        #print(f"Procesando archivo: {archivo_json}")

        if not os.path.exists(archivo_json):
            print(f"El archivo para la ciudad {ciudad} no existe. Se omitirá.")
            continue

        with open(archivo_json, 'r') as f:
            data = json.load(f)

        # Aplicar la lógica específica definida en el callback
        resultados_por_ciudad[ciudad] = callback(data)

    return resultados_por_ciudad

# Ejercicio 1: Calcular años transcurridos entre las dos últimas transacciones
def calcular_anios_transcurridos(data):
    anios_transcurridos = []

    for propiedad in data:
        if len(propiedad['transactions']) >= 2:
            transacciones = sorted(
                propiedad['transactions'],
                key=lambda x: datetime.strptime(x['dateSold'], '%d %b %Y'),
                reverse=True
            )
            ultima_fecha = datetime.strptime(transacciones[0]['dateSold'], '%d %b %Y')
            penultima_fecha = datetime.strptime(transacciones[1]['dateSold'], '%d %b %Y')
            dias_diferencia = (ultima_fecha - penultima_fecha).days
            anios_transcurridos.append(calcular_anios(dias_diferencia))

    return anios_transcurridos

# Ejercicio 2: Calcular porcentaje de aumento/disminución de precios

def calcular_cambio_porcentual(propiedad):
    transacciones = sorted(
        propiedad['transactions'],
        key=lambda x: datetime.strptime(x['dateSold'], '%d %b %Y')
    )
    precio_inicial = limpiar_precio(transacciones[0]['displayPrice'])
    precio_final = limpiar_precio(transacciones[-1]['displayPrice'])

    if precio_inicial is not None and precio_final is not None and precio_inicial > 0:
        return ((precio_final - precio_inicial) / precio_inicial) * 100
    return None


def procesar_cambios_porcentuales(data):
    total_propiedades = 0
    propiedades_con_aumento = 0
    propiedades_con_disminucion = 0

    for propiedad in data:
        if len(propiedad['transactions']) >= 2:
            cambio_porcentual = calcular_cambio_porcentual(propiedad)

            if cambio_porcentual is not None:
                total_propiedades += 1
                if cambio_porcentual > 0:
                    propiedades_con_aumento += 1
                elif cambio_porcentual < 0:
                    propiedades_con_disminucion += 1

    if total_propiedades > 0:
        porcentaje_aumento = (propiedades_con_aumento / total_propiedades) * 100
        porcentaje_disminucion = (propiedades_con_disminucion / total_propiedades) * 100
    else:
        porcentaje_aumento = 0
        porcentaje_disminucion = 0

    return {
        "total_propiedades": total_propiedades,
        "porcentaje_aumento": round(porcentaje_aumento, 2),
        "porcentaje_disminucion": round(porcentaje_disminucion, 2)
    }

# Ejercicio 3: Calcular precio promedio reciente (últimos 5 años)
def calcular_precio_promedio_reciente(data):
    cinco_anios_atras = datetime.now() - timedelta(days=5*365)
    precios_recientes = []

    for propiedad in data:
        for transaccion in propiedad['transactions']:
            fecha_venta = datetime.strptime(transaccion['dateSold'], '%d %b %Y')
            if fecha_venta >= cinco_anios_atras:
                precio = limpiar_precio(transaccion['displayPrice'])
                if precio is not None:
                    precios_recientes.append(precio)

    if precios_recientes:
        return round(sum(precios_recientes) / len(precios_recientes),2)
    return 0

# Configurar el directorio base relativo al script actual
directorio_datos = os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
directorio_destino =os.path.join(os.path.dirname(__file__), '..', 'Steven', 'json')
#Carpeta con destino nuevo


# Verificar si el directorio base existe
if not os.path.exists(directorio_datos):
    print(f"El directorio base no existe: {os.path.abspath(directorio_datos)}")
    exit()

# Lista de ciudades
ciudades = ["london", "birmingham", "leeds", "sheffield", "manchester", 
            "bradford", "bristol", "coventry", "leicester", "nottingham", 
            "stockport", "kingston-upon-hull", "dudley", "newcastle-upon-tyne", 
            "bolton", "walsall", "plymouth", "sunderland", "milton-keynes", 
            "wolverhampton", "rotherham", "southampton", "derby", "northampton", 
            "stoke-on-trent", "oldham", "reading", "luton", "swindon", "york", 
            "portsmouth", "bournemouth", "peterborough", "colchester", "preston", 
            "southend-on-sea", "saint-helens", "norwich", "brighton", "chelmsford", 
            "telford", "huddersfield", "oxford", "middlesbrough", "slough", "poole", 
            "cambridge", "blackpool", "west-bromwich", "exeter", "blackburn", "ipswich", 
            "gloucester", "solihull", "crawley", "basildon", "watford", "eastbourne", 
            "maidstone", "sutton-coldfield", "halifax"]

# Verificar carpetas disponibles
carpetas_existentes = os.listdir(directorio_datos)
ciudades_disponibles = [
    carpeta for carpeta in carpetas_existentes if carpeta.lower() in [ciudad.lower() for ciudad in ciudades]
]
#print("Ciudades disponibles para procesar:")
#print(ciudades_disponibles)

# Ejecutar Ejercicio 1
anios_por_ciudad = procesar_ciudades(ciudades_disponibles, directorio_datos, calcular_anios_transcurridos)

# Guardar resultados de años transcurridos
promedios_por_ciudad = {
    ciudad: round(sum(anios) / len(anios), 2) if anios else 0
    for ciudad, anios in anios_por_ciudad.items()
}
with open(os.path.join(directorio_destino, 'promedios_por_ciudad.json'), 'w') as f:
    json.dump(promedios_por_ciudad, f, indent=4)
print("Resultados de años guardados en promedios_por_ciudad.json")

# Ejecutar Ejercicio 2
resultados_por_ciudad = procesar_ciudades(ciudades_disponibles, directorio_datos, procesar_cambios_porcentuales)

# Guardar resultados de cambios de precio
with open(os.path.join(directorio_destino, 'cambios_precio_por_ciudad.json'), 'w') as f:
    json.dump(resultados_por_ciudad, f, indent=4)
print("Resultados de cambios guardados en cambios_precio_por_ciudad.json")

# Ejecutar Ejercicio 3
precios_promedio_recientes = procesar_ciudades(ciudades_disponibles, directorio_datos, calcular_precio_promedio_reciente)

# Guardar resultados de precios promedio recientes
with open(os.path.join(directorio_destino, 'precios_promedio_recientes.json'), 'w') as f:
    json.dump(precios_promedio_recientes, f, indent=4)
print("Resultados de precios promedio recientes guardados en precios_promedio_recientes.json")


# Función para graficar los 10 primeros valores de un diccionario
def graficar_top_10(datos, titulo, xlabel):
    # Convertir a DataFrame y ordenar
    df = pd.DataFrame(list(datos.items()), columns=["Ciudad", "Valor"])
    df = df.sort_values(by="Valor", ascending=False).head(10)

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.barh(df["Ciudad"], df["Valor"], color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel("Ciudad")
    plt.title(titulo)
    plt.gca().invert_yaxis()  # Invertir el eje Y para que el mayor valor esté arriba
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# Cargar y graficar los resultados de cada ejercicio
ejercicios = {
    "promedios_por_ciudad.json": ("Promedio de Años Entre Transacciones", "Años"),
    "precios_promedio_recientes.json": ("Precios Promedio Recientes", "Precio Promedio")
}

for archivo, (titulo, xlabel) in ejercicios.items():
    ruta_archivo = os.path.join("Steven","json", archivo)
    
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as f:
            datos = json.load(f)
        
        # Filtrar solo valores numéricos y graficar
        datos_filtrados = {k: v for k, v in datos.items() if isinstance(v, (int, float))}
        graficar_top_10(datos_filtrados, titulo, xlabel)
    else:
        print(f"Archivo {archivo} no encontrado.")


"""
# Ruta del archivo JSON (ajústala según tu sistema)
archivo_json = os.path.join(os.path.dirname(__file__), '..', 'Steven', 'json', "cambios_precio_por_ciudad.json")

# Cargar los datos desde el archivo JSON
with open(archivo_json, "r") as f:
    cambios_precio = json.load(f)

# Seleccionar solo las primeras 10 ciudades en el orden en que aparecen
ciudades = list(cambios_precio.keys())[:10]
aumentos = [cambios_precio[ciudad]["porcentaje_aumento"] for ciudad in ciudades[:10]]
disminuciones = [cambios_precio[ciudad]["porcentaje_disminucion"] for ciudad in ciudades[:10]]

# Limitar los datos a solo las primeras 10 ciudades
ciudades = ciudades[:10]
aumentos = aumentos[:10]
disminuciones = disminuciones[:10]

# Posiciones para las barras
x = np.arange(len(ciudades))

# Crear gráfico de barras agrupadas con las primeras 10 ciudades
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - 0.2, aumentos, width=0.4, label='% Aumento', color='skyblue')
ax.bar(x + 0.2, disminuciones, width=0.4, label='% Disminución', color='salmon')

# Configuración de etiquetas y títulos
ax.set_xlabel("Ciudades")
ax.set_ylabel("Porcentaje")
ax.set_title("Porcentaje de Aumento y Disminución de Precios (Primeras 10 Ciudades)")
ax.set_xticks(x)
ax.set_xticklabels(ciudades, rotation=45, ha="right")
ax.legend()

# Mostrar gráfico
plt.show()
"""

def obtener_cantidad_ciudades():
    while True:
        try:
            n = int(input("Ingrese la cantidad de ciudades a mostrar (1-50): "))
            if 1 <= n <= 50:
                return n
            else:
                print("Por favor, ingrese un número entre 1 y 50.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero.")

def graficar_ciudades(num_ciudades, archivo_json="cambios_precio_por_ciudad.json"):
    directorio_destino = os.path.join(os.path.dirname(__file__), '..', 'Steven', 'json')
    ruta_archivo = os.path.join(directorio_destino, archivo_json)

    if not os.path.exists(ruta_archivo):
        print(f"Archivo no encontrado: {ruta_archivo}")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, "Archivo no encontrado", fontsize=12, ha='center')
        ax.set_title(f"{archivo_json} - No encontrado")
        return fig

    with open(ruta_archivo, "r") as f:
        datos = json.load(f)

    if not isinstance(datos, dict):
        print(f"Advertencia: {archivo_json} no tiene el formato esperado (dict).")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, "Datos no válidos", fontsize=12, ha='center')
        ax.set_title(f"{archivo_json} - Formato incorrecto")
        return fig

    # Caso especial: Gráfica de cambios porcentuales
    if archivo_json == "cambios_precio_por_ciudad.json":
        ciudades = list(datos.keys())[:num_ciudades]
        aumentos = [datos[ciudad].get("porcentaje_aumento", 0) for ciudad in ciudades]
        disminuciones = [datos[ciudad].get("porcentaje_disminucion", 0) for ciudad in ciudades]

        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(ciudades))
        width = 0.4

        ax.bar(x, aumentos, width, label="% Aumento", color='skyblue')
        ax.bar([i + width for i in x], disminuciones, width, label="% Disminución", color='salmon')

        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(ciudades, rotation=45, ha="right")

        ax.set_xlabel("Ciudades")
        ax.set_ylabel("Porcentaje")
        ax.set_title("Porcentaje de Aumento y Disminución de Precios (Primeras {} Ciudades)".format(num_ciudades))
        ax.legend()

        return fig

    # Para otros JSONs, extraer valores generales
    datos_filtrados = {ciudad: valor for ciudad, valor in datos.items() if isinstance(valor, (int, float))}
    datos_ordenados = sorted(datos_filtrados.items(), key=lambda x: x[1], reverse=True)
    ciudades_seleccionadas = datos_ordenados[:num_ciudades]
    ciudades = [ciudad[0] for ciudad in ciudades_seleccionadas]
    valores = [ciudad[1] for ciudad in ciudades_seleccionadas]

    if not valores:
        print(f"Advertencia: No hay datos numéricos en {archivo_json}.")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, "Sin datos disponibles", fontsize=12, ha='center')
        ax.set_title(f"{archivo_json} - Sin datos")
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ciudades, valores, color='skyblue')

    ax.set_xticks(range(len(ciudades)))
    ax.set_xticklabels(ciudades, rotation=45, ha="right")

    ax.set_xlabel("Ciudades")
    ax.set_ylabel("Valor")
    ax.set_title(f"Gráfico basado en {archivo_json}")

    return fig
