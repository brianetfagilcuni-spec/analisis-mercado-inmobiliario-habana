"""
Scraper básico de anuncios de venta de casas en Revolico (La Habana).
Usa solo requests + re + pandas. Corre en Termux/PyDroid.

IMPORTANTE: no pude probarlo con internet. Revolico puede cambiar su HTML
o bloquear peticiones; si algo falla, mándame el mensaje exacto del error.
Instalar: pip install requests
"""
import re
import time
import requests
import pandas as pd

BASE = "https://www.revolico.com"
LISTADO = BASE + "/inmobiliaria/casas/la-habana?page={}"   # si falla, abre Revolico en el navegador y copia la URL real
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"}
PAGINAS = 3          # empieza con pocas páginas
PAUSA = 2            # segundos entre peticiones (se amable con el sitio)

def pedir(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text

def limpiar(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()

# 1. Juntar enlaces de anuncios
enlaces = []
for p in range(1, PAGINAS + 1):
    try:
        html = pedir(LISTADO.format(p))
    except Exception as e:
        print("Error en página", p, "->", e)
        break
    nuevos = re.findall(r'href="(/item/[^"?#]+)', html)
    enlaces += [BASE + n for n in nuevos]
    print(f"Página {p}: {len(nuevos)} enlaces")
    time.sleep(PAUSA)
enlaces = list(dict.fromkeys(enlaces))   # quitar repetidos
print("Total de anuncios:", len(enlaces))

# 2. Leer cada anuncio
filas = []
for i, url in enumerate(enlaces, 1):
    try:
        html = pedir(url)
    except Exception as e:
        print("Error en", url, "->", e)
        continue
    t = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    texto = limpiar(html)
    precio = re.search(r"(\d{1,3}(?:,\d{3})+|\d+)\s*USD", texto)
    filas.append({
        "Título": t.group(1).strip() if t else "",
        "Precio": precio.group(0) if precio else "",
        "Descripción": texto[:1500],
        "Enlace": url,
    })
    print(f"{i}/{len(enlaces)} listo")
    time.sleep(PAUSA)

# 3. Guardar
pd.DataFrame(filas).to_csv("datos_crudos_revolico_scraping_nuevo.csv", index=False)
print("Guardado: datos_crudos_revolico_scraping_nuevo.csv")
