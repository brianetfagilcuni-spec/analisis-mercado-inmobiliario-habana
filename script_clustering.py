"""Clustering K-Means (implementado con NumPy, sin scikit-learn) de anuncios inmobiliarios."""
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1. Cargar y corregir precio ----------
df = pd.read_csv("datos_limpios_inmuebles_habana_pro.csv")

def precio_real(txt, fallback):
    m = re.search(r'(\d{1,3}(?:,\d{3})+|\d+)\s*USD', str(txt))
    return float(m.group(1).replace(",", "")) if m else fallback

df["Precio"] = [precio_real(d, p) for d, p in zip(df["Descripción"], df["Precio_Num"])]
df = df[df["Precio"] >= 1000].reset_index(drop=True)

# ---------- 2. Variables ----------
extras = ["Agua","Luz","Gas","Teléfono","Patio","Terraza","Balcon","Jardín",
          "Piscina","Garaje","Placa_Libre","Independiente"]
df["Categoria_Precio"] = pd.cut(df["Precio"], [0, 20000, 50000, 150000, float("inf")],
                                labels=["Económico (<20k)", "Medio (20-50k)", "Alto (50-150k)", "Lujo (>150k)"])
df["N_extras"] = (df[extras] == "Sí").sum(axis=1)
df["log_precio"] = np.log10(df["Precio"])

X = df[["log_precio", "Cuartos", "Baños", "N_extras"]].astype(float).values
Xs = (X - X.mean(axis=0)) / X.std(axis=0)   # estandarizar

# ---------- 3. K-Means en NumPy ----------
def kmeans(X, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    cent = X[rng.choice(len(X), k, replace=False)]
    for _ in range(iters):
        d = ((X[:, None, :] - cent[None, :, :]) ** 2).sum(axis=2)
        lab = d.argmin(axis=1)
        nuevo = np.array([X[lab == j].mean(axis=0) if (lab == j).any() else cent[j]
                          for j in range(k)])
        if np.allclose(nuevo, cent):
            break
        cent = nuevo
    inercia = ((X - cent[lab]) ** 2).sum()
    return lab, cent, inercia

# ---------- 4. Método del codo ----------
ks = range(1, 8)
inercias = [min(kmeans(Xs, k, seed=s)[2] for s in range(10)) for k in ks]
plt.figure(figsize=(6, 4))
plt.plot(list(ks), inercias, marker="o", color="#2a5298")
plt.xlabel("Número de clusters (k)"); plt.ylabel("Inercia")
plt.title("Método del codo")
plt.tight_layout(); plt.savefig("grafico_7_codo.png", dpi=130); plt.close()

# ---------- 5. Clustering final (k = 3) ----------
K = 3
mejor = min((kmeans(Xs, K, seed=s) for s in range(20)), key=lambda r: r[2])
df["Cluster"] = mejor[0]

# Ordenar clusters de más barato a más caro y ponerles nombre
# Nombres según lo que realmente separa a los grupos (precio y nivel de detalle del anuncio)
lujo = df.groupby("Cluster")["Precio"].median().idxmax()
resto = [c for c in df["Cluster"].unique() if c != lujo]
detallado = max(resto, key=lambda c: df.loc[df["Cluster"] == c, "Cuartos"].mean())
nombres = {lujo: "Lujo", detallado: "Detallado", **{c: "Poco detallado" for c in resto if c != detallado}}
df["Segmento"] = df["Cluster"].map(nombres)

# ---------- 6. Perfil de cada segmento ----------
perfil = df.groupby("Segmento").agg(
    Anuncios=("Precio", "count"),
    Precio_mediano=("Precio", "median"),
    Cuartos=("Cuartos", "mean"),
    Banos=("Baños", "mean"),
    Extras=("N_extras", "mean"),
).round(1).reindex(["Poco detallado", "Detallado", "Lujo"])
print(perfil)
print("\nZonas más frecuentes por segmento:")
print(pd.crosstab(df["Zona_Limpia"], df["Segmento"]).sort_values("Lujo", ascending=False).head(8))
perfil.to_csv("datos_limpios_perfil_clusters.csv")
df.to_csv("datos_limpios_con_clusters.csv", index=False)

# ---------- 7. Gráficos ----------
colores = {"Poco detallado": "#7f8c8d", "Detallado": "#27ae60", "Lujo": "#c0392b"}
plt.figure(figsize=(7, 5))
for seg, g in df.groupby("Segmento"):
    plt.scatter(g["N_extras"] + np.random.uniform(-.15, .15, len(g)), g["Precio"],
                label=f"{seg} (n={len(g)})", color=colores[seg], alpha=.75)
plt.yscale("log")
plt.xlabel("Cantidad de servicios/características mencionadas")
plt.ylabel("Precio USD (escala log)")
plt.title("Segmentos de anuncios (K-Means, k=3)")
plt.legend()
plt.tight_layout(); plt.savefig("grafico_8_clusters_scatter.png", dpi=130); plt.close()

plt.figure(figsize=(6, 4))
perfil["Precio_mediano"].plot(kind="bar", color=[colores[s] for s in perfil.index])
plt.title("Precio mediano por segmento (USD)"); plt.xlabel("")
plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig("grafico_9_precio_por_segmento.png", dpi=130); plt.close()
print("Listo")
