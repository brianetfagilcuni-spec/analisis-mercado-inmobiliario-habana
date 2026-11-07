# Análisis del mercado inmobiliario en La Habana

**¿Qué determina realmente el precio de una vivienda en La Habana?**

Proyecto de Introducción a la Ciencia de Datos (MatCom, Universidad de La Habana, ICD 26-27). Combina 92 anuncios de venta de Revolico, 5 inmobiliarias y 35 personas entrevistadas.
**Todo el trabajo se hizo desde un teléfono Android**, con Python en PyDroid 3 y con ayuda de inteligencia artificial (ver [Herramientas](#herramientas-y-uso-de-ia)).

## Dónde empezar
| Si quieres... | Abre |
|---|---|
| Leer la historia completa (motivación, 30 preguntas, conclusión) | [`historia/historia.pdf`](historia/historia.pdf) o [`historia/historia.md`](historia/historia.md) |
| Ver cómo se hizo el trabajo (método, herramientas, límites) | [`informe/informe_tecnico.pdf`](informe/informe_tecnico.pdf) |
| Entender cada columna de los datos | [`datos/diccionario_datos.md`](datos/diccionario_datos.md) |
| Ver las entrevistas, los cuestionarios y el catálogo de inmobiliarias | [`entrevistas/`](entrevistas/) |
| Revisar las fuentes y la evidencia | [`evidencia/`](evidencia/) |
| Ver todos los gráficos | [`graficos/`](graficos/README.md) |
| Preparar la exposición | [`presentacion/guion.md`](presentacion/guion.md) |

## Estructura
```
.
├── README.md
├── codigo/              scripts de scraping, auditoría, estadísticas, gráficos, clustering e informes
│   └── informe_pdf/     generadores de los PDF (informe técnico e historia)
├── datos/
│   ├── crudos/          datos tal como salieron del scraping
│   ├── limpios/         datos corregidos, auditados y resúmenes
│   └── diccionario_datos.md
├── entrevistas/         personas, inmobiliarias, cuestionarios, catálogo y prompts
├── evidencia/           fuentes, fotos de anuncios y pendientes
├── graficos/            gráficos en PNG (con índice)
├── historia/            la historia en PDF y MD, y la bitácora de trabajo
├── informe/             informe técnico en PDF e informe en HTML
├── notebook/            cuaderno con el proceso completo
├── presentacion/        guion de la exposición
└── tests/               pruebas automáticas de calidad de los datos
```

## Resultados principales
- **92 anuncios**; precio mediano **25,000 USD**; la mitad central, entre 12,000 y 61,250 USD.
- Se corrigieron **16 precios** (17%) con errores de extracción. El promedio bajó de 159,776 a 66,298 USD; la mediana casi no cambió. Por eso se usa la mediana.
- **El barrio es el factor más claro:** Plaza de la Revolución, Playa y Habana del Este tienen una mediana de 60,000 USD frente a 15,000 en el resto. Una variable de zona explica cerca de 30% de la variación del precio; el número de servicios mencionados, casi nada. Garaje y agua se confunden con la zona.
- **Lo que la gente valora no aparece en los anuncios:** 28 de 35 personas prefieren casa independiente (en Revolico solo 41% son casas) y ponen el agua como servicio indispensable (23 de 34); los anuncios mencionan más el gas y el teléfono. Ninguno de los 92 anuncios menciona la emigración, que 4 de 5 inmobiliarias dan como motivo principal de venta.
- Los anuncios sirven para ubicar niveles de precio, no para tasar una casa concreta.

## Cómo reproducir
Desde la raíz del repositorio (con Python 3 y `pip install -r codigo/requirements.txt`):
```
python codigo/graficos.py
python codigo/clustering.py
python codigo/auditoria.py
python codigo/estadisticas.py
python codigo/entrevistas_analisis.py
python codigo/generar_informe.py
python codigo/informe_pdf/build_informe.py
python codigo/informe_pdf/build_historia.py
python -m unittest discover -s tests -v
```
El scraping (`codigo/scraping_revolico.py`) no se probó en vivo: el sitio puede cambiar. Los datos extraídos están en `datos/crudos/`.

## Pruebas automáticas
`tests/test_datos.py` (14 pruebas con unittest) comprueba que hay 92 anuncios, que la mediana corregida es 25,000 USD, que no hay precios menores a 1,000 USD ni teléfonos reales, que los códigos de las entrevistas son los esperados y que la historia tiene 30 preguntas con todas sus imágenes.

## Herramientas y uso de IA
- **Dispositivo:** teléfono Android. No se usó computadora.
- **Programación:** Python en PyDroid 3 (y Termux para comandos y Git); pandas, NumPy, SciPy, matplotlib, requests y ReportLab.
- **Datos:** Revolico, WhatsApp y entrevistas en persona, Google Forms y Google Sheets, Facebook (fotos de anuncios).
- **Publicación:** GitHub.
- **Inteligencia artificial:** asistentes de IA (entre ellos Claude) como apoyo para organizar el repositorio, escribir y revisar código, calcular estadísticas y redactar documentos. La recolección de datos, las entrevistas y la revisión de las cifras son de la autora. Los prompts están en `entrevistas/`.

## Privacidad
Los teléfonos están enmascarados (`[tel]`). Las entrevistas son anónimas (códigos P01 a P35 e INM1 a INM5). Las fotos son de publicaciones públicas de una inmobiliaria y se retiran si la agencia lo pide.

## Limitaciones
- Muestra pequeña: 92 anuncios de una sola extracción; varios municipios con 5 anuncios o menos.
- Precios de oferta, no de cierre.
- Entrevistas por conveniencia; las inmobiliarias tienen interés comercial y solo una dio cifras de cierre.
- Hay muchas comparaciones estadísticas con grupos pequeños; algunas diferencias "significativas" pueden ser azar.
- La zona se leyó del texto del anuncio y algunos de Guanabacoa aparecen como Playa.
- No hay datos de Facebook ni Telegram.
- Contexto legal tomado de la prensa (Ley 187/2026); falta leer el texto de la Gaceta Oficial.

## Estado
Ver [`evidencia/pendientes.md`](evidencia/pendientes.md).

**Autora:** Brianet Fagil Cuni, estudiante de primer año de Ciencia de Datos.
