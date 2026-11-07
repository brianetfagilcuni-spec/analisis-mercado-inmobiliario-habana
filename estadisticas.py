"""Estadísticas de los anuncios y de las entrevistas. Ejecutar desde la raíz del repositorio:
    python codigo/estadisticas.py
Salidas: datos/limpios/estadisticas.csv y graficos/grafico_14..16.
Reglas: precio corregido; mediana (no promedio); con menos de 5 anuncios en un grupo no se concluye."""
import re
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
d = pd.read_csv("datos/limpios/inmuebles_habana_pro.csv")
a = pd.read_csv("datos/limpios/inmuebles_auditados.csv")
d["Precio"] = a["Precio_corregido"].values
d["Municipio"] = a["Municipio"].values
d["flag_dup"] = a["flag_duplicado"].values
SI = lambda c: d[c].astype(str).str.startswith("S")
filas = []

def mediana_ic(x, B=2000):
    b = [np.median(rng.choice(x, len(x))) for _ in range(B)]
    return np.percentile(b, [2.5, 97.5])

def comparar(nombre, mask):
    """Compara precio entre dos grupos (con vs sin). Mann-Whitney y bootstrap de la diferencia de medianas."""
    g1, g0 = d.loc[mask, "Precio"].values, d.loc[~mask, "Precio"].values
    r = dict(comparacion=nombre, n_con=len(g1), n_sin=len(g0),
             mediana_con=np.median(g1) if len(g1) else np.nan, mediana_sin=np.median(g0) if len(g0) else np.nan)
    if min(len(g1), len(g0)) < 5:
        r.update(p_mannwhitney=np.nan, dif_mediana_ic95="", concluyente="no (grupo < 5)")
    else:
        p = stats.mannwhitneyu(g1, g0).pvalue
        dif = [np.median(rng.choice(g1, len(g1))) - np.median(rng.choice(g0, len(g0))) for _ in range(2000)]
        lo, hi = np.percentile(dif, [2.5, 97.5])
        r.update(p_mannwhitney=round(p, 4), dif_mediana_ic95=f"[{lo:,.0f}; {hi:,.0f}]",
                 concluyente="sí" if p < 0.05 else "no")
    filas.append(r)

# ---- Descriptivas ----
p = d["Precio"]
print(f"n={len(p)} mediana={p.median():,.0f} Q1={p.quantile(.25):,.0f} Q3={p.quantile(.75):,.0f} media={p.mean():,.0f} "
      f"media/mediana={p.mean()/p.median():.2f}  IC95 mediana={mediana_ic(p.values)}")
print("sin duplicados: n=%d mediana=%.0f" % ((~d.flag_dup).sum(), d.loc[~d.flag_dup, "Precio"].median()))

# ---- Municipio ----
m = d.groupby("Municipio")["Precio"].agg(n="count", mediana="median", q1=lambda x: x.quantile(.25), q3=lambda x: x.quantile(.75)).sort_values("mediana", ascending=False)
print(m)
m.to_csv("datos/limpios/estadisticas_municipio.csv")
comparar("Plaza de la Revolución vs resto", d.Municipio == "Plaza de la Revolución")
comparar("Playa vs resto", d.Municipio == "Playa")
alta = d.Municipio.isin(["Plaza de la Revolución", "Playa", "Habana del Este"])
comparar("Municipios caros (Plaza, Playa, H. del Este) vs resto", alta)
cp = d[d.Municipio.isin(["Centro Habana", "Plaza de la Revolución"])]
u = stats.mannwhitneyu(cp[cp.Municipio == "Centro Habana"].Precio, cp[cp.Municipio != "Centro Habana"].Precio)
filas.append(dict(comparacion="Centro Habana vs Plaza de la Revolución", n_con=(cp.Municipio == "Centro Habana").sum(),
                  n_sin=(cp.Municipio != "Centro Habana").sum(), mediana_con=cp[cp.Municipio == "Centro Habana"].Precio.median(),
                  mediana_sin=cp[cp.Municipio != "Centro Habana"].Precio.median(), p_mannwhitney=round(u.pvalue, 4),
                  dif_mediana_ic95="", concluyente="sí" if u.pvalue < .05 else "no"))

# ---- Tipo ----
print(d.groupby("Tipo_Inmueble")["Precio"].agg(["count", "median"]))
comparar("Casa vs resto", d.Tipo_Inmueble == "Casa")
comparar("Apartamento vs resto", d.Tipo_Inmueble == "Apartamento")

# ---- Características y servicios ----
for c in ["Agua", "Luz", "Gas", "Teléfono", "Internet", "Garaje", "Patio", "Terraza", "Balcon", "Jardín", "Piscina",
          "Placa_Libre", "Independiente", "Amoblado", "Negociable", "Permuta", "Vista_al_mar"]:
    comparar(f"Con {c}", SI(c))
comparar("Marcado Es_Oportunidad (definición no documentada)", d.Es_Oportunidad.astype(str).str.startswith("S"))

# ---- Cuartos y baños (0 = no indicado) ----
for c in ["Cuartos", "Baños"]:
    sub = d[d[c] > 0]
    if len(sub) >= 5:
        r, pv = stats.spearmanr(sub[c], sub["Precio"])
        print(f"Spearman {c} vs precio (n={len(sub)} con dato): rho={r:.2f} p={pv:.3f}")
        filas.append(dict(comparacion=f"Spearman {c} vs precio (solo anuncios que lo indican)", n_con=len(sub), n_sin=len(d) - len(sub),
                          mediana_con=round(r, 2), mediana_sin=np.nan, p_mannwhitney=round(pv, 4), dif_mediana_ic95="rho en 'mediana_con'",
                          concluyente="sí" if pv < .05 else "no"))

# ---- ¿Zona o servicios? R² ajustado ----
srv = ["Agua", "Luz", "Gas", "Garaje", "Patio", "Terraza", "Balcon", "Piscina", "Placa_Libre", "Teléfono"]
d["n_serv"] = sum(SI(c).astype(int) for c in srv)
d["zona_alta"] = alta.astype(int)
d["casa"] = d.Tipo_Inmueble.isin(["Casa", "Biplanta"]).astype(int)
y = np.log(d["Precio"].values)
def r2aj(cols):
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ b
    r2 = 1 - res.var() / y.var(); k = len(cols)
    return 1 - (1 - r2) * (len(y) - 1) / (len(y) - k - 1), b
modelos = {"Solo zona alta": ["zona_alta"], "Solo n.º de servicios": ["n_serv"], "Solo tipo (casa/biplanta)": ["casa"],
           "Zona + tipo": ["zona_alta", "casa"], "Zona + servicios + tipo": ["zona_alta", "n_serv", "casa"]}
reg = []
for k, v in modelos.items():
    r2, b = r2aj(v); reg.append((k, round(r2, 3), [round(float(x), 2) for x in b]))
    print(k, round(r2, 3), [round(float(x), 2) for x in b])
pd.DataFrame([(k, r) for k, r, _ in reg], columns=["modelo", "r2_ajustado"]).to_csv("datos/limpios/estadisticas_modelos.csv", index=False)
# ¿qué pasa con los servicios dentro de la misma zona?
print("Mediana por n_serv dentro de zona alta / resto:")
print(d.groupby(["zona_alta", pd.cut(d.n_serv, [-1, 0, 1, 10])])["Precio"].agg(["count", "median"]))

res = pd.DataFrame(filas)
res.to_csv("datos/limpios/estadisticas.csv", index=False)
print(res.to_string())

# ---- Palabras en los anuncios ----
txt = (d["Título"].fillna("") + " " + d["Descripción"].fillna("")).str.lower()
for w in ["oportunidad", "negociable", "urgente", "ganga", "céntrico|centrico", "excelente", "luminos", "remodelad|reparad", "placa libre",
          "emigr|viaj|salgo del pa", "herencia|documentos|escritura|propiedad", "cisterna|agua"]:
    print(w, int(txt.str.contains(w).sum()))

# ================= GRÁFICOS =================
azul, gris = "#2a5298", "#9aa5b8"
# G14: cajas por municipio (n >= 5)
ok = m[m.n >= 5].index
orden = d[d.Municipio.isin(ok)].groupby("Municipio")["Precio"].median().sort_values().index
plt.figure(figsize=(8, 5))
plt.boxplot([d[d.Municipio == k]["Precio"] for k in orden], vert=False, showfliers=True)
plt.yticks(range(1, len(orden) + 1), [f"{k} (n={m.loc[k,'n']})" for k in orden])
plt.xscale("log"); plt.xlabel("Precio publicado (USD, escala logarítmica)")
plt.title("Dispersión del precio por municipio (solo municipios con 5 o más anuncios)")
plt.tight_layout(); plt.savefig("graficos/grafico_14_cajas_municipio.png", dpi=130); plt.close()

# G15: precio mediano con / sin cada servicio
srvs = ["Agua", "Luz", "Gas", "Garaje", "Patio", "Placa_Libre", "Independiente", "Teléfono"]
con = [d.loc[SI(c), "Precio"].median() for c in srvs]; sin = [d.loc[~SI(c), "Precio"].median() for c in srvs]
ns = [int(SI(c).sum()) for c in srvs]
x = np.arange(len(srvs)); plt.figure(figsize=(8.5, 5))
plt.bar(x - .2, con, .4, color=azul, label="Anuncio lo menciona"); plt.bar(x + .2, sin, .4, color=gris, label="No lo menciona")
plt.xticks(x, [f"{c}\n(n={n})" for c, n in zip(srvs, ns)], fontsize=8); plt.ylabel("Mediana (USD)")
plt.title("Precio mediano según lo que menciona el anuncio\n(diferencias no concluyentes si n pequeño; ver estadisticas.csv)")
plt.legend(); plt.tight_layout(); plt.savefig("graficos/grafico_15_servicios_precio.png", dpi=130); plt.close()

# G16: lo que se ofrece vs lo que se prefiere
P = pd.read_csv("entrevistas/personas.csv")
pref = P["p3_tipo"].dropna().str[0].value_counts(normalize=True) * 100
oferta = d["Tipo_Inmueble"].replace({"Biplanta": "Biplanta"}).value_counts(normalize=True) * 100
cats = ["Casa", "Apartamento", "Biplanta"]
v_of = [oferta.get(c, 0) for c in cats]; v_pr = [pref.get("A", 0), pref.get("B", 0), pref.get("C", 0)]
x = np.arange(3); plt.figure(figsize=(7, 4.5))
plt.bar(x - .2, v_of, .4, color=azul, label=f"Ofertado en Revolico (n={len(d)})")
plt.bar(x + .2, v_pr, .4, color="#e07b39", label=f"Preferido por personas (n={P['p3_tipo'].notna().sum()})")
for i, (u, w) in enumerate(zip(v_of, v_pr)):
    plt.text(i - .2, u + 1, f"{u:.0f}%", ha="center", fontsize=9); plt.text(i + .2, w + 1, f"{w:.0f}%", ha="center", fontsize=9)
plt.xticks(x, cats); plt.ylabel("%"); plt.title("Tipo de vivienda: lo que se ofrece vs. lo que se prefiere")
plt.legend(); plt.tight_layout(); plt.savefig("graficos/grafico_16_oferta_vs_preferencia.png", dpi=130); plt.close()

# ---- Personas: conteos ----
def cuenta(col, letras):
    s = P[col].dropna().astype(str); s = s[s != ""]
    return len(s), {k: int(s.str.contains(k).sum()) for k in letras}
for col, L in [("p1_valora", "ABCDT"), ("p2_zona_cara", "ABCD"), ("p3_tipo", "ABC"), ("p4_servicio", "ABCD"), ("p5_precios", "ABC")]:
    print(col, cuenta(col, L))
print("servicios en anuncios %:", {c: round(SI(c).mean() * 100, 1) for c in ["Agua", "Luz", "Gas", "Teléfono", "Internet", "Garaje", "Patio"]})
