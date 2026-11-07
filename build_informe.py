import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib.utils import ImageReader

F = ""
aud = pd.read_csv(F + "datos/limpios/inmuebles_auditados.csv")
res = pd.read_csv(F + "datos/limpios/auditoria_resumen.csv").set_index("indicador")["valor"]
perfil = pd.read_csv(F + "datos/limpios/perfil_clusters.csv")
tri = pd.read_csv(F + "datos/limpios/triangulacion.csv")
cl = pd.read_csv(F + "datos/limpios/con_clusters.csv")
P = pd.read_csv("entrevistas/personas.csv")
INM = pd.read_csv("entrevistas/inmobiliarias.csv")
def cnt(col, letra):
    r = P[col].dropna().astype(str); r = r[r != ""]
    return int(r.str.contains(letra).sum()), len(r)
c_serv, n1 = cnt("p1_valora", "C"); c_ubic, _ = cnt("p1_valora", "A"); c_prec, _ = cnt("p1_valora", "B"); c_todas, _ = cnt("p1_valora", "T")
c_veda, n2 = cnt("p2_zona_cara", "B"); c_playa, _ = cnt("p2_zona_cara", "A")
c_casa, n3 = cnt("p3_tipo", "A")
c_agua, n4 = cnt("p4_servicio", "A"); c_luz, _ = cnt("p4_servicio", "B"); c_gas, _ = cnt("p4_servicio", "C")
c_sub, n5 = cnt("p5_precios", "A"); c_baj, _ = cnt("p5_precios", "B"); c_est, _ = cnt("p5_precios", "C")
NPERS = len(P)

p = aud["Precio_corregido"]; n = len(aud)
q1, med, q3 = p.quantile(.25), p.median(), p.quantile(.75)
serv = {k: (cl[k] == "Sí").mean() * 100 for k in ["Agua", "Luz", "Gas", "Teléfono", "Internet"]}
sin_cuartos = (cl["Cuartos"] == 0).mean() * 100
tipo = cl.groupby("Tipo_Inmueble")["Precio"].agg(["median", "count"]).sort_values("median")
mun = aud.groupby("Municipio")["Precio_corregido"].agg(["median", "count"])
mun = mun[mun["count"] >= 3].sort_values("median", ascending=False)

AZUL = colors.HexColor("#1e3c72")
ss = getSampleStyleSheet()
cuerpo = ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=AZUL, spaceBefore=14, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=AZUL, spaceBefore=10, spaceAfter=5)
peq = ParagraphStyle("peq", parent=cuerpo, fontSize=8.5, leading=11, alignment=0, spaceAfter=0)
cap = ParagraphStyle("cap", parent=cuerpo, fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=10)
nota = ParagraphStyle("nota", parent=cuerpo, fontSize=9, leading=12.5, backColor=colors.HexColor("#fff8e6"),
                      borderColor=colors.HexColor("#f39c12"), borderWidth=0.8, borderPadding=6, spaceBefore=6, spaceAfter=10)
bul = ParagraphStyle("bul", parent=cuerpo, leftIndent=14, bulletIndent=3, spaceAfter=3, alignment=0)

historia = []
def H1(t): historia.append(Paragraph(t, h1))
def H2(t): historia.append(Paragraph(t, h2))
def Pp(t): historia.append(Paragraph(t, cuerpo))
def B(t): historia.append(Paragraph(t, bul, bulletText="-"))
def NOTA(t): historia.append(Paragraph(t, nota))
def sp(h=6): historia.append(Spacer(1, h))
nfig = [0]
def FIG(archivo, texto, ancho=14.5):
    w, h = ImageReader(F + archivo).getSize()
    nfig[0] += 1
    historia.append(KeepTogether([Image(F + archivo, width=ancho * cm, height=ancho * cm * h / w),
                                  Paragraph(f"Figura {nfig[0]}. {texto}", cap)]))
ntab = [0]
def TAB(filas, anchos, titulo):
    ntab[0] += 1
    datos = [[Paragraph(str(c), peq) for c in fila] for fila in filas]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef8"))]))
    historia.append(Paragraph(f"<b>Tabla {ntab[0]}.</b> {titulo}", ParagraphStyle("tt", parent=cuerpo, fontSize=9, alignment=0, spaceAfter=3, keepWithNext=1)))
    historia.append(t); sp(10)
f0 = lambda x: f"{x:,.0f}"

# ===== portada =====
historia += [Spacer(1, 4.5 * cm),
  Paragraph("Universidad de La Habana<br/>Facultad de Matemática y Computación<br/>Ciencia de Datos, primer año",
            ParagraphStyle("u", parent=cuerpo, alignment=TA_CENTER, fontSize=11, textColor=colors.HexColor("#555555"))),
  Spacer(1, 2.2 * cm),
  Paragraph("Informe técnico", ParagraphStyle("t0", parent=cuerpo, alignment=TA_CENTER, fontSize=13, textColor=AZUL)),
  Spacer(1, .4 * cm),
  Paragraph("El mercado inmobiliario de venta de viviendas en La Habana", ParagraphStyle("t1", parent=cuerpo, alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=AZUL)),
  Spacer(1, .4 * cm),
  Paragraph("Anuncios de Revolico, entrevistas a personas e inmobiliarias, y auditoría de datos",
            ParagraphStyle("t2", parent=cuerpo, alignment=TA_CENTER, fontSize=12, leading=16)),
  Spacer(1, 3.5 * cm),
  Paragraph("<b>Autor:</b> Brianet Fagil Cuni<br/><b>Fecha:</b> noviembre de 2026<br/><b>Repositorio:</b> github.com/brianetfagilcuni-spec/analisis-mercado-inmobiliario-habana",
            ParagraphStyle("a", parent=cuerpo, alignment=TA_CENTER, fontSize=10.5, leading=16)),
  Spacer(1, 2 * cm),
  Paragraph("Datos de las entrevistas al corte de noviembre de 2026.", ParagraphStyle("cz", parent=cuerpo, alignment=TA_CENTER, fontSize=9.5, textColor=colors.HexColor("#555555"))),
  PageBreak()]

# ===== resumen =====
H1("Resumen")
Pp(f"Este trabajo analiza el mercado de venta de viviendas en La Habana a partir de {n} anuncios de Revolico, una segunda extracción de "
   f"{int(tri.iloc[1]['n'])} anuncios válidos y entrevistas a personas e inmobiliarias. El primer hallazgo es metodológico: el 17% de los precios "
   f"extraídos automáticamente ({int(res.iloc[1])} de {n}) era erróneo, lo que inflaba el precio promedio de ${f0(res.iloc[8])} a ${f0(res.iloc[7])} USD. "
   f"Con los precios corregidos, la mediana es de <b>${f0(med)} USD</b>, con la mitad central de los anuncios entre ${f0(q1)} y ${f0(q3)}. "
   f"Por municipio, los más caros son {mun.index[0]}, {mun.index[1]} y {mun.index[2]}; los más baratos con 5 o más anuncios, Arroyo Naranjo y Centro Habana.")
Pp(f"Se entrevistó a {NPERS} personas y a 5 inmobiliarias o gestoras. El clustering K-Means separa los anuncios sobre todo por su nivel de detalle y aísla un pequeño grupo de casas de lujo. Las entrevistas coinciden con "
   "los anuncios en las zonas caras y baratas y señalan una rebaja cercana al 10% entre precio publicado y de cierre. También revelan una "
   "contradicción: las inmobiliarias dicen que la emigración es el motivo principal de venta, pero ningún anuncio la menciona.")
Pp("Durante el estudio se publicó la nueva Ley de la Vivienda (Ley 187/2026), que según la prensa reconoce la actividad inmobiliaria y exige pagos bancarios en la compraventa. Los anuncios analizados son anteriores a la ley.")

# ===== 1 =====
H1("1. Introducción y objetivos")
Pp("El mercado inmobiliario cubano se ha reactivado en los últimos años, pero casi no existen estadísticas oficiales públicas. Los anuncios en línea y "
   "la experiencia de gestores y compradores son hoy las fuentes más accesibles. Este proyecto pregunta: <b>¿cuánto cuesta una vivienda en La Habana, "
   "qué factores influyen y qué tan fiable es lo que muestran los anuncios?</b>")
H2("Objetivo general")
Pp("Caracterizar el mercado de venta de viviendas en La Habana combinando datos extraídos de Revolico con entrevistas, y evaluar la calidad de esos datos.")
H2("Objetivos específicos")
B("Extraer, limpiar y auditar anuncios de venta de viviendas.")
B("Estimar precios por municipio, tipo de inmueble y servicios, usando estadísticos robustos (mediana).")
B("Segmentar los anuncios con K-Means y valorar si los grupos tienen sentido de mercado.")
B("Contrastar los resultados con la opinión de personas e inmobiliarias.")

# ===== 2 =====
H1("2. Datos")
H2("2.1 Anuncios de Revolico (extracción 1)")
Pp(f"Se extrajeron {n} anuncios de venta de casas y apartamentos en La Habana, con título, precio, descripción, servicios mencionados, características "
   f"y enlace. El municipio de cada anuncio es el que muestra la propia plataforma. Los teléfonos presentes en los textos se enmascararon (<i>[tel]</i>) antes de publicar los datos.")
H2("2.2 Segunda extracción (triangulación)")
Pp(f"Una extracción adicional contiene solo título y precio. Tras excluir ofertas de compra, alquileres, gestores y precios menores de 1,000 USD, quedaron "
   f"{int(tri.iloc[1]['n'])} anuncios. No es independiente de la primera: puede contener anuncios repetidos.")
H2("2.3 Entrevistas")
Pp("Se usaron dos instrumentos. A <b>personas</b> que compran o venden vivienda se les aplicó un cuestionario de 5 preguntas de opción múltiple "
   "(valor principal al buscar vivienda, zona más cara, tipo preferido, servicio indispensable y percepción de precios). A <b>inmobiliarias y gestoras</b> se les "
   "envió un cuestionario de 6 preguntas con cifras (zonas, precios de cierre, rebaja, tiempo de venta, servicios, motivos de venta y composición del catálogo) "
   "y, con algunas, una versión de 5 preguntas en texto libre. Las entrevistas a personas se realizaron de dos formas: algunas en persona y otras por WhatsApp, con números de contacto obtenidos de anuncios de Revolico y de grupos de compraventa. El muestreo es por conveniencia. "
   "Las respuestas son anónimas: se identifican con códigos (P01, INM1) y no se guardan nombres ni teléfonos.")

H2("2.4 Fuente institucional: Ley de la Vivienda 187/2026")
Pp("<b>Contexto legal.</b> La Ley 187/2026, de la Vivienda, se publicó en la Gaceta Oficial nº 86 el 14 de octubre de 2026 y entra en vigor el 21 de octubre. Sustituye la ley de 1988. Reconoce a las personas naturales hasta dos viviendas en propiedad, además de una de descanso; exige que la compraventa se formalice ante notario; establece que el pago se haga mediante instrumentos bancarios y elimina la confiscación de la vivienda por salida del país (EFE, 14 de octubre de 2026). La compraventa entre particulares estuvo prohibida durante décadas y se autorizó en 2011. Este estudio se hizo en torno a la publicación de la ley: no mide sus efectos.")
Pp("La extracción de anuncios es anterior a la publicación de la ley (el informe original lleva fecha del 10 de octubre). Algunas entrevistas son posteriores a ella.")

# ===== 3 =====
H1("3. Metodología")
H2("3.1 Corrección de precios")
Pp("La columna de precio numérico del conjunto limpio tenía errores de extracción: dígitos pegados de más (por ejemplo, 560,000 cuando el anuncio decía 60,000) "
   "y valores absurdos (de 1 a 170 USD). Para corregirlo se leyó el precio escrito en el texto del anuncio mediante una expresión regular (número seguido de USD) "
   f"y se descartaron valores menores de 1,000 USD. Se corrigieron {int(res.iloc[1])} de {n} anuncios.")
H2("3.2 Auditoría de calidad")
Pp("Se revisaron cuatro problemas: precios corregidos, zona inconsistente con el municipio de Revolico, anuncios sin descripción (solo teléfono) y anuncios casi "
   "duplicados (mismo municipio y mismo texto). Cada anuncio recibió una marca por problema, y se evaluó cuánto cambian los resultados al quitarlos.")
H2("3.3 Estadísticos")
Pp("Dado que unos pocos anuncios de lujo (hasta 750,000 USD) distorsionan el promedio, el análisis se apoya en la <b>mediana</b> y los cuartiles. "
   "Los municipios con menos de 3 anuncios no se interpretan.")
H2("3.4 Clustering")
Pp("Se aplicó K-Means (implementado con NumPy) sobre cuatro variables estandarizadas: logaritmo del precio, cuartos, baños y cantidad de servicios o características "
   "mencionadas. El método del codo sugirió k = 3. Con 20 inicializaciones aleatorias se conservó la de menor inercia.")
H2("3.5 Tratamiento de las entrevistas")
Pp("Las respuestas de opción múltiple se codificaron con letras. Cuando una persona marcó varias opciones (por ejemplo, AB) se contó una vez cada opción, y "
   "&quot;todas&quot; se codificó aparte. Las preguntas sin respuesta quedan en blanco y cada resultado se calcula sobre quienes respondieron esa pregunta.")

H2("3.6 Herramientas, entorno de trabajo y uso de inteligencia artificial")
Pp("<b>Todo el proyecto se realizó desde un teléfono Android</b>, sin computadora. Las herramientas fueron:")
Pp("<b>Programación y análisis.</b> Python en <b>PyDroid 3</b> (y Termux para comandos y Git), con las bibliotecas pandas, NumPy, SciPy, matplotlib, requests y ReportLab. "
   "Con ellas se hicieron el scraping, la limpieza, la auditoría, el clustering, las pruebas estadísticas, los gráficos y los informes en PDF y HTML.")
Pp("<b>Recolección de datos.</b> Revolico (anuncios de venta), WhatsApp y entrevistas en persona (personas e inmobiliarias), Google Forms y Google Sheets (encuesta y registro de respuestas) y Facebook (evidencia fotográfica de anuncios de una inmobiliaria).")
Pp("<b>Publicación y control de versiones.</b> GitHub como repositorio y control de versiones.")
Pp("<b>Inteligencia artificial.</b> Se usaron asistentes de IA (entre ellos Claude) como apoyo para organizar el repositorio, escribir y revisar scripts, calcular las pruebas estadísticas, "
   "redactar la historia y este informe, y buscar prensa sobre la Ley de la Vivienda. El prompt usado para diseñar la guía de entrevistas está en <i>entrevistas/prompt_diseno_guia.md</i> y el que sirve para analizar las respuestas, en <i>entrevistas/prompt_analisis_entrevistas.md</i>. "
   "La definición del problema, la recolección de los anuncios, las entrevistas y la revisión de cada cifra son de la autora. Se descartó todo contenido propuesto por la IA que no coincidía con los datos reales.")
Pp("<b>Control de calidad.</b> Catorce pruebas automáticas (<i>tests/test_datos.py</i>, con unittest) comprueban que hay 92 anuncios, que la mediana corregida es 25,000 USD, que los precios son válidos, que los códigos de las entrevistas son los esperados, que no hay teléfonos reales en los archivos y que la historia tiene 30 preguntas con todas sus imágenes.")

# ===== 4 =====
H1("4. Resultados: anuncios de Revolico")
H2("4.1 Precios")
Pp(f"La mediana es de ${f0(med)} USD y el promedio de ${f0(p.mean())}. Los anuncios van de ${f0(p.min())} a ${f0(p.max())}. La Figura 1 muestra por qué el promedio "
   f"no es fiable: al corregir los errores baja de ${f0(res.iloc[7])} a ${f0(res.iloc[8])}, mientras que la mediana casi no se mueve "
   f"(${f0(res.iloc[9])} sin corregir, ${f0(res.iloc[10])} corregida, ${f0(res.iloc[11])} sin duplicados).")
FIG("graficos/grafico_12_sensibilidad.png", "La mediana es estable ante las correcciones; el promedio no.", 11.5)
H2("4.2 Precios por municipio")
TAB([["Municipio", "Mediana (USD)", "Anuncios"]] + [[i, f0(r["median"]), int(r["count"])] for i, r in mun.iterrows()], [7, 4, 3],
    "Precio mediano por municipio de Revolico (municipios con 3 o más anuncios).")
FIG("graficos/grafico_10_municipio.png", "Precio mediano por municipio.", 12.5)
Pp("Los municipios más caros son Plaza de la Revolución (que incluye el Vedado), Habana del Este (que incluye Guanabo, zona de playa) y Playa. Diez de Octubre queda en un "
   "nivel intermedio y es heterogéneo. Centro Habana, Cerro y Arroyo Naranjo están entre los más baratos.")
H2("4.3 Tipo de inmueble, servicios y características")
TAB([["Tipo de inmueble", "Mediana (USD)", "Anuncios"]] + [[i, f0(r["median"]), int(r["count"])] for i, r in tipo.iloc[::-1].iterrows()], [7, 4, 3],
    "Precio mediano por tipo de inmueble (Finca y Otro tienen un solo anuncio).")
Pp(f"Los servicios más mencionados son el gas de la calle ({serv['Gas']:.0f}% de los anuncios), el teléfono fijo ({serv['Teléfono']:.0f}%), el agua ({serv['Agua']:.0f}%) y la luz "
   f"({serv['Luz']:.0f}%). Ningún anuncio menciona internet. Además, el {sin_cuartos:.0f}% de los anuncios no indica cuántos cuartos tiene, lo que limita cualquier análisis por tamaño.")
H2("4.4 Auditoría de datos")
TAB([["Indicador", "Valor"]] + [[k, f0(v)] for k, v in res.items()], [11, 3], "Resumen de la auditoría de calidad de los 92 anuncios.")
FIG("graficos/grafico_11_auditoria.png", "Problemas de calidad detectados.", 9.5)
Pp("La zona deducida del texto del anuncio no coincidió con el municipio de Revolico en 10 casos (por ejemplo, anuncios de Guanabo clasificados como Playa) y 13 anuncios quedaron "
   "sin zona. Por eso el análisis geográfico se basa en el municipio de la plataforma.")
H2("4.5 Segmentación con K-Means")
filas = [["Segmento", "Anuncios", "Precio mediano (USD)", "Cuartos", "Baños", "Extras"]]
for _, r in perfil.iterrows():
    filas.append([r["Segmento"], int(r["Anuncios"]), f0(r["Precio_mediano"]), f"{r['Cuartos']:.1f}", f"{r['Banos']:.1f}", f"{r['Extras']:.1f}"])
TAB(filas, [3.6, 2.2, 3.8, 2.2, 2.2, 2.2], "Perfil de los tres segmentos (promedios por grupo).")
FIG("graficos/grafico_8_clusters_scatter.png", "Segmentos de anuncios según servicios mencionados y precio (escala logarítmica).", 12)
Pp("Los grupos no representan tipos de mercado sino, sobre todo, el nivel de detalle del anuncio: el grupo &quot;Poco detallado&quot; casi no informa cuartos ni baños, mientras que "
   "&quot;Detallado&quot; sí lo hace. El tercero agrupa cinco casas de lujo (6 o más cuartos, mediana de 600,000 USD). Esto es un resultado útil por sí mismo: advierte que "
   "la calidad de la información del anuncio condiciona el análisis.")
H2("4.6 Triangulación con la segunda extracción")
filas = [["Fuente", "n", "P25", "Mediana", "P75", "Promedio"]]
for _, r in tri.iterrows():
    filas.append([r["fuente"], int(r["n"]), f0(r["p25"]), f0(r["mediana"]), f0(r["p75"]), f0(r["promedio"])])
TAB(filas, [6.4, 1.4, 2, 2.2, 2, 2.2], "Comparación de estadísticos entre las dos extracciones (USD).")
Pp(f"La segunda extracción da una mediana de ${f0(tri.iloc[1]['mediana'])} USD, frente a ${f0(tri.iloc[0]['mediana'])} de la primera. Coinciden en el orden de magnitud y en la forma de la distribución "
   "(Figura 5 del anexo C); la diferencia puede deberse a la composición de anuncios, no a un error de medición.")

H2("4.7 Pruebas estadísticas")
est = pd.read_csv("datos/limpios/estadisticas.csv")
filas = [["Comparación (precio publicado)", "n con", "n sin", "Mediana con", "Mediana sin", "p (Mann-Whitney)"]]
for _, r in est.iterrows():
    if str(r["comparacion"]).startswith("Spearman"): continue
    filas.append([r["comparacion"], int(r["n_con"]), int(r["n_sin"]), f0(r["mediana_con"]) if pd.notna(r["mediana_con"]) else "-",
                  f0(r["mediana_sin"]), "n < 5" if pd.isna(r["p_mannwhitney"]) else f"{r['p_mannwhitney']:.3f}"])
TAB(filas, [6.2, 1.3, 1.3, 2.2, 2.2, 2.4], "Comparaciones de precio entre grupos (USD). Prueba de Mann-Whitney; con menos de 5 anuncios en un grupo no se concluye.")
Pp("Se hicieron unas 25 comparaciones; con ese número de pruebas se espera que alguna salga &quot;significativa&quot; por azar, así que los p-valores se usan como orientación y no como prueba definitiva. "
   "La diferencia entre municipios caros (Plaza de la Revolución, Playa y Habana del Este) y el resto es la más clara: medianas de 60,000 y 15,000 USD. "
   "El garaje y el agua parecen asociarse al precio, pero la mayoría de esos anuncios están en zonas caras (garaje) o en zonas baratas (agua), de modo que el efecto se confunde con la zona.")
Pp("La correlación de Spearman entre el precio y los cuartos es 0.56 (39 anuncios que lo indican) y con los baños 0.61 (24 anuncios). Los anuncios que dicen cuartos y baños son los más detallados, así que no representan a todos.")
Pp("Un modelo lineal sobre el logaritmo del precio, solo exploratorio, da un R² ajustado de 0.30 con una variable de zona cara, 0.08 con el tipo de vivienda, 0.01 con el número de servicios mencionados y 0.38 con zona y tipo juntos; añadir los servicios no lo mejora (0.37). "
   "La variable de zona cara se definió después de ver los resultados, por lo que el 0.30 es optimista. Código: <i>codigo/estadisticas.py</i>.")
FIG("graficos/grafico_14_cajas_municipio.png", "Dispersión del precio por municipio (municipios con 5 o más anuncios).", 12)
FIG("graficos/grafico_16_oferta_vs_preferencia.png", "Tipo de vivienda ofertado en Revolico frente al preferido por las personas entrevistadas.", 11)

# ===== 5 =====
H1("5. Resultados: entrevistas")
NOTA(f"<b>Corte de datos.</b> Incluyen {NPERS} personas (una de ellas gestora) y {len(INM)} inmobiliarias o gestoras. Las muestras son pequeñas y por conveniencia: "
     "describen lo que dijeron los entrevistados, no representan a todo el mercado.")
H2("5.1 Personas")
preg = {"p1_valora": ("1. Qué valora más al buscar vivienda", {"A": "Ubicación", "B": "Precio", "C": "Servicios básicos", "D": "Espacio", "T": "Todas"}),
        "p2_zona_cara": ("2. Zona más cara", {"A": "Playa", "B": "Vedado", "C": "Centro Habana", "D": "Otra"}),
        "p3_tipo": ("3. Tipo de inmueble preferido", {"A": "Casa independiente", "B": "Apartamento", "C": "Biplanta"}),
        "p4_servicio": ("4. Servicio indispensable", {"A": "Agua", "B": "Luz", "C": "Gas de la calle", "D": "Internet", "T": "Todos"}),
        "p5_precios": ("5. Percepción de precios", {"A": "Subiendo", "B": "Bajando", "C": "Estables"})}
filas = [["Pregunta", "Respuesta", "Personas", "% de quienes respondieron"]]
for col, (tit, mapa) in preg.items():
    r = P[col].dropna().astype(str); r = r[r != ""]; nr = len(r); primera = True
    for letra, nom in mapa.items():
        c = int(r.str.contains(letra).sum())
        if c:
            filas.append([f"{tit} (n={nr})" if primera else "", nom, c, f"{c / nr * 100:.0f}%"]); primera = False
TAB(filas, [6.2, 4.2, 2, 3.4], "Respuestas de las personas. Una persona puede aportar a más de una opción, por lo que los porcentajes pueden sumar más de 100%.")
Pp(f"La casa independiente es la preferida de la gran mayoría ({c_casa} de {n3}). Como valor principal al buscar vivienda, los servicios básicos son la opción más elegida ({c_serv} de {n1}), por delante de la ubicación ({c_ubic}), "
   f"mientras que el precio solo lo eligió {c_prec} {'persona' if c_prec == 1 else 'personas'}; otras {c_todas} dicen que todo importa. El agua es el servicio indispensable más citado ({c_agua} de {n4}), seguida del gas ({c_gas}) y la luz ({c_luz}). "
   f"{'Sobre la zona más cara hay empate técnico entre el Vedado' if abs(c_veda - c_playa) <= 2 else 'Se considera más cara la zona del ' + ('Vedado' if c_veda > c_playa else 'Playa') + ', frente a'} ({c_veda} de {n2}) y Playa ({c_playa} de {n2}). La percepción de precios se inclina hacia que están subiendo ({c_sub} de {n5}), aunque {c_baj} dicen que bajan y {c_est} que se mantienen.")
H2("5.2 Inmobiliarias y gestoras")
TAB([["Código", "Zonas más caras", "Zonas más baratas", "Rebaja", "Tiempo de venta", "Motivo de venta"],
 ["INM1", "Playa, Plaza", "Centro Habana, Diez de Octubre, Cerro", "5% a 15%", "-", "Emigración (principal)"],
 ["INM2", "Playa, Diez de Octubre, Plaza", "San Miguel del Padrón, Cotorro, Regla", "10%", "Más de 12 meses", "Emigración y compra de otra vivienda"],
 ["INM3", "-", "-", "-", "-", "Irse del país o comprar algo mejor"],
 ["INM4", "-", "-", "-", "-", "Reunificación familiar y emigración"],
 ["INM5", "Vedado", "-", "-", "-", "-"]], [1.5, 3.2, 3.8, 1.8, 2.5, 3.6],
 "Resumen de las respuestas de inmobiliarias y gestoras (los guiones indican que no respondieron esa pregunta).")
Pp("Otros datos: INM1 señala que una casa típica en La Habana se cierra entre 18,000 y 30,000 USD, entre 50,000 y 70,000 en Playa y Plaza, y entre 15,000 y 20,000 en Centro Habana, "
   "Diez de Octubre y Cerro. INM3 indica un precio promedio de 40,000 a 180,000 USD según el cliente. El catálogo de INM2 tiene 230 viviendas: 150 casas (65%) y 80 apartamentos (35%). "
   "INM1 y INM3 coinciden en que la mayoría compra para vivir o para alquilar según el caso, y INM1 añade que la inversión para alquilar se ve poco por límites legales y por la caída del turismo. "
   "INM1 cita como problemas documentales frecuentes los títulos desactualizados, las herencias sin declaratoria de herederos y las casas no inscritas en el Registro de la Propiedad.")

# ===== 6 =====
H1("6. Discusión")
B("<b>Zonas.</b> Las inmobiliarias señalan Playa y Plaza como las más caras, y Centro Habana, Cerro, San Miguel, Cotorro y Regla como las más baratas. Los anuncios lo confirman: Plaza, Playa y Habana del Este "
  "(Guanabo) tienen las medianas más altas, y Centro Habana y Cerro, de las más bajas. Diez de Octubre aparece como cara para una inmobiliaria y barata para otra; en los anuncios está en el medio, "
  "lo que sugiere que dentro del municipio hay barrios muy distintos (Víbora, Santos Suárez, Luyanó).")
B("<b>Precio publicado frente a precio de cierre.</b> Las inmobiliarias hablan de una rebaja de 5% a 15% (10% como valor típico). Aplicada a la mediana publicada, el precio de cierre estaría cerca de 22,500 USD (estimación ilustrativa, no medida).")
B("<b>Motivo de venta.</b> Cuatro inmobiliarias mencionan la emigración o la reunificación familiar entre los motivos principales, pero ninguno de los 92 anuncios la menciona según la detección por palabras clave. "
  "El texto del anuncio no refleja por qué se vende, y por eso no sirve para estudiar ese factor.")
B(f"<b>Servicios.</b> Las personas eligen los servicios básicos como valor principal ({c_serv} de {n1}) y el agua como el más indispensable ({c_agua} de {n4}); las inmobiliarias hablan de luz estable, agua constante y gas de la calle. "
  "En los anuncios el gas es lo más citado, y el agua y la luz se mencionan menos. Se anuncia lo que se puede decir con una palabra; la estabilidad del servicio no suele aparecer.")
B("<b>Tiempo de venta.</b> Una inmobiliaria reporta viviendas sin vender desde hace más de un año, y añade que en Plaza y Playa se venden más rápido. Es un solo dato y debe tomarse como indicio.")

B("<b>Marco legal.</b> Varias respuestas encajan con lo que describe la prensa sobre la Ley 187/2026: INM1 menciona el límite legal de viviendas por persona; INM4 menciona el cheque de gerencia como forma de pago, coherente con la exigencia de pagar por vías bancarias; "
  "e INM1 señala como problemas frecuentes los títulos desactualizados y las casas sin inscribir, que se vuelven críticos al exigirse la inscripción registral. Si la ley elimina la confiscación por salida del país, podría cambiar el peso de la emigración como motivo de venta: "
  "es una hipótesis para estudios futuros, no un resultado de este trabajo.")

# ===== 7 =====
H1("7. Limitaciones")
B("Muestra pequeña: 92 anuncios de una sola extracción; varios municipios tienen 1 o 2 anuncios.")
B("Precios de oferta, no de cierre. El precio de cierre solo se conoce por lo que dicen las inmobiliarias.")
B("Sesgo de selección: los anuncios y los contactos para las entrevistas provienen de plataformas y grupos en línea, que no representan a todo el mercado.")
B("Entrevistas por conveniencia, aplicadas en persona y por WhatsApp sin registrar el modo de cada una, lo que puede introducir diferencias; muestras pequeñas; dos versiones del cuestionario para inmobiliarias, por lo que no todas las respuestas son comparables.")
B("Zona y características extraídas del texto con reglas simples; hay errores y datos faltantes (muchos anuncios no indican cuartos).")
B("Anuncios duplicados o casi duplicados; la segunda extracción puede compartir anuncios con la primera.")
B("La Ley 187/2026 entró en vigor el 21 de octubre de 2026: los anuncios son anteriores y parte de las entrevistas se hizo durante o después, por lo que el mercado podría estar cambiando.")
B("El scraper no se probó en un entorno con acceso continuo a internet.")

# ===== 8 =====
H1("8. Conclusiones")
B(f"La calidad de los datos cambia las conclusiones: sin corregir los precios, el promedio parecía de ${f0(res.iloc[7])} USD; corregido, es de ${f0(res.iloc[8])} y la mediana de ${f0(med)}.")
B("La mediana es el estadístico adecuado en este mercado por la presencia de pocos anuncios de lujo y de errores de extracción.")
B("Plaza de la Revolución, Habana del Este (Guanabo) y Playa son las zonas más caras, con medianas de 52,000 a 60,000 USD; Centro Habana, Cerro y Arroyo Naranjo, de 11,000 a 14,000.")
B("Anuncios, personas e inmobiliarias coinciden en el mapa de zonas caras y baratas, y en el peso de los servicios básicos y la casa independiente.")
B("Los anuncios no recogen el motivo de venta ni la estabilidad de los servicios, dos factores que las entrevistas señalan como centrales.")
B("El clustering con las variables disponibles separa la calidad de la información, no segmentos de mercado.")
B("El marco legal cambió durante el estudio (Ley 187/2026): el pago bancario, la inscripción registral y el límite de viviendas pueden afectar precios y plazos, y justifican repetir la medición.")
H2("Trabajo futuro")
B("Ampliar a más extracciones en distintas fechas para medir cambios en el tiempo.")
B("Completar las entrevistas y recoger precios de cierre reales.")
B("Incorporar otra fuente en línea (por ejemplo, grupos de Facebook) y comparar.")

# ===== anexos =====
historia.append(PageBreak())
H1("Anexo A. Cuestionarios")
H2("Personas")
Pp("1. Qué valora más al buscar vivienda: A) ubicación, B) precio, C) servicios básicos (agua, luz, gas), D) espacio.<br/>"
   "2. Zona de La Habana que considera más cara: A) Playa, B) Vedado, C) Centro Habana, D) otra.<br/>"
   "3. Tipo de inmueble preferido: A) casa independiente, B) apartamento, C) biplanta.<br/>"
   "4. Servicio básico indispensable: A) agua, B) luz, C) gas de la calle, D) internet.<br/>"
   "5. Percepción de los precios: A) subiendo, B) bajando, C) estables.")
H2("Inmobiliarias (6 preguntas)")
Pp("1. Zonas más caras y más económicas y precio promedio real de cierre. 2. Porcentaje de rebaja del precio publicado al de cierre. 3. Tiempo promedio de venta en meses. "
   "4. Servicio básico más valorado y aumento aproximado del valor. 5. Motivo de venta: emigración, necesidad de dinero o mudanza (porcentajes). "
   "6. Composición del catálogo: casas, apartamentos y otros (porcentajes).")
H1("Anexo B. Estructura del repositorio")
Pp("El repositorio contiene los datos crudos y limpios (<i>datos_*</i>), los gráficos (<i>graficos/grafico_*</i>), los scripts de scraping, limpieza, clustering, auditoría y generación del informe "
   "(<i>codigo/</i>), un cuaderno con el proceso completo (<i>notebook/notebook_analisis.ipynb</i>), el diccionario de datos (<i>datos/diccionario_datos.md</i>), las pruebas automáticas (<i>tests/</i>), la evidencia (<i>evidencia/</i>, con fuentes y fotos de anuncios), el informe en HTML y las entrevistas anonimizadas con su catálogo y cuestionarios (<i>entrevistas/</i>). "
   "El README explica el orden para reproducir los resultados.")
H1("Anexo C. Figura complementaria")
FIG("graficos/grafico_13_triangulacion.png", "Distribución de precios en las dos extracciones de Revolico (escala logarítmica).", 12)
H1("Anexo E. Fuentes consultadas")
Pp("EFE, &quot;Cuba publica nueva Ley de Vivienda que permite tener hasta dos inmuebles en propiedad&quot;, 14 de octubre de 2026 (Infobae, Swissinfo y Diario Libre).")
Pp("Escambray, &quot;Cuba publica una nueva Ley de la Vivienda: ¿qué cambia?&quot;, octubre de 2026.")
Pp("Periódico Cubano, &quot;Adiós al efectivo: nueva Ley de Vivienda en Cuba cambia las reglas de la compraventa&quot;, octubre de 2026.")
Pp("Directorio Cubano, &quot;Cuba publica una nueva Ley de la Vivienda: estos son los cambios para los propietarios&quot;, 14 de octubre de 2026.")
Pp("La República, &quot;Cuba autoriza compraventa de casas&quot;, 4 de noviembre de 2011 (EFE).")
Pp("Nota: son fuentes de prensa. El texto oficial está en la Gaceta Oficial de la República de Cuba, edición ordinaria nº 86 (14 de octubre de 2026).")

historia.append(PageBreak())
H1("Anexo D. Procedimiento paso a paso")
Pp("El proceso se hizo en el orden siguiente. Cada paso indica el código que lo ejecuta y los archivos que produce, para que se pueda revisar y reproducir.")
pasos = [
 ("1. Recolección de anuncios.", "Se extrajeron 92 anuncios de venta de Revolico con <i>codigo/scraping_revolico.py</i>. Resultado: <i>datos/crudos/revolico_completo.csv</i>. Los teléfonos se enmascararon como [tel] antes de publicar."),
 ("2. Segunda extracción.", "Una extracción de solo título y precio (<i>datos/crudos/revolico_casas.csv</i>). Se excluyeron ofertas de compra, alquileres, gestores y precios menores de 1,000 USD, y quedaron 78 anuncios."),
 ("3. Corrección de precios.", "El precio numérico original tenía errores. Se leyó el precio escrito en el texto de cada anuncio. Resultado: 16 precios corregidos (<i>datos/limpios/inmuebles_auditados.csv</i>)."),
 ("4. Auditoría de calidad.", "Se revisaron la zona frente al municipio de Revolico, los anuncios sin descripción, los casi duplicados y las zonas sin asignar. Código: <i>codigo/auditoria.py</i>. Resumen: <i>datos/limpios/auditoria_resumen.csv</i>."),
 ("5. Estadística descriptiva.", "Se calcularon medianas, cuartiles y promedios por municipio y tipo de inmueble. Gráficos 1 a 6 con <i>codigo/graficos.py</i>. La sensibilidad de la mediana y el promedio está en el gráfico 12. Las pruebas estadísticas (Mann-Whitney, Spearman, regresión sobre el logaritmo del precio) están en <i>codigo/estadisticas.py</i> y sus resultados en <i>datos/limpios/estadisticas.csv</i>."),
 ("6. Clustering.", "K-Means implementado con NumPy, con cuatro variables estandarizadas. El método del codo sugirió k = 3, con 20 inicializaciones. Código: <i>codigo/clustering.py</i>. Resultados: <i>datos/limpios/con_clusters.csv</i> y <i>perfil_clusters.csv</i>."),
 ("7. Entrevistas a personas.", "Cuestionario de 5 preguntas, codificado con letras. Se cargaron con <i>codigo/entrevistas_cargar_respuesta.py</i> en <i>entrevistas/personas.csv</i> (35 personas). El análisis, con <i>codigo/entrevistas_analisis.py</i>, produce los gráficos de <i>graficos/entrevistas/</i>."),
 ("8. Entrevistas a inmobiliarias y gestoras.", "Datos numéricos en <i>entrevistas/inmobiliarias.csv</i>, respuestas de texto libre en <i>entrevistas/respuestas_cualitativas.csv</i>. Cuando una respuesta era un rango, se usó el punto medio y se anotó en la columna de notas."),
 ("9. Triangulación.", "Comparación entre las dos extracciones (<i>datos/limpios/triangulacion.csv</i>, gráfico 13). Las dos muestras no son independientes."),
 ("10. Integración.", "Se contrastaron los anuncios, las personas y las inmobiliarias. Los hallazgos están en la historia (<i>historia/historia.md</i>)."),
 ("11. Informes.", "<i>codigo/generar_informe.py</i> produce <i>informe/informe_inmobiliario.html</i>. <i>codigo/informe_pdf/build_informe.py</i> produce este informe, y <i>build_historia.py</i> produce la historia en PDF."),
 ("12. Verificación.", "Se comprobó que no hay teléfonos en los archivos publicados, que cada cifra del texto sale de un archivo de datos, y que los scripts se ejecutan desde la raíz del repositorio en el orden indicado en el README."),
]
for titulo, cuerpo_txt in pasos:
    Pp("<b>" + titulo + "</b> " + cuerpo_txt)

def pie(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2.2 * cm, 1.3 * cm, "Informe técnico - Mercado inmobiliario de venta de viviendas en La Habana")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, f"Página {doc.page}")
    canvas.restoreState()
doc = BaseDocTemplate("informe/informe_tecnico.pdf", pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                      title="Informe técnico: mercado inmobiliario en La Habana", author="Brianet Fagil Cuni")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")], onPage=pie)])
doc.build(historia); print("PDF creado")
