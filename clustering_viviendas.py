# Script de Clustering K-Means para la segmentación de viviendas
import pandas as pd
from sklearn.cluster import KMeans

def ejecutar_clustering():
    df = pd.read_csv("../datos/datos_inmobiliarios_habana_limpios.csv")
    X = df[['precio_mediano_usd']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X)
    print("Clustering completado con éxito.")
    print(df)

if __name__ == "__main__":
    ejecutar_clustering()
