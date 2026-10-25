import re
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Cargar
df = pd.read_csv("datos_limpios_inmuebles_habana_pro.csv")

# 2. Corregir precio: tomar el precio real del texto del anuncio
def precio_real(txt, fallback):
    m = re.search(r'(\d{1,3}(?:,\d{3})+|\d+)\s*USD', str(txt))
    return float(m.group(1).replace(",", "")) if m else fallback

df["Precio"] = [precio_real(d, p) for d, p in zip(df["Descripción"], df["Precio_Num"])]
df = df[df["Precio"] >= 1000].copy()   # quitar precios absurdos (1, 3, 40 USD...)
# Categoría recalculada con el precio corregido (la del CSV venía de precios erróneos)
df["Categoria_Precio"] = pd.cut(df["Precio"], [0, 20000, 50000, 150000, float("inf")],
                                labels=["Económico (<20k)", "Medio (20-50k)", "Alto (50-150k)", "Lujo (>150k)"])
df["Zona"] = df["Zona_Limpia"].replace("Otra Zona / No Especificada", "Sin especificar")

print("Anuncios usados:", len(df))
print("Mediana:", df["Precio"].median(), "| Promedio:", round(df["Precio"].mean()))

azul = "#2a5298"

# G1: mediana por zona (zonas con 2+ anuncios)
g = df.groupby("Zona")["Precio"].agg(["median", "count"])
g = g[g["count"] >= 2].sort_values("median")
plt.figure(figsize=(8, 6))
plt.barh(g.index, g["median"], color=azul)
for i, (v, n) in enumerate(zip(g["median"], g["count"])):
    plt.text(v, i, f" ${v:,.0f} (n={n})", va="center", fontsize=8)
plt.title("Precio mediano por zona (USD)")
plt.xlim(0, g["median"].max() * 1.25)
plt.tight_layout(); plt.savefig("grafico_1_precio_por_zona.png", dpi=130); plt.close()

# G2: categoría de precio
c = df["Categoria_Precio"].value_counts().reindex(df["Categoria_Precio"].cat.categories)
plt.figure(figsize=(6, 6))
plt.pie(c, labels=c.index, autopct="%1.0f%%", startangle=90)
plt.title("Categoría de precio")
plt.tight_layout(); plt.savefig("grafico_2_categoria_precio.png", dpi=130); plt.close()

# G3: tipo de inmueble
t = df["Tipo_Inmueble"].value_counts()
plt.figure(figsize=(7, 5))
plt.bar(t.index, t.values, color="#8e44ad")
plt.title("Anuncios por tipo de inmueble")
plt.tight_layout(); plt.savefig("grafico_3_tipo_inmueble.png", dpi=130); plt.close()

# G4: servicios
sv = ["Agua", "Luz", "Gas", "Teléfono", "Internet"]
s = (df[sv] == "Sí").sum()
plt.figure(figsize=(7, 5))
plt.bar(s.index, s.values, color="#27ae60")
plt.title("Anuncios que mencionan cada servicio")
plt.tight_layout(); plt.savefig("grafico_4_servicios.png", dpi=130); plt.close()

# G5: características
ca = ["Patio", "Terraza", "Balcon", "Jardín", "Piscina", "Garaje", "Vista_al_mar", "Placa_Libre", "Independiente"]
k = (df[ca] == "Sí").sum().sort_values()
plt.figure(figsize=(7, 5))
plt.barh(k.index, k.values, color="#e67e22")
plt.title("Características más mencionadas")
plt.tight_layout(); plt.savefig("grafico_5_caracteristicas.png", dpi=130); plt.close()

# G6: histograma de precios (escala log)
plt.figure(figsize=(7, 5))
plt.hist(df["Precio"], bins=[1e3,3e3,6e3,1e4,2e4,4e4,8e4,2e5,8e5], color=azul, edgecolor="white")
plt.xscale("log")
plt.title("Distribución de precios (escala log)")
plt.xlabel("USD")
plt.tight_layout(); plt.savefig("grafico_6_distribucion_precios.png", dpi=130); plt.close()
print("Listo")
