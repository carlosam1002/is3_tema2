"""Reportes de gestion (Incremento 3): tramites por estado y tiempos (F3.14) y recaudacion (F3.15).
El reporte de uso del portal (F3.16) se movio a v1.3.0 por RCA-03."""
from collections import Counter, defaultdict

from .solicitudes import DIA


class ServicioReportes:
    def __init__(self, solicitudes, pagos):
        self._solicitudes = solicitudes
        self._pagos = pagos

    def tramites(self):
        todas = self._solicitudes.todas()
        por_estado = Counter(s["estado"] for s in todas)
        dias = defaultdict(list)
        for s in todas:
            if s["estado"] == "resuelta":
                dias[s["tramite"]].append((s["linea_tiempo"][-1]["momento"] - s["creada"]) / DIA)
        return {"total": len(todas), "por_estado": dict(sorted(por_estado.items())),
                "dias_promedio_resolucion": {t: round(sum(v) / len(v), 1) for t, v in sorted(dias.items())},
                "vencidas": sum(1 for s in self._solicitudes.bandeja() if s["vencida"])}

    def recaudacion(self):
        aprobados = [t for t in self._pagos.transacciones() if t["estado"] == "aprobado"]
        por_concepto = defaultdict(int)
        for t in aprobados:
            por_concepto[t["concepto"]] += t["monto"]
        return {"cantidad_pagos": len(aprobados), "total": sum(t["monto"] for t in aprobados),
                "por_concepto": dict(sorted(por_concepto.items()))}
