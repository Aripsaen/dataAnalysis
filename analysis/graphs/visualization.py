import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import statsmodels.api as sm

plt.style.use('seaborn-v0_8-darkgrid')

# Ruta del archivo auxiliar con los promedios
promedios_path = "analysis/auxiliary_files/promedios-por-ciudad.csv"

# Ruta de la carpeta donde se guardaron los archivos de tendencias
tendencias_path = "analysis/auxiliary_files/tendencias"

# Ruta del archivo de propiedades procesadas
propiedades_path = "analysis/auxiliary_files/propiedades_procesadas.csv"


# Verificar si el archivo existe
if not os.path.exists(promedios_path):
    print("No hay datos de promedios disponibles. Ejecuta `average-prices-per-city.py` primero.")
    exit()
    
# Verificar si existen archivos de tendencias
if not os.path.exists(tendencias_path) or not os.listdir(tendencias_path):
    print("No hay datos de tendencias disponibles. Ejecuta `tendency.py` primero.")
    exit()
    
# Verificar si el archivo existe
if not os.path.exists(propiedades_path):
    print("No hay datos de propiedades procesadas. Ejecuta `regression.py` primero.")
    exit()
    
# Obtener la lista de ciudades con tendencias guardadas
archivos = [f for f in os.listdir(tendencias_path) if f.startswith("tendencias_") and f.endswith(".csv")]
ciudades = [archivo.replace("tendencias_", "").replace(".csv", "") for archivo in archivos]

# Cargar los datos
df_promedios = pd.read_csv(promedios_path)

# Ordenar los datos de mayor a menor precio
df_promedios_sorted = df_promedios.sort_values(by="Promedio (£)", ascending=False)

# Cargar los datos
df = pd.read_csv(propiedades_path)

# Función para mostrar la ventana de análisis de precios
def abrir_ventana_precios():
    ventana_precios = tk.Toplevel(root)
    ventana_precios.title("Análisis de Precios Promedio por Ciudad")
    ventana_precios.geometry("500x250")

    # Etiqueta de selección de número de ciudades
    label = tk.Label(ventana_precios, text="Seleccione cuántas ciudades desea visualizar:", font=("Arial", 12))
    label.pack(pady=10)

    # Opciones de cantidad de ciudades a visualizar
    opciones_ciudades = [5, 10, 20, len(df_promedios)]  # Incluye la opción de todas las ciudades
    cantidad_var = tk.IntVar()
    cantidad_var.set(10)  # Valor por defecto

    # Crear Dropdown (Combobox) para seleccionar cantidad de ciudades
    dropdown = ttk.Combobox(ventana_precios, textvariable=cantidad_var, values=opciones_ciudades, state="readonly", font=("Arial", 12))
    dropdown.pack(pady=10)

    # Función para generar la gráfica
    def mostrar_grafico_tendencias_prom():
        num_ciudades = cantidad_var.get()
        top_ciudades = df_promedios_sorted.head(num_ciudades)

        # Crear gráfico
        plt.figure(figsize=(12, 8))
        plt.barh(top_ciudades['Ciudad'], top_ciudades['Promedio (£)'], color='skyblue')

        # Personalizar el gráfico
        plt.xlabel("Precio Promedio (£)", fontsize=12)
        plt.ylabel("Ciudad", fontsize=12)
        plt.title(f"Top {num_ciudades} Ciudades con Mayor Precio Promedio", fontsize=14)
        plt.gca().invert_yaxis()  # Invertir el eje para mejor visualización
        plt.tight_layout()

        # Mostrar gráfico
        plt.show()

    # Botón para generar la gráfica
    btn_mostrar = tk.Button(ventana_precios, text="Mostrar Gráfico", command=mostrar_grafico_tendencias_prom, font=("Arial", 12), bg="blue", fg="white")
    btn_mostrar.pack(pady=20)
    
def abrir_ventana_tendencias():
    ventana_tendencias = tk.Toplevel(root)
    ventana_tendencias.title("Análisis de Tendencias de Precios")
    ventana_tendencias.geometry("500x250")

    # Etiqueta de selección de ciudad
    label = tk.Label(ventana_tendencias, text="Seleccione una ciudad:", font=("Arial", 12))
    label.pack(pady=10)

    # Variable para el Dropdown
    ciudad_var = tk.StringVar()
    ciudad_var.set(ciudades[0])  # Valor por defecto

    # Crear Dropdown (Combobox) para seleccionar ciudad
    dropdown = ttk.Combobox(ventana_tendencias, textvariable=ciudad_var, values=ciudades, state="readonly", font=("Arial", 12))
    dropdown.pack(pady=10)
    
    def mostrar_grafico_tendencias():
        ciudad_seleccionada = ciudad_var.get()
        archivo_ciudad = os.path.join(tendencias_path, f"tendencias_{ciudad_seleccionada}.csv")

        # Cargar los datos
        df = pd.read_csv(archivo_ciudad)

        # Crear gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(df['yearSold'], df['displayPrice'], marker='o', linestyle='-', color='b')

        # Personalizar el gráfico
        plt.title(f"Evolución de Precios en {ciudad_seleccionada.capitalize()}", fontsize=14)
        plt.xlabel("Año", fontsize=12)
        plt.ylabel("Precio Promedio (£)", fontsize=12)
        plt.grid()
        plt.tight_layout()

        # Mostrar gráfico
        plt.show()
        

 # Botón para generar la gráfica
    btn_mostrar = tk.Button(ventana_tendencias, text="Mostrar Gráfico", command=mostrar_grafico_tendencias, font=("Arial", 12), bg="green", fg="white")
    btn_mostrar.pack(pady=20)

# Función para abrir la ventana de análisis de influencia de variables
def abrir_ventana_influencia():
    ventana_influencia = tk.Toplevel(root)
    ventana_influencia.title("Influencia de Variables en el Precio")
    ventana_influencia.geometry("500x250")

    # Etiqueta de selección de variable
    label = tk.Label(ventana_influencia, text="Seleccione la variable a analizar:", font=("Arial", 12))
    label.pack(pady=10)

    # Opciones de variables para regresión
    opciones_variables = ["Antigüedad", "TipoPropiedad"]
    variable_var = tk.StringVar()
    variable_var.set(opciones_variables[0])  # Valor por defecto

    # Crear Dropdown (Combobox) para seleccionar variable
    dropdown = ttk.Combobox(ventana_influencia, textvariable=variable_var, values=opciones_variables, state="readonly", font=("Arial", 12))
    dropdown.pack(pady=10)

    # Función para generar la regresión y la gráfica
    def mostrar_grafico():
        variable_seleccionada = variable_var.get()
        
        if variable_seleccionada == "Antigüedad":
            X = df["Antigüedad"]
            Y = df["PrecioReciente"]

            # Agregar constante y realizar regresión
            X = sm.add_constant(X)
            model = sm.OLS(Y, X).fit()
            r2_value = model.rsquared

            # Predicciones
            df["PredictedPrice"] = model.predict(X)

            # Crear gráfico
            plt.figure(figsize=(8, 5))
            plt.scatter(df["Antigüedad"], df["PrecioReciente"], alpha=0.5, s=10, label="Precios reales")
            plt.plot(df["Antigüedad"], df["PredictedPrice"], color='red', linewidth=2, label="Línea de regresión")

            # Agregar el texto de R^2 en la gráfica
            plt.text(
                min(df["Antigüedad"]) + 2, max(df["PrecioReciente"]) * 0.9,
                f"R² = {r2_value:.3f}",
                fontsize=12, bbox=dict(facecolor='white', alpha=0.7)
            )

            plt.xlabel("Antigüedad de la Propiedad (Años)", fontsize=12)
            plt.ylabel("Precio de Venta (£)", fontsize=12)
            plt.title("Regresión: Antigüedad vs Precio de Venta", fontsize=14)
            plt.legend()
            plt.grid(True)
            plt.show()

        elif variable_seleccionada == "TipoPropiedad":
            # Regresiones por tipo de propiedad
            for prop_type in df["TipoPropiedad"].unique():
                df_subset = df[df["TipoPropiedad"] == prop_type]
                
                if len(df_subset) > 2:
                    X_subset = df_subset["Antigüedad"]
                    Y_subset = df_subset["PrecioReciente"]

                    # Agregar constante y realizar regresión
                    X_subset = sm.add_constant(X_subset)
                    model_subset = sm.OLS(Y_subset, X_subset).fit()
                    r2_subset = model_subset.rsquared

                    # Predicciones
                    df_subset["PredictedPrice"] = model_subset.predict(X_subset)

                    # Crear gráfico
                    plt.figure(figsize=(8, 5))
                    plt.scatter(df_subset["Antigüedad"], df_subset["PrecioReciente"], alpha=0.5, label="Precios reales")
                    plt.plot(df_subset["Antigüedad"], df_subset["PredictedPrice"], color='red', linewidth=2, label="Línea de regresión")

                    # Agregar el texto de R^2 en la gráfica
                    plt.text(
                        min(df_subset["Antigüedad"]) + 2, max(df_subset["PrecioReciente"]) * 0.9,
                        f"R² = {r2_subset:.3f}",
                        fontsize=12, bbox=dict(facecolor='white', alpha=0.7)
                    )

                    plt.xlabel("Antigüedad de la Propiedad (Años)", fontsize=12)
                    plt.ylabel("Precio de Venta (£)", fontsize=12)
                    plt.title(f"Regresión para {prop_type}: Antigüedad vs Precio de Venta", fontsize=14)
                    plt.legend()
                    plt.grid(True)
                    plt.show()

    # Botón para generar la gráfica
    btn_mostrar = tk.Button(ventana_influencia, text="Mostrar Gráfico", command=mostrar_grafico, font=("Arial", 12), bg="orange", fg="white")
    btn_mostrar.pack(pady=20)


# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Análisis de Precios Inmobiliarios")
root.geometry("500x300")

# Etiqueta de bienvenida
label = tk.Label(root, text="Seleccione el tipo de análisis que desea realizar:", font=("Arial", 14))
label.pack(pady=20)

# Botones de selección
btn_precios = tk.Button(root, text="Análisis de precios promedio por ciudad", command=abrir_ventana_precios, font=("Arial", 12), width=40, bg="blue", fg="white")
btn_precios.pack(pady=10)

btn_tendencias = tk.Button(root, text="Análisis de tendencias de precios", command=abrir_ventana_tendencias, font=("Arial", 12), width=40, bg="green", fg="white")
btn_tendencias.pack(pady=10)

btn_influencia = tk.Button(root, text="Influencia de variables en el precio", command=abrir_ventana_influencia, font=("Arial", 12), width=40, bg="orange", fg="white")
btn_influencia.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
