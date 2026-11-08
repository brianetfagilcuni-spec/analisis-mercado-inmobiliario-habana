"""Pruebas automáticas de calidad. Ejecutar desde la carpeta del repositorio:
    python -m unittest test_datos -v
Comprueban que los datos y la documentación coinciden con las cifras que se publican."""
import os, re, glob, unittest
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(ROOT, *a)
def leer(ruta, **kw):
    with open(ruta, encoding="utf-8", **kw) as fh:
        return fh.read()

MUNICIPIOS_HABANA = {"Playa", "Plaza de la Revolución", "Centro Habana", "Habana Vieja", "Regla", "Habana del Este", "Guanabacoa",
                     "San Miguel del Padrón", "Diez de Octubre", "Cerro", "Marianao", "La Lisa", "Boyeros", "Arroyo Naranjo", "Cotorro"}

class TestAnuncios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pro = pd.read_csv(p("inmuebles_habana_pro.csv"))
        cls.aud = pd.read_csv(p("inmuebles_auditados.csv"))

    def test_92_anuncios(self):
        self.assertEqual(len(self.pro), 92)
        self.assertEqual(len(self.aud), 92)

    def test_precio_corregido_valido(self):
        pr = self.aud["Precio_corregido"]
        self.assertTrue(pr.notna().all())
        self.assertGreaterEqual(pr.min(), 1000, "hay precios menores a 1,000 USD sin revisar")

    def test_mediana_corregida(self):
        self.assertEqual(self.aud["Precio_corregido"].median(), 25000)

    def test_16_precios_corregidos(self):
        self.assertEqual(int((self.aud["Precio_corregido"] != self.aud["Precio_original"]).sum()), 16)

    def test_municipios_de_la_habana(self):
        self.assertTrue(set(self.aud["Municipio"]).issubset(MUNICIPIOS_HABANA))

    def test_zonas_caras_frente_al_resto(self):
        alta = self.aud["Municipio"].isin(["Plaza de la Revolución", "Playa", "Habana del Este"])
        self.assertEqual(self.aud.loc[alta, "Precio_corregido"].median(), 60000)
        self.assertEqual(self.aud.loc[~alta, "Precio_corregido"].median(), 15000)

    def test_ninguna_menciona_emigracion(self):
        self.assertTrue((self.pro["Menciona_Emigracion"] == "No").all())

    def test_sin_telefonos_reales(self):
        patron = re.compile(r"(?<!\d)(?:\+?53[ -]?)?[5-7]\d{7}(?!\d)")
        for f in glob.glob(p("*.csv")) + glob.glob(p("*.md")):
            txt = re.sub(r"https?://\S+", "", leer(f, errors="ignore"))
            self.assertIsNone(patron.search(txt), f"posible teléfono en {os.path.basename(f)}")

class TestEntrevistas(unittest.TestCase):
    def test_personas(self):
        d = pd.read_csv(p("personas.csv"))
        self.assertEqual(len(d), 35)
        self.assertEqual(list(d["codigo"]), [f"P{i:02d}" for i in range(1, 36)])
        for col, validas in [("p3_tipo", "ABC"), ("p5_precios", "ABC"), ("p4_servicio", "ABCDT"), ("p1_valora", "ABCDT")]:
            for v in d[col].dropna().astype(str):
                self.assertTrue(set(v).issubset(set(validas)), f"{col}: valor inesperado {v}")

    def test_inmobiliarias(self):
        d = pd.read_csv(p("inmobiliarias.csv"))
        self.assertEqual(list(d["codigo"]), [f"INM{i}" for i in range(1, 6)])

    def test_respuestas_cualitativas(self):
        d = pd.read_csv(p("respuestas_cualitativas.csv"))
        self.assertEqual(len(d), 25)
        self.assertTrue(set(d["tipo"]).issubset({"persona", "inmobiliaria"}))

class TestDocumentacion(unittest.TestCase):
    def test_historia_tiene_30_preguntas(self):
        t = leer(p("historia.md"))
        nums = [int(n) for n in re.findall(r"^\*\*(\d+)\. ", t, re.M)]
        self.assertEqual(nums, list(range(1, 31)))

    def test_imagenes_existen(self):
        for md in ["historia.md", "informe_tecnico.md", "anuncios_fotografias.md"]:
            for ruta in re.findall(r"!\[.*?\]\((.*?)\)", leer(p(md))):
                self.assertTrue(os.path.exists(p(ruta)), f"falta {ruta} (en {md})")

    def test_archivos_clave(self):
        for f in ["README.md", "diccionario_datos.md", "historia.md", "historia.pdf", "informe_tecnico.md", "informe_tecnico.pdf",
                  "bitacora.md", "catalogo_inmobiliarias.md", "tabla_entrevistas.md", "cuestionarios.md", "fuentes.md",
                  "anuncios_fotografias.md", "requirements.txt", "index.html", "plan_campana_comunicacion.md", "plan_campana_comunicacion.pdf"]:
            self.assertTrue(os.path.exists(p(f)), f"falta {f}")

if __name__ == "__main__":
    unittest.main()
