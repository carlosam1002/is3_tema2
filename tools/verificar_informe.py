"""Contrasta las cifras del informe del TP 2 contra la salida de tools/estimacion.py.

Uso:  python tools/verificar_informe.py ruta/al/informe.pdf
Requiere pdftotext (poppler-utils). Devuelve codigo 1 si encuentra alguna diferencia.
"""
import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def formato_py(valor):
    """Formato paraguayo: punto de miles y coma decimal (2.304,2)."""
    return f"{valor:,.1f}".replace(",", "@").replace(".", ",").replace("@", ".")


CIFRAS = [
    ("E_PERT de I1 en la linea base", 711.7),
    ("E_PERT de I2 en la linea base", 717.5),
    ("E_PERT de I3 en la linea base", 875.0),
    ("E_PERT total de la linea base", 2304.2),
    ("Desvio estandar del proyecto", 153.2),
    ("E_PERT del nucleo Must de I1", 636.7),
    ("Valor al 84 % del nucleo Must de I1", 698.7),
    ("E_PERT de I2 recalibrado", 793.8),
    ("E_PERT de I3 recalibrado", 911.7),
    ("E_PERT de I3 tras el evento de cambio", 902.9),
    ("E_PERT de I2 sin aplicar R-MA", 829.0),
    ("E_PERT de I3 sin aplicar R-MA", 924.0),
]

TEXTOS = [
    ("Capacidad recalibrada de 115 h/semana", "115.0 h/sem", "115 h"),
    ("Costo total recalibrado de 192,2 MGs", "192.2 MGs", "192,2"),
    ("Incertidumbre relativa recalibrada de 7,6 %", "recalibrado=7.6%", "7,6 %"),
    ("Diferencia de esfuerzo por el evento: -8,8 h", "-8.8 h", "8,8 h"),
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pdf = sys.argv[1]
    informe = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                             capture_output=True, text=True).stdout
    script = subprocess.run([sys.executable, "tools/estimacion.py"],
                            capture_output=True, text=True, cwd=RAIZ).stdout

    ok = fallas = 0
    for nombre, valor in CIFRAS:
        en_script = f"{valor:.1f}" in script
        en_informe = formato_py(valor) in informe
        bien = en_script and en_informe
        ok, fallas = ok + bien, fallas + (not bien)
        print(f"{'OK' if bien else 'FALLA':5}  {nombre:42} {formato_py(valor):>9}")

    for nombre, patron_script, patron_informe in TEXTOS:
        bien = patron_script in script and patron_informe in informe
        ok, fallas = ok + bien, fallas + (not bien)
        print(f"{'OK' if bien else 'FALLA':5}  {nombre:42}")

    print(f"\n{ok} verificaciones correctas, {fallas} con diferencias")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
