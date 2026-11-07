🏠 Análisis Empírico del Mercado Inmobiliario en La Habana: Un Enfoque en Ciencia de Datos

Proyecto de Introducción a la Ciencia de Datos | Facultad de Matemática y Computación (MatCom) - Universidad de La Habana
Autora: Brianet Fagil Cuni (ICD 26-27)

🏆 Hito de Resiliencia Técnica: Este proyecto fue concebido, programado, analizado y documentado íntegramente desde un teléfono Android (utilizando PyDroid 3 y Termux). No se utilizó computadora en ninguna fase.

https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white
https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white
https://img.shields.io/badge/Status-Completado-success?style=for-the-badge

---

📑 Índice de Navegación

1. Abstract
2. Preguntas de Investigación
3. Metodología y Rigor Científico
4. Hallazgos Clave
5. Galería de Visualizaciones
6. Guía del Repositorio
7. Reproducibilidad
8. Control de Calidad

---

1. 📝 Abstract (Resumen Ejecutivo)

Este estudio aborda la problemática del mercado inmobiliario en La Habana. Mediante la triangulación de 3 fuentes de evidencia (scraping web de 92 anuncios, entrevistas a 35 personas y 5 inmobiliarias reales), se construyó un dataset robusto. El análisis revela una profunda brecha entre la oferta publicada y la demanda real: mientras los anuncios priorizan atributos comerciales (gas, teléfono), los compradores priorizan necesidades vitales (agua diaria, estabilidad eléctrica). El estudio emplea estadística no paramétrica y clustering (K-Means) para demostrar que la ubicación explica el 30% de la varianza del precio.

---

2. ❓ Preguntas de Investigación

· Principal: ¿Qué características observables de una vivienda están estadísticamente asociadas a su precio de venta en La Habana?
· Secundarias:
  1. ¿Cuál es el precio mediano real frente al promedio distorsionado por outliers?
  2. ¿Cómo varían las medianas de precios entre los municipios?
  3. ¿Qué características correlacionan con precios altos?
  4. ¿Existe divergencia entre las preferencias del comprador y la oferta?
  5. ¿Se pueden segmentar los anuncios mediante Machine Learning?

---

3. 🧠 Metodología y Rigor Científico

Para asegurar la validez académica, se tomaron decisiones estrictas:

1. Uso de la Mediana sobre el Promedio: El promedio (159,776 USD) era engañoso por 7 propiedades de ultra-lujo. Se adoptó la mediana (25,000 USD) como medida robusta.
2. Auditoría y Cero Imputación: Se auditó manualmente el texto para corregir 16 precios erróneos. No se inventaron datos faltantes.
3. Estadística No Paramétrica: Se utilizó la prueba de Mann-Whitney U para validar diferencias entre zonas, dado que los precios no siguen una distribución normal.
4. Clustering (K-Means): Implementado desde cero (NumPy). Se aplicó logaritmo al precio y estandarización Z-score para evitar sesgos.

---

4. 📊 Hallazgos Clave (El "Qué" y el "Por qué")

· 📍 El Poder de la Ubicación: La zona explica un R² ajustado de ~30%. Zonas premium (Plaza, Playa) triplican la mediana base (60k vs 15k USD).
· 💧 La Paradoja del Agua: El 68% valora el agua diaria. Sin embargo, los anuncios priorizan mencionar el gas y el teléfono. El mercado publica lo fácil, no lo vital.
· ✈️ La Emigración Invisible: 0 de 92 anuncios la mencionan, pero el 80% de las inmobiliarias confirma que es el motor principal del mercado.
· 🏘️ Desajuste Oferta-Demanda: El 80% prefiere casa independiente, pero el 50% de la oferta son apartamentos.
· 👵 El Factor Etario: Los adultos mayores no compran pisos altos, forzando a los vendedores a bajar precios.
· 🚗 El Mito del Garaje: Al analizar intra-zona, se descubre que el garaje no encarece la vivienda; solo es un proxy de "barrio rico".

---

5. 🖼️ Galería de Visualizaciones (Evidencia Gráfica)

Aquí se demuestra visualmente el análisis realizado. (Haz clic en las imágenes para verlas en alta resolución):

Distribución y Medianas por Zona

grafico_1_precio_por_zona.png
grafico_14_cajas_municipio.png

La Brecha de los Servicios y la Demanda

grafico_15_servicios_precio.png
grafico_16_oferta_vs_preferencia.png

Machine Learning y Clústeres

grafico_8_clusters_scatter.png

---

6. 🗂️ Guía de Navegación del Repositorio

📂 Recurso 📄 Archivo 📝 Contenido
La Historia historia.pdf Narrativa completa, 30 hallazgos y conclusiones.
Informe Técnico informe_tecnico.pdf Metodología profunda, pipeline y límites.
Proceso Interactivo notebook_analisis.ipynb Jupyter Notebook paso a paso.
Bitácora bitacora.md Registro diario del desarrollo.
Diccionario diccionario_datos.md Explicación de cada columna de los CSV.
Defensa Oral guion.md Estructura de la presentación.

---

7. 🛠️ Reproducibilidad del Pipeline

Para reproducir el análisis:

```bash
pip install -r requirements.txt
python auditoria.py          # Limpieza y corrección
python estadisticas.py       # Pruebas de hipótesis
python clustering.py         # K-Means
python entrevistas_analisis.py
python generar_informe.py    # Gráficos y reporte
```

---

8. 🧪 Control de Calidad (QA) y Pruebas

El archivo test_datos.py contiene 14 pruebas automáticas (unittest) que garantizan:

· Exactitud de los 92 anuncios.
· Ausencia de precios ilógicos (< 1,000 USD).
· Anonimización de entrevistas (P01-P35).
· Integridad del PDF de historia.

---

9. 🔒 Ética, Privacidad y Limitaciones

· Privacidad: Teléfonos enmascarados ([tel]). Entrevistas 100% anónimas.
· Uso de IA: Apoyo en estructuración y redacción. La recolección, validación y análisis estadístico son autoría exclusiva de la estudiante.
· Limitaciones: Muestra de 92 anuncios (una sola extracción). Precios de oferta, no de cierre real.

---

“En la Ciencia de Datos, los datos no hablan por sí solos; requieren a alguien que los limpie, los cuestione y les dé voz con rigor científico.”
