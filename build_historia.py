"""Genera historia/historia.pdf (storytelling) a partir de historia/historia.md.
Ejecutar desde la raíz del repositorio:  python codigo/informe_pdf/build_historia.py
Las imágenes se leen de graficos/ (las rutas ../graficos/... del .md se ajustan solas)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, KeepTogether,
                                Table, TableStyle, NextPageTemplate, PageBreak, CondPageBreak, HRFlowable)
from reportlab.lib.utils import ImageReader

BURG = colors.HexColor("#6b1f2e"); GOLD = colors.HexColor("#b8914b"); CREAM = colors.HexColor("#faf8f3")
INK = colors.HexColor("#1a1f2b"); GREY = colors.HexColor("#6b7488"); SAND = colors.HexColor("#f3ead7")
W, H = A4
ML = 2.2 * cm

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10.3, leading=15.2, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=7)
bul = ParagraphStyle("bul", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=4, alignment=TA_LEFT)
h1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=30, leading=34, textColor=BURG, spaceAfter=6)
sub = ParagraphStyle("sub", parent=body, fontName="Times-Italic", fontSize=12.5, leading=17, textColor=GREY, alignment=TA_LEFT, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=21, leading=25, textColor=BURG, spaceBefore=6, spaceAfter=2)
qtxt = ParagraphStyle("q", fontName="Helvetica-Bold", fontSize=10.8, leading=14.5, textColor=INK, alignment=TA_LEFT)
qnum = ParagraphStyle("qn", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.white, alignment=TA_CENTER)
cap = ParagraphStyle("cap", parent=body, fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=GREY, spaceAfter=8)
call = ParagraphStyle("call", parent=body, fontSize=10, leading=14.2, alignment=TA_LEFT, spaceAfter=0)
cardn = ParagraphStyle("cn", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=INK, alignment=TA_CENTER)
cardl = ParagraphStyle("cl", fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=GREY, alignment=TA_CENTER)

def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)

def question(num, text):
    t = Table([[Paragraph(num, qnum), Paragraph(inline(text), qtxt)]], colWidths=[0.9 * cm, W - 2 * ML - 1.1 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), BURG), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (1, 0), (1, 0), 8), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LINEBELOW", (1, 0), (1, 0), 0.6, GOLD)]))
    return t

def callout(text):
    t = Table([[Paragraph(inline(text), call)]], colWidths=[W - 2 * ML])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SAND), ("LINEBEFORE", (0, 0), (0, 0), 3, GOLD),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return [Spacer(1, 4), t, Spacer(1, 10)]

def cards(rows):
    tops = [colors.HexColor(c) for c in ("#9aa5b8", "#9aa5b8", "#1d4ed8", "#15803d", "#b8914b", "#b8914b", "#6b1f2e", "#dc2626")]
    cells = [[Paragraph(inline(a), cardn), Paragraph(inline(b), cardl)] for a, b in rows]
    cw = (W - 2 * ML - 3 * 0.3 * cm) / 4
    data, styles = [], [("VALIGN", (0, 0), (-1, -1), "TOP")]
    for r in range(0, len(cells), 4):
        chunk = cells[r:r + 4]
        data.append([[c[0], Spacer(1, 3), c[1]] for c in chunk] + [""] * (4 - len(chunk)))
    t = Table(data, colWidths=[cw] * 4, rowHeights=[2.5 * cm] * len(data), hAlign="LEFT")
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(len(cells)):
        r, c = divmod(i, 4)
        st += [("BACKGROUND", (c, r), (c, r), colors.white), ("LINEABOVE", (c, r), (c, r), 3, tops[i % len(tops)]),
               ("BOX", (c, r), (c, r), 0.4, colors.HexColor("#e2e5ec"))]
    t.setStyle(TableStyle(st))
    # separación entre tarjetas: Table no admite gaps; se simula con bordes blancos gruesos
    t.setStyle(TableStyle([("INNERGRID", (0, 0), (-1, -1), 4, CREAM)]))
    return [Spacer(1, 4), t, Spacer(1, 10)]

story = [NextPageTemplate("body"), PageBreak()]
lines = open("historia/historia.md", encoding="utf-8").read().split("\n")
para, pending_q, table_rows = [], None, []

def flush():
    global para, pending_q
    if para:
        p = Paragraph(inline(" ".join(para)), body); para = []
        if pending_q is not None:
            story.append(KeepTogether([pending_q, Spacer(1, 3), p])); pending_q = None
        else:
            story.append(p)
    elif pending_q is not None:
        story.append(pending_q); pending_q = None

for ln in lines:
    s = ln.strip()
    if s.startswith("|"):
        flush()
        cols = [c.strip() for c in s.strip("|").split("|")]
        if not all(re.fullmatch(r"-+", c) for c in cols):
            table_rows.append(cols)
        continue
    elif table_rows:
        story += cards(table_rows[1:]); table_rows = []
    if not s:
        flush(); continue
    m = re.match(r"!\[(.*?)\]\((.*?)\)", s)
    if m:
        flush()
        path = m.group(2).replace("../", "")
        iw, ih = ImageReader(path).getSize()
        Wd = 13.2 * cm
        story.append(KeepTogether([Image(path, width=Wd, height=Wd * ih / iw), Paragraph(inline(m.group(1)), cap)]))
    elif s == "---":
        flush(); story.append(PageBreak())
    elif s.startswith("# "):
        flush(); story += [Paragraph(inline(s[2:]), h1), HRFlowable(width="25%", thickness=2, color=GOLD, spaceAfter=8, hAlign="LEFT")]
    elif s.startswith("## "):
        flush(); story += [CondPageBreak(7 * cm), Spacer(1, 8), Paragraph(inline(s[3:]), h2),
                           HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceAfter=8)]
    elif s.startswith("> "):
        flush(); story += callout(s[2:])
    elif re.match(r"^\*\*(\d+)\. (.+)\*\*$", s):
        flush(); mm = re.match(r"^\*\*(\d+)\. (.+)\*\*$", s); pending_q = question(mm.group(1), mm.group(2))
    elif re.match(r"^\d+\. ", s):
        flush(); story.append(Paragraph(inline(re.sub(r"^\d+\. ", "", s)), bul, bulletText=s.split(".")[0] + "."))
    elif s.startswith("- "):
        flush(); story.append(Paragraph(inline(s[2:]), bul, bulletText="•"))
    elif s.startswith("*") and s.endswith("*") and not s.startswith("**") and not story[-1:] == []:
        flush(); story.append(Paragraph(inline(s), sub))
    else:
        para.append(s)
flush()
if table_rows: story += cards(table_rows[1:])

def cover(c, d):
    c.saveState()
    c.setFillColor(colors.HexColor("#5a1a27")); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#6b2a33")); c.rect(0, H - 9 * cm, W, 9 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#5a1a27")); c.rect(0, H - 9 * cm - 0.01, W, 0.02, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#e8dcc0")); c.setFont("Times-Roman", 17); c.drawString(ML, H - 3.1 * cm, "UNIVERSIDAD DE LA HABANA")
    t = c.beginText(ML, H - 11.3 * cm); t.setFont("Helvetica-Bold", 8.5); t.setFillColor(GOLD); t.setCharSpace(2.4)
    t.textOut("INTRODUCCIÓN A LA CIENCIA DE DATOS"); t.setCharSpace(0); c.drawText(t)
    c.setStrokeColor(GOLD); c.setLineWidth(2.5); c.line(ML, H - 11.9 * cm, ML + 4 * cm, H - 11.9 * cm)
    ts = ParagraphStyle("ct", fontName="Times-Bold", fontSize=36, leading=41, textColor=colors.HexColor("#d9c88f"))
    p = Paragraph("¿Qué determina realmente el precio de una vivienda en La Habana?", ts)
    pw, ph = p.wrap(W - 2 * ML, 10 * cm); p.drawOn(c, ML, H - 12.8 * cm - ph)
    ss = ParagraphStyle("cs", fontName="Times-Roman", fontSize=15, leading=21, textColor=colors.white)
    p2 = Paragraph("Una historia contada con datos: anuncios de Revolico, entrevistas a inmobiliarias y una encuesta a 35 personas.", ss)
    w2, h2_ = p2.wrap(W - 2 * ML - 2 * cm, 6 * cm); p2.drawOn(c, ML, H - 12.8 * cm - ph - 0.8 * cm - h2_)
    c.setStrokeColor(colors.HexColor("#8a6a70")); c.setLineWidth(0.6); c.line(ML, 3.2 * cm, W - ML, 3.2 * cm)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9); c.drawString(ML, 2.5 * cm, "Brianet Fagil Cuni")
    c.setFillColor(colors.HexColor("#d3c3c6")); c.setFont("Helvetica", 8.5)
    c.drawString(ML, 2.0 * cm, "Estudiante de 1.er año de Ciencia de Datos  ·  MatCom  ·  ICD 26-27")
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 9); c.drawRightString(W - ML, 2.5 * cm, "Noviembre de 2026")
    c.restoreState()

def pagina(c, d):
    c.saveState()
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont("Times-Roman", 8.5); c.setFillColor(GREY)
    c.drawString(ML, 1.3 * cm, "¿Qué determina el precio de una vivienda en La Habana?")
    c.drawRightString(W - ML, 1.3 * cm, str(d.page))
    c.restoreState()

doc = BaseDocTemplate("historia/historia.pdf", pagesize=A4, leftMargin=ML, rightMargin=ML, topMargin=2 * cm, bottomMargin=2.2 * cm,
                      title="¿Qué determina realmente el precio de una vivienda en La Habana?", author="Brianet Fagil Cuni")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[Frame(0, 0, W, H, id="f0")], onPage=cover),
    PageTemplate(id="body", frames=[Frame(ML, 2.2 * cm, W - 2 * ML, H - 4.2 * cm, id="f1")], onPage=pagina)])
doc.build(story)
print("historia generada")
