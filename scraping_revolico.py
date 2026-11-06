# Script de Scraping y Extracción de Fuentes
import pandas as pd

def extraer_revolico():
    # Simulación del proceso automatizado de extracción de anuncios de Revolico
    print("Extrayendo datos de Revolico...")
    data = {"id": [1, 2], "municipio": ["Playa", "Centro Habana"], "precio": [617000, 13500]}
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = extraer_revolico()
    df.to_csv("datos_revolico_raw.csv", index=False)
