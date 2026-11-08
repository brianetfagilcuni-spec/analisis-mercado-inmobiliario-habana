"""Genera index.html (la historia como página web) a partir de historia.md.
Ejecutar desde la carpeta del repositorio:  python build_web.py
La página se publica con GitHub Pages y usa Umami (analítica sin cookies) para contar visitas, tiempo y lectura."""
import re, html

URL = "https://brianetfagilcuni-spec.github.io/analisis-mercado-inmobiliario-habana/"
REPO = "https://github.com/brianetfagilcuni-spec/analisis-mercado-inmobiliario-habana"
UMAMI_ID = "PEGA-AQUI-TU-ID-DE-UMAMI"   # <- reemplaza por el ID de tu sitio en Umami (ver plan_campana_comunicacion.md)

def esc(t): return html.escape(t, quote=False)
def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)

lines = open("historia.md", encoding="utf-8").read().split("\n")
title = lines[0][2:].strip()
subtitle = ""
body, i = [], 1
# bloques
blocks, para, tabla, lista = [], [], [], []
def flush():
    global para, lista
    if para: blocks.append(("p", " ".join(para))); para = []
    if lista: blocks.append(("ul" if lista[0][0] == "-" else "ol", [x[1] for x in lista])); lista = []
for ln in lines[1:]:
    s = ln.strip()
    if s.startswith("|"):
        flush(); cols = [c.strip() for c in s.strip("|").split("|")]
        if not all(re.fullmatch(r"-+", c) for c in cols): tabla.append(cols)
        continue
    elif tabla:
        blocks.append(("cards", tabla[1:])); tabla = []
    if not s: flush(); continue
    m = re.match(r"!\[(.*?)\]\((.*?)\)", s)
    if m: flush(); blocks.append(("img", m.group(1), m.group(2)))
    elif s == "---": flush(); blocks.append(("hr",))
    elif s.startswith("## "): flush(); blocks.append(("h2", s[3:]))
    elif s.startswith("> "): flush(); blocks.append(("callout", s[2:]))
    elif re.match(r"^\*\*(\d+)\. (.+)\*\*$", s):
        flush(); mm = re.match(r"^\*\*(\d+)\. (.+)\*\*$", s); blocks.append(("q", mm.group(1), mm.group(2)))
    elif re.match(r"^\d+\. ", s): 
        if para: flush()
        lista.append(("1", re.sub(r"^\d+\. ", "", s)))
    elif s.startswith("- "):
        if para: flush()
        lista.append(("-", s[2:]))
    elif s.startswith("*") and s.endswith("*") and not s.startswith("**") and not subtitle: subtitle = s.strip("*")
    else:
        if lista: flush()
        para.append(s)
flush()

out, toc, inq, insec = [], [], False, False
def slug(t): return re.sub(r"[^a-z0-9]+", "-", t.lower().translate(str.maketrans("áéíóúüñ", "aeiouun"))).strip("-")
def close_q():
    global inq
    if inq: out.append("</article>"); inq = False
for b in blocks:
    k = b[0]
    if k == "h2":
        close_q()
        if insec: out.append("</section>")
        sid = slug(b[1]); toc.append((sid, b[1]))
        out.append(f'<section id="{sid}"><h2>{inline(b[1])}</h2>'); insec = True
    elif k == "q":
        close_q(); out.append(f'<article class="q" id="p{b[1]}"><h3><span class="n">{b[1]}</span>{inline(b[2])}</h3>'); inq = True
    elif k == "p": out.append(f"<p>{inline(b[1])}</p>")
    elif k in ("ul", "ol"): out.append(f"<{k}>" + "".join(f"<li>{inline(x)}</li>" for x in b[1]) + f"</{k}>")
    elif k == "img": out.append(f'<figure><img src="{b[2]}" alt="{esc(b[1])}" loading="lazy"><figcaption>{esc(b[1])}</figcaption></figure>')
    elif k == "callout": out.append(f'<aside class="callout">{inline(b[1])}</aside>')
    elif k == "cards": out.append('<div class="cards">' + "".join(f'<div class="card"><b>{inline(a)}</b><span>{inline(c)}</span></div>' for a, c in b[1]) + "</div>")
    elif k == "hr": close_q()
close_q()
if insec: out.append("</section>")
contenido = "\n".join(out)
words = len(re.sub(r"<[^>]+>", " ", contenido).split()); minutos = max(1, round(words / 200))
tocs = "".join(f'<a href="#{s}">{esc(t)}</a>' for s, t in toc)
desc = "Una historia contada con datos: 92 anuncios de Revolico, 5 inmobiliarias y 35 personas responden qué determina el precio de una vivienda en La Habana."
share_text = "¿Qué determina realmente el precio de una vivienda en La Habana? Una historia contada con datos"

pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}montaje_6_casas.jpg">
<meta name="twitter:card" content="summary_large_image">
<!-- Analítica sin cookies (Umami). Reemplaza el ID por el de tu sitio. -->
<script defer src="https://cloud.umami.is/script.js" data-website-id="{UMAMI_ID}"></script>
<style>
:root{{--bg:#faf8f3;--ink:#1a1f2b;--mute:#667085;--burg:#6b1f2e;--gold:#b8914b;--sand:#f3ead7;--card:#fff;--line:#e7e2d6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181d;--ink:#eceff4;--mute:#9aa3b2;--burg:#e0a3ad;--gold:#d4b36a;--sand:#2a2620;--card:#1f2229;--line:#2e323b}}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 Georgia,"Times New Roman",serif}}
#bar{{position:fixed;top:0;left:0;height:4px;width:0;background:var(--gold);z-index:9}}
header.hero{{background:linear-gradient(135deg,#5a1a27,#6b2a33);color:#fff;padding:56px 20px 44px}}
.wrap{{max-width:760px;margin:0 auto;padding:0 18px}}
.hero .wrap{{padding:0}}
.kicker{{font:600 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#d9c88f}}
.hero h1{{font-size:clamp(28px,6vw,44px);line-height:1.12;margin:14px 0 12px;color:#f0e3b8}}
.hero p.sub{{font-size:19px;line-height:1.5;margin:0 0 6px;color:#fff;opacity:.92}}
.meta{{font:14px Helvetica,Arial,sans-serif;color:#e8dcc0;margin:14px 0 22px}}
.btn{{display:inline-block;font:600 15px Helvetica,Arial,sans-serif;padding:11px 18px;border-radius:8px;text-decoration:none;margin:4px 6px 4px 0;border:0;cursor:pointer}}
.btn.p{{background:var(--gold);color:#241a08}}.btn.s{{background:rgba(255,255,255,.14);color:#fff}}
nav.toc{{font:14px/1.9 Helvetica,Arial,sans-serif;background:var(--sand);border-radius:10px;padding:14px 18px;margin:26px 0}}
nav.toc b{{display:block;margin-bottom:4px;color:var(--burg)}}nav.toc a{{display:block;color:var(--ink);text-decoration:none;padding:2px 0}}nav.toc a:hover{{color:var(--burg)}}
section{{margin:44px 0}}
h2{{font-size:28px;line-height:1.2;color:var(--burg);border-bottom:2px solid var(--gold);padding-bottom:8px;margin:0 0 18px}}
h3{{font:700 18px/1.35 Helvetica,Arial,sans-serif;margin:0 0 8px;display:flex;gap:10px;align-items:flex-start}}
.n{{flex:none;background:var(--burg);color:var(--bg);border-radius:6px;min-width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;font-size:14px}}
article.q{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 18px 6px;margin:18px 0}}
article.q p{{margin:0 0 14px}}
figure{{margin:18px 0}}figure img{{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);background:#fff}}
figcaption{{font:13px Helvetica,Arial,sans-serif;color:var(--mute);text-align:center;margin-top:6px}}
.callout{{border-left:4px solid var(--gold);background:var(--sand);padding:12px 16px;border-radius:0 8px 8px 0;margin:22px 0;font-size:16px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--gold);border-radius:8px;padding:14px;text-align:center;font-family:Helvetica,Arial,sans-serif}}
.card b{{display:block;font-size:22px}}.card span{{font-size:13px;color:var(--mute)}}
ul,ol{{padding-left:22px}}li{{margin:6px 0}}
.share{{background:var(--sand);border-radius:12px;padding:18px;text-align:center;margin:36px 0;font-family:Helvetica,Arial,sans-serif}}
.share .btn{{background:var(--burg);color:var(--bg)}}
footer{{border-top:1px solid var(--line);padding:26px 0 60px;font:14px/1.7 Helvetica,Arial,sans-serif;color:var(--mute)}}
footer a{{color:var(--burg)}}
#top{{position:fixed;right:16px;bottom:16px;background:var(--burg);color:var(--bg);border:0;border-radius:50%;width:44px;height:44px;font-size:20px;display:none;cursor:pointer}}
</style>
</head>
<body>
<div id="bar"></div>
<header class="hero"><div class="wrap">
<div class="kicker">Introducción a la Ciencia de Datos · Universidad de La Habana</div>
<h1>{esc(title)}</h1>
<p class="sub">{esc(subtitle)}</p>
<div class="meta">Brianet Fagil Cuni · Lectura de unos {minutos} minutos · 30 preguntas, 25 gráficos</div>
<a class="btn p" href="#antes-de-empezar-la-pregunta-que-no-tenia-respuesta" data-umami-event="empezar-lectura">Leer la historia</a>
<a class="btn s" href="historia.pdf" data-umami-event="descargar-historia-pdf">Descargar PDF</a>
</div></header>
<main class="wrap">
<nav class="toc"><b>En esta historia</b>{tocs}</nav>
{contenido}
<div class="share"><p><strong>¿Te sirvió? Compártela.</strong><br>Cada persona que la lea ayuda a que más gente entienda el mercado de la vivienda.</p>
<a class="btn" data-umami-event="compartir-whatsapp" href="https://wa.me/?text={html.escape(share_text.replace(' ', '%20'))}%20{URL}%3Futm_source%3Dwhatsapp%26utm_medium%3Dcompartir" target="_blank" rel="noopener">WhatsApp</a>
<a class="btn" data-umami-event="compartir-facebook" href="https://www.facebook.com/sharer/sharer.php?u={URL}%3Futm_source%3Dfacebook%26utm_medium%3Dcompartir" target="_blank" rel="noopener">Facebook</a>
<a class="btn" data-umami-event="compartir-telegram" href="https://t.me/share/url?url={URL}%3Futm_source%3Dtelegram%26utm_medium%3Dcompartir&text={html.escape(share_text.replace(' ', '%20'))}" target="_blank" rel="noopener">Telegram</a>
<button class="btn" id="copiar" data-umami-event="copiar-enlace">Copiar enlace</button></div>
</main>
<footer><div class="wrap">
<p><strong>Más del proyecto:</strong>
<a href="informe_tecnico.pdf" data-umami-event="ver-informe-tecnico">Informe técnico (PDF)</a> ·
<a href="README.md">README</a> ·
<a href="{REPO}" data-umami-event="ver-repositorio">Repositorio en GitHub</a></p>
<p>Hecho íntegramente desde un teléfono Android, con Python en PyDroid 3 y con ayuda de inteligencia artificial. Los datos de las entrevistas son anónimos y se conservan de forma privada; esta página solo cuenta visitas de forma agregada y sin cookies.</p>
</div></footer>
<button id="top" aria-label="Volver arriba">↑</button>
<script>
(function(){{
  var bar=document.getElementById('bar'),top=document.getElementById('top'),hit={{}};
  function pct(){{var h=document.documentElement,s=h.scrollTop||document.body.scrollTop,t=h.scrollHeight-h.clientHeight;return t>0?Math.round(s/t*100):0}}
  window.addEventListener('scroll',function(){{
    var p=pct();bar.style.width=p+'%';top.style.display=p>8?'block':'none';
    [25,50,75,100].forEach(function(m){{if(p>=m-(m==100?2:0)&&!hit[m]){{hit[m]=1;try{{if(window.umami)umami.track('lectura-'+m+'-por-ciento')}}catch(e){{}}}}}});
  }},{{passive:true}});
  top.onclick=function(){{window.scrollTo({{top:0}})}};
  document.getElementById('copiar').onclick=function(){{var b=this;(navigator.clipboard?navigator.clipboard.writeText('{URL}'):Promise.reject()).then(function(){{b.textContent='¡Copiado!'}},function(){{prompt('Copia este enlace:','{URL}')}})}};
}})();
</script>
</body>
</html>"""
open("index.html", "w", encoding="utf-8").write(pagina)
print("index.html generado:", len(pagina) // 1024, "KB;", len(toc), "secciones;", minutos, "min de lectura")
