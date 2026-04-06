import re
import csv
import os

# Configuración
ARCHIVO_TEXTO = "La_Curación_Por_El_Ayuno.txt"
SALIDA_CSV = "fragmentos_por_dia.csv"
NUM_DIAS = 40

# Palabras clave para identificar fragmentos relevantes
PALABRAS_CLAVE = [
    "ayuno", "hambre", "cura", "enfermedad", "dolencia", "salud", "purificación",
    "lengua", "sedimento", "autofagia", "cetosis", "cuerpos cetónicos", "acetona",
    "enema", "purgante", "agua", "limón", "coco", "electrolitos", "minerales",
    "corazón", "arterias", "aorta", "esclerosis", "reuma", "artritis", "cáncer",
    "diabetes", "úlcera", "hidropesía", "neurastenia", "nervios", "neurosis",
    "Kellogg", "Suvorin", "Carton", "Guelpa", "Ehret", "Hipócrates"
]

def extraer_fragmentos():
    if not os.path.exists(ARCHIVO_TEXTO):
        print(f"❌ No se encuentra el archivo {ARCHIVO_TEXTO}")
        return

    with open(ARCHIVO_TEXTO, "r", encoding="utf-8") as f:
        texto = f.read()

    # Dividir en párrafos (por dos o más saltos de línea)
    parrafos = re.split(r'\n\s*\n', texto)
    parrafos = [p.strip() for p in parrafos if len(p.strip()) > 100]  # ignorar muy cortos

    # Filtrar párrafos que contengan al menos una palabra clave
    relevantes = []
    for p in parrafos:
        if any(kw.lower() in p.lower() for kw in PALABRAS_CLAVE):
            # Limpiar saltos de línea internos
            p_clean = re.sub(r'\s+', ' ', p)
            relevantes.append(p_clean)

    print(f"✅ Se encontraron {len(relevantes)} párrafos relevantes.")

    # Asignar fragmentos a los 40 días (cíclicamente)
    asignacion = []
    for i in range(NUM_DIAS):
        idx = i % len(relevantes)
        fragmento = relevantes[idx]
        # Acortar si es demasiado largo (máx 500 caracteres)
        if len(fragmento) > 500:
            fragmento = fragmento[:500] + "..."
        asignacion.append({
            "dia": i+1,
            "consideracion": fragmento,
            "cita_autor": "Alexi Suvorin (extraído de 'La Curación por El Ayuno')",
            "cita_texto": fragmento[:200] + "...",
            "cita_referencia": "La Curación por El Ayuno, s/f"
        })

    # Guardar CSV
    with open(SALIDA_CSV, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["dia", "consideracion", "cita_autor", "cita_texto", "cita_referencia"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asignacion)

    print(f"✅ CSV generado: {SALIDA_CSV}")

if __name__ == "__main__":
    extraer_fragmentos()