import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from anlisis.precios import obtener_datos  # Importar datos desde precios.py
from Steven.timeSold import obtener_cantidad_ciudades, graficar_ciudades

# Obtener datos desde precios.py
city_differences, city_ages, transaction_counts, cities_list, initial_prices, final_prices, price_differences, average_ages, city_differences_sorted = obtener_datos()

directorio_destino = os.path.join(os.path.dirname(__file__), '..', 'Steven', 'json')

# Interfaz Gráfica con Tkinter
class CityAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Ciudades")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        self.n = tk.IntVar(value=5)
        self.figures = []
        self.current_index = 0
        self.create_widgets()
        self.update_graph()
    
    def create_widgets(self):
        # Frame para controles
        control_frame = tk.Frame(self.root, bg="#ffffff", pady=10)
        control_frame.pack(fill=tk.X)
        
        # Etiqueta
        label = tk.Label(control_frame, text="Seleccione la cantidad de ciudades:", bg="#ffffff", font=("Arial", 12))
        label.pack(side=tk.LEFT, padx=10)
        
        # Barra deslizante
        self.slider = ttk.Scale(control_frame, from_=1, to=len(cities_list), orient='horizontal', variable=self.n, command=self.update_graph)
        self.slider.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Botones de navegación
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        btn_prev = ttk.Button(button_frame, text="◀ Anterior", command=self.prev_graph)
        btn_prev.pack(side=tk.LEFT, padx=10)
        btn_next = ttk.Button(button_frame, text="Siguiente ▶", command=self.next_graph)
        btn_next.pack(side=tk.RIGHT, padx=10)
        
        # Canvas para la gráfica
        self.canvas_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    def update_graph(self, event=None):
        n = self.n.get()
        top_n_cities = city_differences_sorted[:int(n)]
        self.figures = [
            self.create_price_comparison_chart(top_n_cities),
            self.create_age_difference_chart(top_n_cities),
            self.create_transaction_count_chart(top_n_cities),
            self.create_time_sold_graph(n),
            self.create_recent_average_price_graph(n),
            self.create_price_change_percentage_graph(n)
        ]
        self.current_index = 0
        self.display_graph()

    def create_age_difference_chart(self, top_n_cities):
        fig, ax1 = plt.subplots(figsize=(8, 5))
        city_names = [city[0] for city in top_n_cities]
        indices = range(len(city_names))
        bar_width = 0.25

        ages = [average_ages[cities_list.index(city[0])] for city in top_n_cities]
        price_diffs = [city[1] / 1000 for city in top_n_cities]

        ax1.bar(indices, ages, bar_width, label="Antigüedad Promedio (Años)", color='orange')
        ax2 = ax1.twinx()
        ax2.bar([i + bar_width for i in indices], price_diffs, bar_width, label="Diferencia de Precio (£K)", color='purple')

        ax1.set_xticks([i + bar_width for i in indices])
        ax1.set_xticklabels(city_names, rotation=45, ha="right")
        
        ax1.set_xlabel("Ciudades")
        ax1.set_ylabel("Antigüedad Promedio (Años)")
        ax2.set_ylabel("Diferencia de Precio (£K)")
        ax1.set_title("Antigüedad Promedio y Diferencia de Precio por Ciudad")
        ax1.legend()
        ax2.legend()

        return fig

    def create_transaction_count_chart(self, top_n_cities):
        fig, ax = plt.subplots(figsize=(8, 5))
        city_names = [city[0] for city in top_n_cities]
        counts = [transaction_counts[city[0]] for city in top_n_cities]
        
        ax.bar(city_names, counts, color='skyblue')
        ax.set_xticks(range(len(city_names)))
        ax.set_xticklabels(city_names, rotation=45, ha="right")
        
        ax.set_xlabel("Ciudades")
        ax.set_ylabel("Número de Transacciones")
        ax.set_title("Número de Transacciones Inmobiliarias")
        
        return fig

    
    def create_price_comparison_chart(self, top_n_cities):
        fig, ax = plt.subplots(figsize=(8, 5))
        city_names = [city[0] for city in top_n_cities]
        indices = range(len(city_names))
        bar_width = 0.25
        
        initial_p = [initial_prices[cities_list.index(city[0])] for city in top_n_cities]
        final_p = [final_prices[cities_list.index(city[0])] for city in top_n_cities]
        price_diffs = [city[1] for city in top_n_cities]
        
        ax.bar(indices, initial_p, bar_width, label="Venta Inicial", color='blue')
        ax.bar([i + bar_width for i in indices], final_p, bar_width, label="Venta Final", color='green')
        ax.bar([i + 2 * bar_width for i in indices], price_diffs, bar_width, label="Diferencia", color='red')
        
        ax.set_xticks([i + bar_width for i in indices])
        ax.set_xticklabels(city_names, rotation=45, ha="right")
        ax.legend()
        
        ax.set_xlabel("Ciudades")
        ax.set_ylabel("Precios en £")
        ax.set_title("Comparación de Precios de Venta")
        
        return fig
    
    def create_time_sold_graph(self, num_ciudades):
        fig = graficar_ciudades(num_ciudades, "promedios_por_ciudad.json")  # Archivo correcto para esta gráfica
        return fig

    def create_recent_average_price_graph(self, num_ciudades):
        fig = graficar_ciudades(num_ciudades, "precios_promedio_recientes.json")
        return fig

    def create_price_change_percentage_graph(self, num_ciudades):
        # Cargar datos del JSON
        directorio_destino = os.path.join(os.path.dirname(__file__), '..', 'Steven', 'json')
        ruta_archivo = os.path.join(directorio_destino, "cambios_precio_por_ciudad.json")

        if not os.path.exists(ruta_archivo):
            print("Archivo no encontrado:", ruta_archivo)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.text(0.5, 0.5, "Archivo no encontrado", fontsize=12, ha='center')
            ax.set_title("Cambio Porcentual de Precio - No encontrado")
            return fig

        with open(ruta_archivo, "r") as f:
            datos = json.load(f)

        if not isinstance(datos, dict):
            print("Advertencia: cambios_precio_por_ciudad.json tiene formato incorrecto.")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.text(0.5, 0.5, "Datos no válidos", fontsize=12, ha='center')
            ax.set_title("Cambio Porcentual de Precio - Datos no válidos")
            return fig

        # Extraer los datos correctos
        ciudades = list(datos.keys())[:num_ciudades]
        aumentos = [datos[ciudad].get("porcentaje_aumento", 0) for ciudad in ciudades]
        disminuciones = [datos[ciudad].get("porcentaje_disminucion", 0) for ciudad in ciudades]

        # Verificar si hay datos válidos
        if not any(aumentos) and not any(disminuciones):
            print("Advertencia: No hay datos numéricos en cambios_precio_por_ciudad.json.")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.text(0.5, 0.5, "Sin datos disponibles", fontsize=12, ha='center')
            ax.set_title("Cambio Porcentual de Precio - Sin datos")
            return fig

        # Crear gráfico de barras agrupadas
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


    
    def display_graph(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(self.figures[self.current_index], master=self.canvas_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    
    def next_graph(self):
        self.current_index = (self.current_index + 1) % len(self.figures)
        self.display_graph()
    
    def prev_graph(self):
        self.current_index = (self.current_index - 1) % len(self.figures)
        self.display_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = CityAnalysisApp(root)
    root.mainloop()
