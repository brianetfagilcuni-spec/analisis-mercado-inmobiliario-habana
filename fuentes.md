# Fuentes de datos

Todo el trabajo se hizo en un período de tres semanas, entre octubre y principios de noviembre de 2026 (ver `bitacora.md`).

| Dato | Fuente | Método | Estado |
|---|---|---|---|
| 92 anuncios de venta | Revolico (web) | Scraping con `scraping_revolico.py` en PyDroid 3; teléfonos enmascarados | Completo |
| 78 anuncios (contraste) | Revolico (web), solo título y precio | Extracción separada (`revolico_casas.csv`) | Completo |
| Encuesta a 35 personas | Personas que compran o venden, en persona y por WhatsApp | Cuestionario de 5 preguntas, muestreo por conveniencia | Completo |
| Entrevistas a 5 inmobiliarias o gestoras | Inmobiliarias y gestoras, por WhatsApp | Cuestionario de 6 preguntas y texto libre | Completo |
| Catálogo de viviendas | Una de las cinco inmobiliarias compartió el suyo (enlace de Facebook y fotos). Las otras cuatro prefirieron no compartirlo, para proteger su información | Capturas y enlace en `anuncios_fotografias.md` | Una de cinco |
| Evidencia fotográfica | Seis capturas de anuncios de una inmobiliaria en Facebook: https://www.facebook.com/share/1BvYySV94j/ | Capturas de pantalla (`casa_1_...` a `casa_6_...`) | Completo; no entra en las estadísticas |
| Contexto legal | Prensa sobre la Ley 187/2026 (lista abajo) | Búsqueda web | Completo (fuentes de prensa) |

## Privacidad de las fuentes
- Muchas personas pidieron que no se publicara su nombre ni su número: esos datos se conservan de forma privada y no están en el repositorio.
- Las inmobiliarias que no quisieron compartir su catálogo no aparecen con nombre; se identifican como INM1 a INM5.
- Los teléfonos de los anuncios de Revolico están enmascarados como `[tel]`.

## Fuentes de prensa sobre la Ley 187/2026 (de la Vivienda)
Fecha de consulta: 5 de noviembre de 2026. Son fuentes de prensa; el texto oficial está en la Gaceta Oficial de la República de Cuba, edición ordinaria nº 86 (14 de octubre de 2026).

| Medio | Título | Fecha | Enlace |
|---|---|---|---|
| Escambray | Cuba publica una nueva Ley de la Vivienda: ¿qué cambia? | oct. 2026 | https://www.escambray.cu/2026/cuba-publica-una-nueva-ley-de-la-vivienda-que-cambia/ |
| Diario Libre (EFE) | Cuba publica nueva Ley de la Vivienda que permite tener hasta dos inmuebles en propiedad | 14 oct. 2026 | https://www.diariolibre.com/mundo/america-latina/2026/10/14/cuba-publica-nueva-ley-de-la-vivienda-que-reconoce-propiedad/3689466 |
| ABC Color (EFE) | Cuba publica nueva Ley de Vivienda que permite tener hasta dos inmuebles en propiedad | 14 oct. 2026 | https://www.abc.com.py/internacionales/2026/10/14/cuba-publica-nueva-ley-de-vivienda-que-permite-tener-hasta-dos-inmuebles-en-propiedad/ |
| Directorio Cubano | Cuba prohíbe pagar viviendas en efectivo: nuevas reglas para comprar y vender casas en la isla | oct. 2026 | https://www.directoriocubano.info/?p=155517 |
| Periódico Cubano | Publican la nueva Ley de la Vivienda de Cuba: un resumen de sus principales puntos | 14 oct. 2026 | https://www.periodicocubano.com/publican-la-nueva-ley-de-la-vivienda-de-cuba-un-resumen-de-sus-principales-puntos/ |

Lo que dicen, en breve: aprobada el 30 de julio de 2026, publicada el 14 de octubre y en vigor desde el 21; sustituye la Ley General de la Vivienda de 1988; reconoce hasta dos viviendas (más una de descanso); la compraventa se formaliza ante notario; el pago se hace por medios bancarios y no en efectivo; elimina la confiscación por salida del país.
