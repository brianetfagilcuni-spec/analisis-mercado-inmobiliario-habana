# =========================================================
# SCRIPT DE LIMPIEZA Y CLUSTERING K-MEANS DE PRECIOS
# =========================================================
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Cargar datos scrapeados y de catálogos
datos = {
    'municipio': ['Playa', 'Vedado', 'Santo Suárez', 'Habana del Este', '10 de Octubre', 'Cerro', 'Centro Habana'],
    'precio_mediano_usd': [617000, 80000, 55000, 37500, 25000, 13750, 13500],
    'demanda': ['Muy Alta', 'Alta', 'Media', 'Media', 'Media-Baja', 'Baja', 'Media-Baja']
}

df = pd.DataFrame(datos)

# Normalización
scaler = StandardScaler()
df['precio_scaled'] = scaler.fit_transform(df[['precio_mediano_usd']])

# Clustering K-Means (3 Clusters)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(df[['precio_scaled']])

cluster_names = {
    df[df['municipio']=='Playa']['cluster_id'].values[0]: 'Cluster 1: Exclusivo / Alta Gama',
    df[df['municipio']=='Vedado']['cluster_id'].values[0]: 'Cluster 2: Gama Media-Alta',
    df[df['municipio']=='Centro Habana']['cluster_id'].values[0]: 'Cluster 3: Popular / Accesible'
}

df['cluster_nombre'] = df['cluster_id'].map(cluster_names)
df_limpio = df.drop(columns=['precio_scaled'])

# Guardar dataset limpio y agrupado
df_limpio.to_csv('../datos/datos_inmobiliarios_habana_limpios.csv', index=False)
print("Clustering completado y datos guardados en ../datos/datos_inmobiliarios_habana_limpios.csv")
