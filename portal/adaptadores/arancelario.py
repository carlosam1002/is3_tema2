"""Adaptador del sistema arancelario / financiero (archivo externo F3.11).

Contrato de interfaz:
    deudas(usuario) -> list[dict {id, concepto, monto, vencimiento}]   (monto en guaranies)
    registrar_pago(id_deuda: str, referencia: str, monto: int) -> str  numero de recibo
    Un pago con monto distinto a la deuda lanza ValueError.
"""
import itertools


class SistemaArancelarioSimulado:
    def __init__(self):
        self._deudas = {
            "est001": [
                {"id": "D-1001", "concepto": "Cuota 7 - Matrícula 2026", "monto": 350_000, "vencimiento": "2026-10-10"},
                {"id": "D-1002", "concepto": "Derecho de examen final", "monto": 120_000, "vencimiento": "2026-11-20"},
            ],
            "est002": [
                {"id": "D-2001", "concepto": "Cuota 7 - Matrícula 2026", "monto": 350_000, "vencimiento": "2026-10-10"},
            ],
        }
        self._recibos = itertools.count(1)

    def deudas(self, usuario):
        return [dict(d) for d in self._deudas.get(usuario, [])]

    def registrar_pago(self, id_deuda, referencia, monto):
        for lista in self._deudas.values():
            for d in lista:
                if d["id"] == id_deuda:
                    if d["monto"] != monto:
                        raise ValueError("Monto distinto a la deuda")
                    lista.remove(d)
                    return f"REC-{next(self._recibos):06d}"
        raise KeyError(id_deuda)
