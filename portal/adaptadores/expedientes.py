"""Adaptador del sistema de expedientes / mesa de entrada (archivo externo F2.11).

Contrato de interfaz (acordado con Mesa de Entrada y la Direccion TIC):
    registrar(tramite: str, usuario: str, resumen: str) -> str  numero "EXP-AAAA-NNNNNN"
    Si el sistema no esta disponible lanza ConnectionError.
"""


class ExpedientesSimulado:
    def __init__(self, anio=2026):
        self.anio = anio
        self.disponible = True
        self.registrados = []

    def registrar(self, tramite, usuario, resumen):
        if not self.disponible:
            raise ConnectionError("Sistema de expedientes no disponible")
        self.registrados.append((tramite, usuario, resumen))
        return f"EXP-{self.anio}-{len(self.registrados):06d}"
