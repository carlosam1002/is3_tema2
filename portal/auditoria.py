"""Registro de auditoria de accesos y operaciones (archivo interno F1.09)."""
import time


class RegistroAuditoria:
    def __init__(self, reloj=time.time):
        self._eventos = []
        self._reloj = reloj

    def registrar(self, usuario, evento, detalle=None):
        self._eventos.append({"momento": self._reloj(), "usuario": usuario, "evento": evento, "detalle": detalle})

    def eventos(self, usuario=None, evento=None):
        return [e for e in self._eventos
                if (usuario is None or e["usuario"] == usuario) and (evento is None or e["evento"] == evento)]
