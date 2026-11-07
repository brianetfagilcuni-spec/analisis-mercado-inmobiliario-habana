# Diccionario de datos

Todos los precios están en USD. "Sí/No" son texto. Una columna con 0 en cuartos o baños significa **no indicado**, no "cero".

## `limpios/inmuebles_habana_pro.csv` (92 filas, archivo principal)
| Columna | Descripción |
|---|---|
| Título | Título del anuncio |
| Tipo_Inmueble | Apartamento, Casa, Biplanta, Finca u Otro |
| Categoria_Precio | Rango de precio del scraping original. **No usar**: se calculó con el precio sin corregir; los scripts la recalculan con el precio corregido |
| Precio_Num | Precio extraído automáticamente. **Tiene errores** (dígitos de más, valores de 1 a 170 USD). Usar `Precio_corregido` |
| Moneda | Siempre USD en esta extracción |
| Zona_Limpia | Zona leída del texto del anuncio (por ejemplo, Vedado). "Otra zona" si no se pudo asignar |
| Categoria_Ubicacion | Premium, Centro, Periferia o No Clasificada, según la zona (clasificación del scraping) |
| Cuartos, Baños | Cantidad indicada en el anuncio; 0 si no la dice |
| Puntuacion | Puntaje de 0 a 13 de cuántos datos trae el anuncio; mide el nivel de detalle, no la calidad de la vivienda |
| Es_Oportunidad | Marca del scraping (Sí/No). **Su definición no está documentada**; solo 6 textos dicen "oportunidad". No se usa en la historia |
| Menciona_Emigracion | Sí/No según palabras clave en el texto. Es "No" en los 92 anuncios |
| Agua, Luz, Gas, Teléfono, Internet | Sí si el anuncio menciona ese servicio |
| Cocina, Sala, Comedor | Sí si el anuncio menciona ese espacio |
| Patio, Terraza, Balcon, Jardín, Piscina, Garaje, Vista_al_mar | Sí si el anuncio menciona esa característica |
| Placa_Libre, Independiente, Amoblado | Sí si el anuncio lo dice |
| Negociable, Permuta | Sí si el anuncio lo dice |
| Descripción | Texto del anuncio, con los teléfonos enmascarados como [tel] |
| Enlace | URL del anuncio en Revolico |

## `limpios/inmuebles_auditados.csv` (92 filas)
| Columna | Descripción |
|---|---|
| Título, Tipo_Inmueble, Zona_Limpia, Enlace | Igual que arriba |
| Municipio | Municipio según Revolico (13 municipios distintos en la muestra) |
| Precio_original | `Precio_Num` tal como salió del scraping |
| **Precio_corregido** | Precio leído del texto del anuncio. **Es el precio que se usa en todo el análisis** |
| flag_precio_corregido | Sí si el precio original era erróneo (16 anuncios) |
| flag_precio_ambiguo | Sí si el texto trae más de un precio (4) |
| flag_zona_distinta | Sí si la zona del texto no coincide con el municipio de Revolico (10) |
| flag_zona_sin_asignar | Sí si la zona quedó como "Otra zona" (13) |
| flag_duplicado | Sí si es casi duplicado de otro anuncio (2) |
| flag_sin_detalle | Sí si el anuncio no tiene descripción (12) |

## `limpios/con_clusters.csv` (92 filas)
Las columnas de `inmuebles_habana_pro.csv` más: `Precio` (precio corregido), `N_extras` (cantidad de servicios y características), `log_precio`, `Cluster` (0 a 2) y `Segmento` (Poco detallado, Detallado o Lujo).

## Resúmenes
| Archivo | Contenido |
|---|---|
| `limpios/perfil_clusters.csv` | Por segmento: anuncios, precio mediano, cuartos, baños y extras |
| `limpios/triangulacion.csv` | n, cuartiles, mediana y promedio de las dos extracciones |
| `limpios/auditoria_resumen.csv` | Indicadores de la auditoría (indicador, valor) |
| `limpios/estadisticas.csv` | Comparaciones de precio entre grupos: n con y sin, medianas, p de Mann-Whitney, diferencia de medianas con intervalo bootstrap y si es concluyente |
| `limpios/estadisticas_municipio.csv` | Por municipio: n, mediana y cuartiles |
| `limpios/estadisticas_modelos.csv` | R² ajustado de cada modelo sobre el logaritmo del precio |

## `crudos/`
| Archivo | Contenido |
|---|---|
| `revolico_completo.csv` | Extracción 1 tal como salió del scraping (teléfonos enmascarados) |
| `revolico_casas.csv` | Extracción 2: solo título y precio, con otro proceso de filtrado |

## `../entrevistas/`
| Archivo | Contenido |
|---|---|
| `personas.csv` | 35 filas (P01 a P35). `rol`; `p1_valora` a `p5_precios` con las letras del cuestionario (ver `entrevistas/cuestionarios.md`); varias letras en una celda significan varias opciones |
| `inmobiliarias.csv` | 5 filas (INM1 a INM5). Zonas caras y baratas, precios de cierre en USD (punto medio cuando se dio un rango), rebaja en %, meses de venta, servicio más valorado, motivos y composición del catálogo en %, y notas |
| `respuestas_cualitativas.csv` | 25 respuestas de texto libre: `codigo`, `tipo` (persona o inmobiliaria), `tema`, `respuesta` |

Los códigos P01 a P35 e INM1 a INM5 son anónimos. No se guardan nombres ni teléfonos.
