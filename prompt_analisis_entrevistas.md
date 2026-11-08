# Prompt para analizar las entrevistas

Se usa con un asistente de inteligencia artificial para ordenar y comparar las respuestas de las entrevistas **sin que invente datos**. Antes de usarlo se quitan nombres y teléfonos: cada persona o inmobiliaria se identifica solo con un código (P01 a P35, INM1 a INM5).

## Prompt ejecutado
```
Eres analista de investigación cualitativa. Te paso entrevistas a
inmobiliarias de La Habana sobre la venta de casas. Cada entrevista tiene
un código (INM1, INM2...).

Devuelve una tabla con una fila por entrevista y estas columnas:
1. Zonas que consideran caras y baratas
2. Precios o rangos mencionados (con la zona)
3. Diferencia entre precio publicado y precio de cierre
4. Factores que dicen que pesan en el precio
5. Motivos de venta
6. Problemas legales o de documentos
7. Plataformas que usan
8. Datos de su catálogo (cantidades, si las dan)

Reglas:
- Usa solo lo que dice el texto. Si algo no se mencionó, escribe "no mencionado".
- Marca con (cita) lo textual y escribe la cita entre comillas, corta.
- Si una cifra es un rango, déjala como rango; no calcules el punto medio.
- Separa hechos, opiniones y estimaciones.
- No completes con conocimiento externo ni generalices a todo el mercado.

Al final agrega:
A) Coincidencias entre entrevistas.
B) Contradicciones o diferencias.
C) Afirmaciones que solo dice una entrevista (más débiles).
D) Tres preguntas de seguimiento que valdría la pena hacer.
```

## Qué se hizo con el resultado
1. Se comparó cada fila de la tabla con las respuestas originales y se corrigió lo que no coincidía.
2. Las cifras se pasaron a `inmobiliarias.csv` (con el rango en la columna `notas`) y el texto libre a `respuestas_cualitativas.csv`.
3. Se ejecutó `entrevistas_analisis.py` para generar los gráficos de las entrevistas.
4. Se actualizaron `catalogo_inmobiliarias.md`, `tabla_entrevistas.md` y el capítulo 6 de la historia.

Las coincidencias y contradicciones que salieron del análisis están en la sección 5 del informe técnico y en el análisis final de la historia.
