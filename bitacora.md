# Bitácora de trabajo (tres semanas)

Registro de cómo se hizo el proyecto, semana por semana. Todo se hizo desde un teléfono Android, con Python en PyDroid 3 (y Termux para comandos y Git) y con apoyo de asistentes de IA. Los días se cuentan dentro de cada semana de trabajo.

## Semana 1 (16 al 22 de octubre): del tema a los primeros datos
| Días | Qué se hizo | Resultado |
|---|---|---|
| 1 y 2 | Definir la pregunta ("¿qué determina el precio de una vivienda en La Habana?"), elegir Revolico como fuente principal y decidir las variables a extraer (precio, zona, tipo, cuartos, servicios, características) | Pregunta y plan de trabajo |
| 3 a 5 | Escribir el scraper en PyDroid 3, extraer los anuncios y enmascarar los teléfonos | `scraping_revolico.py`, `revolico_completo.csv` (92 anuncios) |
| 6 y 7 | Limpieza inicial de los datos y primeros gráficos (precio por zona, rango de precio, tipo de inmueble, servicios y características) | `inmuebles_habana_pro.csv`, gráficos 1 a 6 |

**Aprendizaje de la semana:** el primer promedio daba casi 160,000 USD, una cifra que no tenía sentido. Había que desconfiar de los datos.

## Semana 2 (23 al 29 de octubre): auditar, agrupar y salir a preguntar
| Días | Qué se hizo | Resultado |
|---|---|---|
| 1 y 2 | Auditar los precios contra el texto de cada anuncio; se detectaron y corrigieron 16 precios con errores de extracción; se revisaron zonas, duplicados y anuncios sin descripción | `auditoria.py`, `inmuebles_auditados.csv`, gráficos 11 y 12 |
| 3 | Segunda extracción (título y precio) y comparación con la primera | `revolico_casas.csv`, `triangulacion.csv`, gráfico 13 |
| 4 y 5 | Clustering K-Means con el método del codo (k = 3); se vio que los grupos separan por nivel de detalle del anuncio y no por tipo de mercado | `clustering.py`, `con_clusters.csv`, gráficos 7 a 9 |
| 6 y 7 | Diseñar los cuestionarios (5 preguntas para personas y 6 para inmobiliarias) y empezar las entrevistas por WhatsApp y en persona; usar IA para proponer la guía | `cuestionarios.md`, `prompt_diseno_guia.md` |

**Aprendizaje de la semana:** la mediana es estable y el promedio no; los grupos del clustering reflejan cuánta información da el anuncio.

## Semana 3 (30 de octubre al 6 de noviembre): entrevistas, estadística y documentos
| Días | Qué se hizo | Resultado |
|---|---|---|
| 1 y 2 | Terminar las entrevistas (35 personas y 5 inmobiliarias), codificarlas y anonimizarlas; pedir los catálogos (solo una inmobiliaria lo compartió) | `personas.csv`, `inmobiliarias.csv`, `respuestas_cualitativas.csv` |
| 3 y 4 | Estadística: medianas, Mann-Whitney, Spearman, bootstrap y regresión sobre el logaritmo del precio; gráficos de las entrevistas y de comparación | `estadisticas.py`, `estadisticas*.csv`, gráficos 14 a 16, `entrevistas_analisis.py` |
| 5 | Contexto legal (prensa sobre la Ley 187/2026), evidencia fotográfica y fuentes | `fuentes.md`, `anuncios_fotografias.md` |
| 6 y 7 | Redactar la historia con 30 preguntas, el informe técnico, el diccionario de datos, las pruebas automáticas, el README y el guion de la exposición; revisar cada cifra contra los datos | `historia.md` y `.pdf`, `informe_tecnico.md` y `.pdf`, `diccionario_datos.md`, `test_datos.py` |

**Aprendizaje de la semana:** el barrio explica cerca de un tercio de la variación del precio, y lo que la gente valora (agua, luz) casi no aparece en los anuncios.

## Decisiones y problemas
- **Mediana en lugar de promedio**, porque siete anuncios de más de 150,000 USD arrastraban el promedio.
- **No imputar datos:** donde el anuncio no dice algo (cuartos, estado), se deja como no indicado.
- **Mínimo de 5 anuncios** por grupo para concluir; los municipios con menos se muestran, pero no se interpretan.
- **Privacidad:** teléfonos enmascarados, códigos en lugar de nombres, y catálogos solo de quien quiso compartirlos.
- **Problema:** las inmobiliarias dieron respuestas distintas y parciales; se anotó lo que dijo cada una y no se completaron los vacíos.
- **Problema:** Revolico puede bloquear el acceso en línea; por eso se conservan los datos extraídos en `revolico_completo.csv`.
