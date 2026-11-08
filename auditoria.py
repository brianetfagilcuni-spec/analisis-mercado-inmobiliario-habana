"""Auditoría de datos de Revolico: precios, duplicados, municipio y comparación con una segunda extracción.
Ejecutar con los archivos de este repositorio en la misma carpeta."""
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("inmuebles_habana_pro.csv")

# ---------- 1. Precio: original vs corregido ----------
def precio_real(txt, fallback):
    m = re.search(r'(\d{1,3}(?:,\d{3})+|\d+)\s*USD', str(txt))
    return float(m.group(1).replace(",", "")) if m else fallback

df["Precio_original"] = df["Precio_Num"]
df["Precio_corregido"] = [precio_real(d, p) for d, p in zip(df["Descripción"], df["Precio_Num"])]
df["flag_precio_corregido"] = df["Precio_original"] != df["Precio_corregido"]

# anuncios con más de un precio distinto escrito en el texto (ambiguos)
def n_precios(txt):
    v = re.findall(r'(\d{1,3}(?:,\d{3})+|\d+)\s*USD', str(txt))
    return len({float(x.replace(",", "")) for x in v})
df["flag_precio_ambiguo"] = df["Descripción"].map(n_precios) > 1

# ---------- 2. Municipio según Revolico (más fiable que la zona deducida del texto) ----------
df["Municipio"] = df["Descripción"].str.extract(r'visitas?\s+([A-Za-zÁÉÍÓÚáéíóúñÑ ]+?),\s*La Habana')[0]
df["Municipio"] = df["Municipio"].replace({"Plaza": "Plaza de la Revolución"})
equiv = {"10 De Octubre": "Diez de Octubre", "Santo Suárez": "Diez de Octubre", "Sevillano": "Diez de Octubre",
         "Vedado": "Plaza de la Revolución", "San Miguel": "San Miguel del Padrón"}
zona_norm = df["Zona_Limpia"].replace(equiv)
df["flag_zona_distinta"] = (zona_norm != df["Municipio"]) & (df["Zona_Limpia"] != "Otra Zona / No Especificada")
df["flag_zona_sin_asignar"] = df["Zona_Limpia"] == "Otra Zona / No Especificada"

# ---------- 3. Duplicados y anuncios sin detalle ----------
def cuerpo(t):
    t = str(t); i = t.find("Guardar Más"); t = t[i + 11:] if i >= 0 else t
    t = re.sub(r'\[tel\]|\d+', '#', t.lower())
    t = re.sub(r'publicidad|llamar|whatsapp', '', t)      # texto repetido de la plataforma
    t = re.sub(r'[^a-záéíóúñ# ]', '', t)
    return re.sub(r'\s+', ' ', t).strip()[:60]

df["_clave"] = df["Descripción"].map(cuerpo)
df["flag_sin_detalle"] = df["_clave"].str.replace("#", "").str.strip().str.len() < 25
con_texto = ~df["flag_sin_detalle"]
df["flag_duplicado"] = con_texto & df.duplicated(["Municipio", "_clave"], keep="first")

# ---------- 4. Resumen de auditoría ----------
n = len(df)
base = df["Precio_corregido"]
sin_dup = df[~df["flag_duplicado"]]["Precio_corregido"]
resumen = pd.DataFrame([
 ("Anuncios analizados", n),
 ("Precios corregidos (el CSV tenía un valor distinto al del anuncio)", int(df["flag_precio_corregido"].sum())),
 ("Anuncios con más de un precio distinto en el texto", int(df["flag_precio_ambiguo"].sum())),
 ("Anuncios con zona distinta al municipio de Revolico", int(df["flag_zona_distinta"].sum())),
 ("Anuncios con zona sin asignar ('Otra zona')", int(df["flag_zona_sin_asignar"].sum())),
 ("Anuncios casi duplicados (mismo texto y municipio)", int(df["flag_duplicado"].sum())),
 ("Anuncios sin descripción (solo teléfono)", int(df["flag_sin_detalle"].sum())),
 ("Precio promedio original (USD)", round(df["Precio_original"].mean())),
 ("Precio promedio corregido (USD)", round(base.mean())),
 ("Precio mediano original (USD)", df["Precio_original"].median()),
 ("Precio mediano corregido (USD)", base.median()),
 ("Precio mediano corregido sin duplicados (USD)", sin_dup.median()),
], columns=["indicador", "valor"])
resumen.to_csv("auditoria_resumen.csv", index=False)
print(resumen.to_string(index=False))

# ---------- 5. Guardar dataset auditado (sin descripciones ni teléfonos) ----------
cols = ["Título", "Tipo_Inmueble", "Zona_Limpia", "Municipio", "Precio_original", "Precio_corregido",
        "flag_precio_corregido", "flag_precio_ambiguo", "flag_zona_distinta", "flag_zona_sin_asignar",
        "flag_duplicado", "flag_sin_detalle", "Enlace"]
df[cols].to_csv("inmuebles_auditados.csv", index=False)

azul, rojo = "#2a5298", "#c0392b"

# ---------- 6. Gráfico 10: mediana por municipio ----------
g = df.groupby("Municipio")["Precio_corregido"].agg(["median", "count"])
g = g[g["count"] >= 3].sort_values("median")
plt.figure(figsize=(8, 6))
plt.barh(g.index, g["median"], color=azul)
for i, (v, k) in enumerate(zip(g["median"], g["count"])):
    plt.text(v, i, f" ${v:,.0f} (n={k})", va="center", fontsize=8)
plt.xlim(0, g["median"].max() * 1.3)
plt.title("Precio mediano por municipio de Revolico (USD)\nmunicipios con 3 o más anuncios")
plt.tight_layout(); plt.savefig("grafico_10_municipio.png", dpi=130); plt.close()

# ---------- 7. Gráfico 11: problemas encontrados ----------
prob = pd.Series({
    "Precio corregido": df["flag_precio_corregido"].sum(),
    "Zona distinta al municipio": df["flag_zona_distinta"].sum(),
    "Zona sin asignar": df["flag_zona_sin_asignar"].sum(),
    "Sin descripción": df["flag_sin_detalle"].sum(),
    "Casi duplicados": df["flag_duplicado"].sum(),
    "Precio ambiguo": df["flag_precio_ambiguo"].sum(),
}).sort_values()
plt.figure(figsize=(7, 4.5))
plt.barh(prob.index, prob.values, color=rojo)
for i, v in enumerate(prob.values):
    plt.text(v, i, f" {int(v)} ({v / n * 100:.0f}%)", va="center", fontsize=9)
plt.xlim(0, prob.max() * 1.3)
plt.title(f"Problemas de calidad detectados ({n} anuncios)")
plt.tight_layout(); plt.savefig("grafico_11_auditoria.png", dpi=130); plt.close()

# ---------- 8. Gráfico 12: sensibilidad de la mediana y el promedio ----------
versiones = ["Original\n(sin corregir)", "Corregido", "Corregido\nsin duplicados"]
med = [df["Precio_original"].median(), base.median(), sin_dup.median()]
prom = [df["Precio_original"].mean(), base.mean(), sin_dup.mean()]
x = np.arange(3)
plt.figure(figsize=(7, 4.5))
plt.bar(x - 0.2, med, 0.4, label="Mediana", color=azul)
plt.bar(x + 0.2, prom, 0.4, label="Promedio", color="#e67e22")
for i in range(3):
    plt.text(x[i] - 0.2, med[i], f"{med[i]:,.0f}", ha="center", va="bottom", fontsize=8)
    plt.text(x[i] + 0.2, prom[i], f"{prom[i]:,.0f}", ha="center", va="bottom", fontsize=8)
plt.xticks(x, versiones); plt.ylabel("USD"); plt.legend()
plt.title("La mediana es estable; el promedio no")
plt.tight_layout(); plt.savefig("grafico_12_sensibilidad.png", dpi=130); plt.close()

# ---------- 9. Triangulación con una segunda extracción ----------
c = pd.read_csv("revolico_casas.csv")
c = c[c["Precio"].notna()].copy()
c["Precio"] = pd.to_numeric(c["Precio"], errors="coerce")
excluir = c["Título"].str.contains(r"compro|gestor|renta|pistola|encuentra tu|permuto", case=False, regex=True)
c2 = c[(~excluir) & (c["Precio"] >= 1000) & (c["Precio"] <= 1_000_000)]
descartados = len(c) - len(c2)
a, b = base, c2["Precio"]
tri = pd.DataFrame({
    "fuente": ["Extracción 1 (92 anuncios, con descripción)", "Extracción 2 (solo título y precio)"],
    "n": [len(a), len(b)],
    "p25": [a.quantile(.25), b.quantile(.25)],
    "mediana": [a.median(), b.median()],
    "p75": [a.quantile(.75), b.quantile(.75)],
    "promedio": [a.mean(), b.mean()],
}).round(0)
tri.to_csv("triangulacion.csv", index=False)
print(tri.to_string(index=False), "| descartados de la 2a:", descartados)

plt.figure(figsize=(7, 4.5))
bp = plt.boxplot([a, b], vert=False, widths=.5, patch_artist=True)
for p, col in zip(bp["boxes"], [azul, "#27ae60"]): p.set_facecolor(col); p.set_alpha(.6)
plt.xscale("log")
plt.yticks([1, 2], [f"Extracción 1\n(n={len(a)})", f"Extracción 2\n(n={len(b)})"])
plt.xlabel("Precio USD (escala log)")
plt.title("Triangulación: dos extracciones de Revolico")
plt.tight_layout(); plt.savefig("grafico_13_triangulacion.png", dpi=130); plt.close()
print("Listo")
