# Prompt usado para diseñar la guía de entrevistas

Se usó un asistente de inteligencia artificial para proponer la estructura de la guía y la plantilla de tabulación. Este es el prompt:

> Actúa como un investigador de campo en ciencia de datos aplicado a la vida cotidiana en La Habana. Diseña una guía de entrevista semiestructurada y una plantilla de tabulación estructurada para 40 sujetos (35 ciudadanos locales y 5 gestores o agencias inmobiliarias) abordando:
> 1. Ubicación de la vivienda y precio mediano negociado.
> 2. Tipo de moneda solicitada (USD, EUR, MLC, CUP) y forma de pago.
> 3. Limitaciones constructivas, estado del inmueble y liquidez del sector.
> 4. Consentimiento y confidencialidad respecto a la divulgación de datos personales.

**Qué se hizo con el resultado.** La IA propone una guía y una plantilla, no respuestas. Las respuestas reales de las entrevistas son las de `personas.csv` (35 personas) e `inmobiliarias.csv` (5 inmobiliarias). Los cuestionarios finales usados están en [`cuestionarios.md`](cuestionarios.md). Para analizar las respuestas reales se usa el prompt de [`prompt_analisis_entrevistas.md`](prompt_analisis_entrevistas.md).
