"""Consultas academicas (F1.04 a F1.07) sobre el sistema academico institucional."""
from .errores import NoEncontrado


class ServicioConsultas:
    def __init__(self, academico):
        self._academico = academico

    def _leer(self, metodo, usuario):
        try:
            return getattr(self._academico, metodo)(usuario)
        except KeyError:
            raise NoEncontrado("El usuario no tiene registro académico")

    def calificaciones(self, usuario):
        return self._leer("calificaciones", usuario)

    def horario(self, usuario):
        return self._leer("horario", usuario)

    def historial(self, usuario):
        h = self._leer("historial", usuario)
        avance = round(100 * len(h["aprobadas"]) / h["total_malla"], 1) if h["total_malla"] else 0.0
        return dict(h, avance_porcentaje=avance)

    def inscripcion(self, usuario):
        return self._leer("inscripcion", usuario)
