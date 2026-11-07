"""Agrega una respuesta de persona al CSV. Uso:  python scripts/cargar_respuesta.py
Pega el texto como te lo mandan. Acepta: 1A 2B 3C | 1-c 2-b | 1AB (varias opciones) | 1Todas.
Si falta alguna pregunta, te pregunta si la dejas en blanco. Códigos: P01, P02... (sin nombres ni teléfonos)."""
import csv, re

RUTA = "entrevistas/personas.csv"
validas = {"1": "ABCD", "2": "ABCD", "3": "ABC", "4": "ABCD", "5": "ABC"}

n = sum(1 for _ in open(RUTA, encoding="utf-8")) - 1
codigo = f"P{n + 1:02d}"
print("Código asignado:", codigo)
texto = input("Respuestas: ").upper().replace(",", " ")
resp = {}
for k, v in re.findall(r"([1-5])\s*[-:.)]?\s*(TOD[AO]S?|[A-D]+)", texto):
    resp[k] = "T" if v.startswith("TOD") else "".join(sorted(set(v)))

malas = [k for k, v in resp.items() if v != "T" and not set(v) <= set(validas[k])]
if malas:
    print("Opción inválida en:", malas); raise SystemExit
faltan = [k for k in validas if k not in resp]
if faltan and input(f"Faltan las preguntas {faltan}. ¿Guardar en blanco? (s/n): ").lower() != "s":
    raise SystemExit

otra = input("Si en la 2 puso D, ¿qué zona? (Enter si no): ").strip() if "D" in resp.get("2", "") else ""
rol = input("Rol (comprador / vendedor / gestora / otro): ").strip().lower() or "otro"

with open(RUTA, "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow([codigo, rol] + [resp.get("1", ""), resp.get("2", ""), otra,
                            resp.get("3", ""), resp.get("4", ""), resp.get("5", "")])
print("Guardado.", codigo)
