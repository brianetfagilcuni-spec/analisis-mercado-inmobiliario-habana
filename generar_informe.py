"""Genera informe_inmobiliario.html con los datos corregidos y los gráficos incrustados."""
import re, base64, datetime
import pandas as pd

df = pd.read_csv("con_clusters.csv")

aud = pd.read_csv("inmuebles_auditados.csv")
res = pd.read_csv("auditoria_resumen.csv").set_index("indicador")["valor"]
tri = pd.read_csv("triangulacion.csv")
gm = aud.groupby("Municipio")["Precio_corregido"].agg(["median", "count"])
gm = gm[gm["count"] >= 5].sort_values("median", ascending=False)
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
 ("Precio mediano por zona (texto del anuncio)", "1_precio_por_zona.png",
  f"Entre las zonas con 5 o más anuncios, <b>{zona_top}</b> es la más cara (mediana ${zona_top_med:,.0f}) y <b>{zona_bar}</b> la más barata (${zona_bar_med:,.0f}). Se usa la mediana porque unos pocos anuncios de lujo distorsionan el promedio. Ojo: esta zona se dedujo del texto y tiene errores (ver auditoría)."),
 ("Precio mediano por municipio de Revolico", "10_municipio.png",
  f"Con el municipio que muestra Revolico en cada anuncio (más fiable), los más caros son <b>{gm.index[0]}</b> (${gm.iloc[0]['median']:,.0f}, n={int(gm.iloc[0]['count'])}), <b>{gm.index[1]}</b> (${gm.iloc[1]['median']:,.0f}, n={int(gm.iloc[1]['count'])}) y <b>{gm.index[2]}</b> (${gm.iloc[2]['median']:,.0f}, n={int(gm.iloc[2]['count'])}); el más barato entre los de 5 o más anuncios es <b>{gm.index[-1]}</b> (${gm.iloc[-1]['median']:,.0f}). Habana del Este incluye Guanabo."),
 ("Distribución de precios", "6_distribucion_precios.png",
  "La mayoría de los anuncios está entre $5,000 y $50,000. Hay una cola pequeña de propiedades de más de $200,000."),
 ("Tipo de inmueble", "3_tipo_inmueble.png", f"El tipo más anunciado es <b>{tipo_top}</b>."),
 ("Servicios mencionados", "4_servicios.png",
  f"El gas de la calle es el servicio más citado ({gas:.0f}% de los anuncios). Ningún anuncio menciona internet."),
 ("Características", "5_caracteristicas.png", "Terraza y entrada independiente son lo que más destacan los vendedores."),
 ("Categoría de precio", "2_categoria_precio.png", "Categorías recalculadas con el precio corregido: Económico (menos de 20k), Medio (20-50k), Alto (50-150k) y Lujo (más de 150k)."),
 ("Clustering: método del codo", "7_codo.png", "La inercia baja con claridad hasta k=3, por eso se eligieron 3 grupos."),
 ("Clustering: segmentos", "8_clusters_scatter.png",
  f"Los grupos separan sobre todo el <b>nivel de detalle</b> del anuncio: el {pct_sin_cuartos:.0f}% no indica cuántos cuartos tiene. Aparece además un grupo pequeño de casas de lujo (6 o más cuartos)."),
 ("Precio por segmento", "9_precio_por_segmento.png", "Mediana de precio de cada grupo."),
 ("Auditoría: problemas de calidad detectados", "11_auditoria.png",
  f"De {n} anuncios, se corrigieron {int(res.iloc[1])} precios, {int(res.iloc[3])} tenían una zona distinta al municipio de Revolico, {int(res.iloc[4])} no tenían zona, {int(res.iloc[6])} no traían descripción y {int(res.iloc[5])} eran casi duplicados."),
 ("Auditoría: estabilidad de los resultados", "12_sensibilidad.png",
  f"La mediana apenas cambia (${res.iloc[9]:,.0f} sin corregir, ${res.iloc[10]:,.0f} corregida y ${res.iloc[11]:,.0f} sin duplicados), pero el promedio baja de ${res.iloc[7]:,.0f} a ${res.iloc[8]:,.0f}. Por eso el análisis se apoya en la mediana."),
 ("Triangulación con una segunda extracción", "13_triangulacion.png",
  f"Una segunda extracción de Revolico (solo título y precio, n={int(tri.iloc[1]['n'])}) da una mediana de ${tri.iloc[1]['mediana']:,.0f}, frente a ${tri.iloc[0]['mediana']:,.0f} de la primera. Coinciden en el orden de magnitud; la diferencia puede deberse a la composición de anuncios. No son muestras independientes: pueden compartir anuncios."),
]

bloques = "".join(
    f'<div class="card"><h2>{i}. {t}</h2><img src="{img("grafico_"+f)}" alt="{t}"><div class="concl">{c}</div></div>'
    for i, (t, f, c) in enumerate(secciones, 1))

perfil = pd.read_csv("perfil_clusters.csv")
tabla = "<table><tr>" + "".join(f"<th>{c}</th>" for c in perfil.columns) + "</tr>" + "".join(
    "<tr>" + "".join(f"<td>{v:,.1f}</td>" if isinstance(v, float) else f"<td>{v}</td>" for v in fila) + "</tr>"
    for fila in perfil.itertuples(index=False)) + "</table>"

tabla_aud = "<table><tr><th>Indicador</th><th>Valor</th></tr>" + "".join(
    f"<tr><td>{k}</td><td>{v:,.0f}</td></tr>" for k, v in res.items()) + "</table>"

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
<div class="card warn"><h2>Corrección de datos (detalle en la auditoría)</h2>
La versión anterior del informe tenía errores de precio (por ejemplo 560,000 USD cuando el anuncio decía 60,000). Aquí el precio se toma del texto original del anuncio y se descartan precios menores a 1,000 USD. Por eso el promedio baja de $159,776 a ${prom:,.0f}.</div>
{bloques}
<div class="card"><h2>Perfil de los segmentos (K-Means, k=3)</h2>{tabla}</div>
<div class="card"><h2>Resumen de la auditoría</h2>{tabla_aud}</div>
<div class="card warn"><h2>Limitaciones</h2>
Muestra pequeña ({n} anuncios, una sola extracción). Varias zonas tienen muy pocos anuncios. La zona se leyó del texto del anuncio y algunos de Guanabo aparecen como Playa. Los precios son de oferta, no de cierre. Hay anuncios casi duplicados. Las entrevistas a personas e inmobiliarias están en proceso y se agregarán de forma anónima. El proceso completo está en <code>notebook_analisis.ipynb</code>.</div>
<footer>Proyecto de Ciencia de Datos · Fuente: Revolico.com</footer>
</div></body></html>"""
open("informe_inmobiliario.html", "w", encoding="utf-8").write(html)
print("Informe generado")
