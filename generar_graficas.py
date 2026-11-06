# Script de Generación de Gráficas Analíticas (Matplotlib)
import matplotlib.pyplot as plt
import os

def generar_grafica_ejemplo():
    os.makedirs("graficas", exist_ok=True)
    municipios = ['Playa', 'Vedado', 'Centro Habana']
    precios = [617000, 80000, 13500]
    
    plt.figure(figsize=(8, 5))
    plt.barh(municipios, precios, color='#2b5c8f', edgecolor='black')
    plt.xlabel('Precio Mediano (USD)', fontweight='bold')
    plt.title('Distribución de Precios por Municipio', fontweight='bold')
    plt.tight_layout()
    plt.savefig("graficas/ejemplo_precios.png", dpi=300)
    plt.close()
    print("Gráfica generada con éxito.")

if __name__ == "__main__":
    generar_grafica_ejemplo()
