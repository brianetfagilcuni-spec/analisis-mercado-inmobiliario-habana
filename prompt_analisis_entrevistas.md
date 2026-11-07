# Prompt para analizar entrevistas y notas de audio

Úsalo con un asistente de IA. Antes: quita nombres y teléfonos. Si tienes un audio, primero hay que pasarlo a texto: WhatsApp puede transcribir notas de voz en algunas versiones (Ajustes > Chats > Transcripciones de mensajes de voz), o usa una app de voz a texto. Revisa la transcripción por encima antes de analizarla.

## Prompt
```
Eres analista de investigación cualitativa. Te paso entrevistas a
inmobiliarias de La Habana sobre la venta de casas. Cada entrevista tiene
un código (INM1, INM2...) y puede ser una transcripción de audio.

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
- Si la transcripción tiene partes dudosas o ininteligibles, márcalas con [dudoso]
  y no las interpretes.
- Separa hechos, opiniones y estimaciones.
- No completes con conocimiento externo ni generalices a todo el mercado.

Al final agrega:
A) Coincidencias entre entrevistas.
B) Contradicciones o diferencias.
C) Afirmaciones que solo dice una entrevista (más débiles).
D) Tres preguntas de seguimiento que valdría la pena hacer.
```

## Después del análisis
1. Compara cada fila con lo que dice el audio o el chat; corrige lo que no coincida.
2. Pasa las respuestas al formato del repositorio: cifras a `inmobiliarias.csv` (con el rango en `notas`) y texto libre a `respuestas_cualitativas.csv`.
3. Ejecuta `python codigo/entrevistas_analisis.py` para actualizar los gráficos.
4. Actualiza `catalogo_inmobiliarias.md` y, si cambia algo, el capítulo 6 de `historia/historia.md`.
