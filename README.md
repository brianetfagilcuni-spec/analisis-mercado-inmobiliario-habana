# Análisis del mercado inmobiliario en La Habana

Extracción, limpieza y análisis de anuncios de venta de viviendas en Revolico (La Habana). Proyecto de Ciencia de Datos, Universidad de La Habana.

## Archivos (por prefijo del nombre)
- `datos_crudos_*.csv`: datos tal como salieron del scraping (sin teléfonos, enmascarados como `[tel]`).
- `datos_limpios_*.csv`: datos limpios y resúmenes. El archivo principal es `datos_limpios_inmuebles_habana_pro.csv`.
- `datos_limpios_con_clusters.csv` y `datos_limpios_perfil_clusters.csv`: resultado del clustering.
- `grafico_1` a `grafico_9`: gráficos en PNG (precios por zona, tipos, servicios, características, clustering).
- `script_scraping_revolico.py`: descarga anuncios de Revolico (sin probar en vivo; el sitio puede cambiar).
- `script_graficos.py`, `script_clustering.py`, `script_generar_informe.py`: análisis en Python (Pandas, NumPy, Matplotlib).
- `informe_inmobiliario.html`: informe con los datos corregidos y los gráficos incrustados (descargar y abrir en el navegador).

## Cómo reproducir
Con todos los archivos en la misma carpeta, ejecutar en este orden:
```
python script_graficos.py
python script_clustering.py
python script_generar_informe.py
```

## Nota sobre los precios
La columna `Precio_Num` del CSV limpio tiene errores de extracción (dígitos de más o precios de 1 a 170 USD). Los scripts corrigen el precio leyendo el texto original del anuncio y descartan valores menores a 1,000 USD.
Con la corrección: 92 anuncios, mediana 25,000 USD y promedio unos 66,000 USD. La zona más cara por mediana es el Vedado.

## Clustering (K-Means, k=3)
Variables: logaritmo del precio, cuartos, baños y cantidad de servicios/características mencionadas. Los grupos separan sobre todo el **nivel de detalle del anuncio** (muchos anuncios no indican cuántos cuartos tienen) y un grupo pequeño de casas de lujo. No es una segmentación de mercado definitiva.

## Entrevistas
En proceso (personas e inmobiliarias). Se agregarán de forma anónima, con códigos y sin nombres ni teléfonos.

## Limitaciones
Muestra pequeña (92 anuncios, una sola extracción). Varias zonas tienen muy pocos anuncios. La zona se leyó del texto del anuncio y algunos de Guanabo aparecen como Playa. Los precios son de oferta, no de cierre. Hay anuncios duplicados.
