# Entrevistas

Todas las entrevistas están anonimizadas con códigos. No se publican nombres, teléfonos ni catálogos de terceros sin permiso.

| Archivo | Contenido |
|---|---|
| `personas.csv` | 35 personas (P01-P35), cuestionario de 5 preguntas codificado con letras |
| `inmobiliarias.csv` | 5 inmobiliarias o gestoras (INM1-INM5), datos numéricos y notas |
| `respuestas_cualitativas.csv` | Respuestas de texto libre, por tema |
| `catalogo_inmobiliarias.md` | Ficha de cada inmobiliaria: qué dijo, qué evidencia hay y qué falta |
| `prompt_analisis_entrevistas.md` | Prompt para analizar entrevistas y notas de audio con una IA, sin inventar datos |
| `resumen_muestra.csv`, `resumen_inmobiliarias.csv` | Resúmenes generados por `codigo/entrevistas_analisis.py` |

## Claves del cuestionario de personas
Puede haber varias letras en una respuesta (por ejemplo `AB`); `T` significa "todas".

| Pregunta | Opciones |
|---|---|
| 1. ¿Qué valora más al buscar vivienda? | A Ubicación · B Precio · C Servicios básicos · D Espacio · T Todas |
| 2. ¿Qué zona es la más cara? | A Playa · B Vedado · C Centro Habana · D Otra (`p2_otra_zona`) |
| 3. ¿Qué tipo de inmueble prefiere? | A Casa independiente · B Apartamento · C Biplanta |
| 4. ¿Qué servicio es indispensable? | A Agua · B Luz · C Gas de la calle · D Internet · T Todos |
| 5. ¿Cómo ve los precios? | A Subiendo · B Bajando · C Estables |
