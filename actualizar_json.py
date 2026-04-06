import json
import csv

JSON_ORIGINAL = "estructura.json"
CSV_FRAGMENTOS = "fragmentos_por_dia.csv"
JSON_SALIDA = "estructura_actualizado.json"

def actualizar_json():
    # Leer el CSV
    asignaciones = {}
    with open(CSV_FRAGMENTOS, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dia = int(row["dia"])
            asignaciones[dia] = {
                "consideraciones_extra": [row["consideracion"]],
                "citas": [{
                    "autor": row["cita_autor"],
                    "texto": row["cita_texto"],
                    "referencia": row["cita_referencia"]
                }]
            }

    # Leer JSON original
    with open(JSON_ORIGINAL, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Recorrer el JSON y añadir los campos a cada tema de los días
    for trayecto in data.get("trayectos", []):
        for semestre in trayecto.get("semestres", []):
            for clase in semestre.get("clases", []):
                for tema in clase.get("temas", []):
                    tema_id = tema.get("id", "")
                    # Extraer número del id (ej. "dia23" -> 23)
                    numero = None
                    if tema_id.startswith("dia"):
                        try:
                            numero = int(tema_id[3:])
                        except:
                            pass
                    if numero and 1 <= numero <= 40 and numero in asignaciones:
                        tema["consideraciones_extra"] = asignaciones[numero]["consideraciones_extra"]
                        tema["citas"] = asignaciones[numero]["citas"]
                        print(f"✅ Añadido al tema {tema_id} (día {numero})")

    # Guardar JSON actualizado
    with open(JSON_SALIDA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON actualizado guardado como {JSON_SALIDA}")

if __name__ == "__main__":
    actualizar_json()