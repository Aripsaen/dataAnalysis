import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def cargar_datos():
    archivo = filedialog.askopenfilename()
    print(f"Archivo seleccionado: {archivo}")

def mostrar_grafico():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])  # Gráfico de ejemplo

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Interfaz de Análisis de Datos")

btn_cargar = tk.Button(ventana, text="Cargar Datos", command=cargar_datos)
btn_cargar.pack()

btn_grafico = tk.Button(ventana, text="Mostrar Gráfico", command=mostrar_grafico)
btn_grafico.pack()

ventana.mainloop()