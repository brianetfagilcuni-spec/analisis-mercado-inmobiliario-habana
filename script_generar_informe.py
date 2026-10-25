"""Genera informe/informe_inmobiliario.html con los datos corregidos y los gráficos incrustados."""
import re, base64, datetime
import pandas as pd

df = pd.read_csv("datos_limpios_con_clusters.csv")

n = len(df)
prom, med = df["Precio"].mean(), df["Precio"].median()
pmin, pmax = df["Precio"].min(), df["Precio"].max()
caros = (df["Precio"] > 150000).sum()

z = df.groupby("Zona_Limpia")["Precio"].agg(["median", "count"])
z = z[(z["count"] >= 5) & (z.index != "Otra Zona / No Especificada")].sort_values("median", ascending=False)
zona_top, zona_top_med = z.index[0], z.iloc[0]["median"]
zona_bar, zona_bar_med = z.index[-1], z.iloc[-1]["median"]
tipo_top = df["Tipo_Inmueble"].value_counts().idxmax()
pct_sin_cuartos = (df["Cuartos"] == 0).mean() * 100
gas = (df["Gas"] == "Sí").mean() * 100

def img(ruta):
    with open(ruta, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

secciones = [
 ("1. Precio mediano por zona", "1_precio_por_zona.png",
  f"Entre las zonas con 5 o más anuncios, <b>{zona_top}</b> es la más cara (mediana ${zona_top_med:,.0f}) y <b>{zona_bar}</b> la más barata (${zona_bar_med:,.0f}). Se usa la mediana porque unos pocos anuncios de lujo distorsionan el promedio."),
 ("2. Distribución de precios", "6_distribucion_precios.png",
  f"La mayoría de los anuncios está entre $5,000 y $50,000. Hay una cola pequeña de propiedades de más de $200,000."),
 ("3. Tipo de inmueble", "3_tipo_inmueble.png", f"El tipo más anunciado es <b>{tipo_top}</b>."),
 ("4. Servicios mencionados", "4_servicios.png",
  f"El gas de la calle es el servicio más citado ({gas:.0f}% de los anuncios). Ningún anuncio menciona internet."),
 ("5. Características", "5_caracteristicas.png", "Terraza y entrada independiente son lo que más destacan los vendedores."),
 ("6. Categoría de precio", "2_categoria_precio.png", "Reparto de anuncios según la categoría asignada en la limpieza de datos."),
 ("7. Clustering: método del codo", "7_codo.png", "La inercia baja con claridad hasta k=3, por eso se eligieron 3 grupos."),
 ("8. Clustering: segmentos", "8_clusters_scatter.png",
  f"Los grupos separan sobre todo el <b>nivel de detalle</b> del anuncio: el {pct_sin_cuartos:.0f}% no indica cuántos cuartos tiene. Aparece además un grupo pequeño de casas de lujo (6 o más cuartos)."),
 ("9. Precio por segmento", "9_precio_por_segmento.png", "Mediana de precio de cada grupo."),
]

bloques = "".join(
    f'<div class="card"><h2>{t}</h2><img src="{img("grafico_"+f)}" alt="{t}"><div class="concl">{c}</div></div>'
    for t, f, c in secciones)

perfil = pd.read_csv("datos_limpios_perfil_clusters.csv")
tabla = "<table><tr>" + "".join(f"<th>{c}</th>" for c in perfil.columns) + "</tr>" + "".join(
    "<tr>" + "".join(f"<td>{v:,.1f}</td>" if isinstance(v, float) else f"<td>{v}</td>" for v in fila) + "</tr>"
    for fila in perfil.itertuples(index=False)) + "</table>"

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Informe Mercado Inmobiliario La Habana</title>
<style>
body{{font-family:Arial,sans-serif;background:#f4f6f9;color:#2c3e50;margin:0;padding:12px;line-height:1.5}}
.w{{max-width:900px;margin:auto}}
header{{background:linear-gradient(135deg,#1e3c72,#2a5298);color:#fff;padding:20px;border-radius:12px;text-align:center;margin-bottom:16px}}
header h1{{font-size:1.4em;margin:0 0 6px}} header p{{margin:2px 0;font-size:.85em;opacity:.9}}
.k{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:16px}}
.k div{{background:#fff;border-left:4px solid #2a5298;border-radius:8px;padding:12px;text-align:center}}
.k b{{display:block;font-size:1.3em;color:#1e3c72}} .k span{{font-size:.75em;color:#7f8c8d;text-transform:uppercase}}
.card{{background:#fff;border-radius:12px;padding:16px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.card h2{{font-size:1.05em;color:#1e3c72;margin:0 0 10px;border-bottom:2px solid #ecf0f1;padding-bottom:6px}}
img{{max-width:100%;height:auto;display:block;margin:auto}}
.concl{{background:#eaf3fb;border-left:4px solid #2a5298;padding:10px 12px;border-radius:6px;margin-top:10px;font-size:.9em}}
table{{width:100%;border-collapse:collapse;font-size:.85em}} th,td{{padding:6px;border-bottom:1px solid #ecf0f1;text-align:left}} th{{background:#f8f9fa}}
.warn{{background:#fff8e6;border-left:4px solid #f39c12}}
footer{{text-align:center;font-size:.8em;color:#7f8c8d;padding:12px}}
</style></head><body><div class="w">
<header><h1>Informe del Mercado Inmobiliario</h1>
<p>La Habana, Cuba · {n} anuncios de venta de Revolico</p>
<p>Datos corregidos · Generado el {datetime.date.today():%d/%m/%Y}</p></header>
<div class="k">
<div><b>{n}</b><span>Anuncios</span></div>
<div><b>${med:,.0f}</b><span>Precio mediano</span></div>
<div><b>${prom:,.0f}</b><span>Precio promedio</span></div>
<div><b>${pmin:,.0f}</b><span>Mínimo</span></div>
<div><b>${pmax:,.0f}</b><span>Máximo</span></div>
<div><b>{caros}</b><span>Más de $150k</span></div></div>
<div class="card warn"><h2>Corrección de datos</h2>
La versión anterior del informe tenía errores de precio (por ejemplo 560,000 USD cuando el anuncio decía 60,000). Aquí el precio se toma del texto original del anuncio y se descartan precios menores a 1,000 USD. Por eso el promedio baja de $159,776 a ${prom:,.0f}.</div>
{bloques}
<div class="card"><h2>Perfil de los segmentos (K-Means, k=3)</h2>{tabla}</div>
<div class="card warn"><h2>Limitaciones</h2>
Muestra pequeña ({n} anuncios, una sola extracción). Varias zonas tienen muy pocos anuncios. La zona se leyó del texto del anuncio y algunos de Guanabo aparecen como Playa. Los precios son de oferta, no de cierre. Hay anuncios duplicados.</div>
<footer>Proyecto de Ciencia de Datos · Fuente: Revolico.com</footer>
</div></body></html>"""
open("informe_inmobiliario.html", "w", encoding="utf-8").write(html)
print("Informe generado")
