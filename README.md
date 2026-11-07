# Gráficos

Todos se generan con los scripts de `codigo/` a partir de los datos de `datos/` y `entrevistas/`. No se editan a mano. Las preguntas se refieren a `historia/historia.md`.

## Anuncios de Revolico (92 anuncios, precios corregidos)
| Archivo | Qué muestra | Preguntas |
|---|---|---|
| `grafico_1_precio_por_zona.png` | Precio mediano por zona del anuncio, con n | 7, 8 |
| `grafico_10_municipio.png` | Precio mediano por municipio | 7, 8, 10 |
| `grafico_14_cajas_municipio.png` | Dispersión del precio por municipio (n ≥ 5) | 12 |
| `grafico_2_categoria_precio.png` | Reparto por rango de precio | 6 |
| `grafico_6_distribucion_precios.png` | Distribución de los precios | 1, 2 |
| `grafico_3_tipo_inmueble.png` | Anuncios por tipo de vivienda | 14, 32 |
| `grafico_4_servicios.png` | Anuncios que mencionan cada servicio | 18 |
| `grafico_5_caracteristicas.png` | Características más mencionadas | 16, 20 |
| `grafico_15_servicios_precio.png` | Precio mediano con y sin cada característica | 19, 20, 21 |

## Calidad de los datos y segunda extracción
| Archivo | Qué muestra | Preguntas |
|---|---|---|
| `grafico_11_auditoria.png` | Problemas detectados en la auditoría | 3, 4 |
| `grafico_12_sensibilidad.png` | La mediana es estable; el promedio no | 2, 3 |
| `grafico_13_triangulacion.png` | Comparación con la segunda extracción | 5 |

## Clustering (exploratorio)
| Archivo | Qué muestra |
|---|---|
| `grafico_7_codo.png` | Método del codo para elegir k |
| `grafico_8_clusters_scatter.png` | Segmentos: separan por nivel de detalle del anuncio, más un grupo de lujo |
| `grafico_9_precio_por_segmento.png` | Precio mediano por segmento |

## Anuncios frente a personas
| Archivo | Qué muestra | Preguntas |
|---|---|---|
| `grafico_16_oferta_vs_preferencia.png` | Tipo ofertado frente al preferido | 32 |

## Entrevistas (`entrevistas/`)
| Archivo | Qué muestra | Preguntas |
|---|---|---|
| `personas_1_p1_valora.png` | Qué valoran las personas al buscar vivienda (n = 35) | 33 |
| `personas_2_p2_zona_cara.png` | Zona que creen más cara | 34 |
| `personas_3_p3_tipo.png` | Tipo de vivienda preferido | 32 |
| `personas_4_p4_servicio.png` | Servicio indispensable | 33 |
| `personas_5_p5_precios.png` | Cómo ven la evolución de los precios | 35 |
| `inmob_zonas_caras.png`, `inmob_zonas_baratas.png` | Zonas que mencionan las inmobiliarias (n pequeño) | 13 |
| `inmob_servicio.png` | Servicios que destacan las inmobiliarias | 33 |
| `inmob_catalogo.png` | Catálogo de una inmobiliaria (cifra dicha en la entrevista, no verificada) | 32 |

Los gráficos con pocas inmobiliarias (n = 2 a 5) son descriptivos: no sirven para generalizar.
