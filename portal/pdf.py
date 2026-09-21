"""Generador minimo de PDF de una pagina (sin dependencias externas)."""


def _esc(texto):
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generar_pdf(titulo, lineas):
    ops = ["BT", "/F1 14 Tf", "50 790 Td", f"({_esc(titulo)}) Tj", "/F1 10 Tf", "0 -8 Td"]
    for linea in lineas:
        ops += ["0 -16 Td", f"({_esc(str(linea))}) Tj"]
    ops.append("ET")
    stream = "\n".join(ops).encode("cp1252", "replace")
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
    ]
    salida = bytearray(b"%PDF-1.4\n")
    posiciones = []
    for i, obj in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida += b"%d 0 obj\n" % i + obj + b"\nendobj\n"
    xref = len(salida)
    salida += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objetos) + 1)
    for pos in posiciones:
        salida += b"%010d 00000 n \n" % pos
    salida += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objetos) + 1, xref)
    return bytes(salida)
