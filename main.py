from preprocessing import calculate_days_on_market, calculate_price_changes, plot_avg_price_by_zone

def main():
    # Preprocesamiento
    file_path = 'dataAnalysis/datos/csv/london-87490/data.csv'
    calculate_days_on_market(file_path)
    calculate_price_changes(file_path)

    # Visualización
    plot_avg_price_by_zone(file_path)

if __name__ == "__main__":
    main()
