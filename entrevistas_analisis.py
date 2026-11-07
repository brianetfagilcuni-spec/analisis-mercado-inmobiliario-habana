"""Gráficos de las entrevistas (personas e inmobiliarias). Si aún no hay datos, avisa y no falla."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "graficos/entrevistas/"

def leer(ruta):
    df = pd.read_csv(ruta)
    return df if len(df) else None

# ================= RESUMEN DE MUESTRA =================
_P, _I = pd.read_csv("entrevistas/personas.csv"), pd.read_csv("entrevistas/inmobiliarias.csv")
filas = [("Cuestionario de personas (5 preguntas)", "total entrevistados", len(_P)),
         ("Cuestionario de personas (5 preguntas)", "de ellos gestoras", int((_P["rol"] == "gestora").sum()))]
for c in ["p1_valora", "p2_zona_cara", "p3_tipo", "p4_servicio", "p5_precios"]:
    filas.append(("Cuestionario de personas (5 preguntas)", f"respondieron {c}", int(_P[c].notna().sum())))
filas.append(("Inmobiliarias / gestoras", "total entrevistadas", len(_I)))
for c in ["rebaja_pct", "meses_venta", "precio_cierre_zonas_caras_usd", "catalogo_casas_pct"]:
    filas.append(("Inmobiliarias / gestoras", f"respondieron {c}", int(pd.to_numeric(_I[c], errors="coerce").notna().sum())))
pd.DataFrame(filas, columns=["grupo", "dato", "n"]).to_csv("entrevistas/resumen_muestra.csv", index=False)
print(f"MUESTRA: {len(_P)} en cuestionario de personas (incluye {int((_P['rol']=='gestora').sum())} gestora) | {len(_I)} inmobiliarias/gestoras")

# ================= PERSONAS =================
P = leer("entrevistas/personas.csv")
if P is None:
    print("personas.csv está vacío: aún no hay respuestas.")
else:
    n = len(P)
    preguntas = {
        "p1_valora": ("¿Qué valora más al buscar vivienda?", {"A": "Ubicación", "B": "Precio", "C": "Servicios básicos", "D": "Espacio", "T": "Todas"}),
        "p2_zona_cara": ("Zona considerada más cara", {"A": "Playa", "B": "Vedado", "C": "Centro Habana", "D": "Otra"}),
        "p3_tipo": ("Tipo de inmueble preferido", {"A": "Casa independiente", "B": "Apartamento", "C": "Biplanta"}),
        "p4_servicio": ("Servicio indispensable", {"A": "Agua", "B": "Luz", "C": "Gas de la calle", "D": "Internet"}),
        "p5_precios": ("Percepción de precios", {"A": "Subiendo", "B": "Bajando", "C": "Estables"}),
    }
    for i, (col, (titulo, mapa)) in enumerate(preguntas.items(), 1):
        mapa = {**mapa, "T": "Todas / todos"}
        resp = P[col].dropna().astype(str).str.strip()
        resp = resp[resp != ""]
        nr = len(resp)
        if nr == 0:
            continue
        # una respuesta puede tener varias letras (ej. "AB"): cuenta a cada opción mencionada
        cuenta = {nombre: int(resp.str.contains(letra).sum()) for letra, nombre in mapa.items()}
        c = pd.Series(cuenta)
        c = c[c > 0].sort_values()
        pct = c / nr * 100
        plt.figure(figsize=(7, 4.5))
        plt.barh(c.index, pct.values, color="#2a5298")
        for j, (v, k) in enumerate(zip(pct.values, c.values)):
            plt.text(v, j, f" {v:.0f}% ({k})", va="center", fontsize=9)
        plt.xlim(0, max(pct.max() * 1.25, 10))
        plt.xlabel("% de quienes respondieron (puede sumar más de 100 si marcaron varias)")
        plt.title(f"{titulo} (n={nr})")
        plt.tight_layout(); plt.savefig(f"{OUT}personas_{i}_{col}.png", dpi=130); plt.close()
    print(f"Gráficos de personas listos (n={n}).")

# ================= INMOBILIARIAS =================
I = leer("entrevistas/inmobiliarias.csv")
if I is None:
    print("inmobiliarias.csv está vacío: aún no hay respuestas.")
else:
    m = len(I)

    # zonas más caras / más baratas (cuántas inmobiliarias las mencionan)
    for tipo, cols, color, nombre in [("caras", ["zona_cara_1", "zona_cara_2", "zona_cara_3"], "#c0392b", "más caras"),
                                      ("baratas", ["zona_barata_1", "zona_barata_2", "zona_barata_3"], "#27ae60", "más económicas")]:
        z = pd.Series(I[cols].values.ravel()).dropna().astype(str).str.strip().str.title().value_counts()
        if len(z):
            plt.figure(figsize=(7, 4.5))
            plt.barh(z.index[::-1], z.values[::-1], color=color)
            plt.xlabel("Nº de inmobiliarias que la mencionan")
            plt.title(f"Zonas {nombre} según inmobiliarias (n={int(I[cols].notna().any(axis=1).sum())})")
            plt.tight_layout(); plt.savefig(f"{OUT}inmob_zonas_{tipo}.png", dpi=130); plt.close()

    # resumen numérico
    num = ["precio_cierre_zonas_caras_usd", "precio_cierre_zonas_baratas_usd", "rebaja_pct", "meses_venta", "aumento_valor_pct"]
    resumen = I[num].apply(pd.to_numeric, errors="coerce").agg(["count", "mean", "median", "min", "max"]).round(1).T
    resumen.to_csv("entrevistas/resumen_inmobiliarias.csv")
    print(resumen)

    # motivos de venta (promedio)
    mot = I[["motivo_emigracion_pct", "motivo_dinero_pct", "motivo_mudanza_pct"]].apply(pd.to_numeric, errors="coerce").mean()
    if mot.notna().any():
        plt.figure(figsize=(6, 6))
        plt.pie(mot.values, labels=["Emigración", "Necesidad de dinero", "Mudanza"], autopct="%1.0f%%", startangle=90)
        plt.title(f"Motivo de venta (promedio, n={int(I[['motivo_emigracion_pct']].notna().sum().iloc[0])})")
        plt.tight_layout(); plt.savefig(f"{OUT}inmob_motivos_venta.png", dpi=130); plt.close()

    # composición de catálogo (promedio)
    cat = I[["catalogo_casas_pct", "catalogo_apto_pct", "catalogo_otros_pct"]].apply(pd.to_numeric, errors="coerce").mean()
    if cat.notna().any():
        plt.figure(figsize=(6, 6))
        plt.pie(cat.values, labels=["Casas", "Apartamentos", "Otros"], autopct="%1.0f%%", startangle=90)
        plt.title(f"Composición del catálogo (promedio, n={int(I[['catalogo_casas_pct']].notna().sum().iloc[0])})")
        plt.tight_layout(); plt.savefig(f"{OUT}inmob_catalogo.png", dpi=130); plt.close()

    # servicio más valorado
    s = I["servicio_mas_valorado"].dropna().astype(str).str.strip().str.title().value_counts()
    if len(s):
        plt.figure(figsize=(6, 4))
        plt.bar(s.index, s.values, color="#8e44ad")
        plt.title(f"Servicio más valorado por compradores (n={int(s.sum())})")
        plt.tight_layout(); plt.savefig(f"{OUT}inmob_servicio.png", dpi=130); plt.close()
    print(f"Gráficos de inmobiliarias listos (n={m}).")
