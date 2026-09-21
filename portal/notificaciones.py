"""Notificaciones (Incremento 3): envio por correo (F3.06), archivo interno (F3.08),
preferencias (F3.12) y bandeja en el portal (F3.13)."""
import itertools
import time

from .errores import DatosInvalidos, NoEncontrado

TIPOS = {"solicitud_estado", "pago_confirmado"}


class ServicioNotificaciones:
    def __init__(self, proveedor, correo_de, reloj=time.time):
        self._proveedor = proveedor
        self._correo_de = correo_de  # funcion usuario -> correo
        self._reloj = reloj
        self._notificaciones = []
        self._preferencias = {}
        self._ids = itertools.count(1)

    def preferencias(self, usuario):
        return dict({"correo": True, "tipos": sorted(TIPOS)}, **self._preferencias.get(usuario, {}))

    def actualizar_preferencias(self, usuario, correo=None, tipos=None):
        cambios = {}
        if correo is not None:
            cambios["correo"] = bool(correo)
        if tipos is not None:
            if not set(tipos) <= TIPOS:
                raise DatosInvalidos("Tipo de notificación desconocido")
            cambios["tipos"] = sorted(tipos)
        self._preferencias.setdefault(usuario, {}).update(cambios)
        return self.preferencias(usuario)

    def notificar(self, usuario, tipo, asunto, cuerpo):
        n = {"id": next(self._ids), "usuario": usuario, "tipo": tipo, "asunto": asunto, "cuerpo": cuerpo,
             "momento": self._reloj(), "leida": False, "envio": "no_requerido"}
        self._notificaciones.append(n)
        pref = self.preferencias(usuario)
        if pref["correo"] and tipo in pref["tipos"]:
            self._enviar(n)
        return dict(n)

    def reintentar_pendientes(self):
        for n in self._notificaciones:
            if n["envio"] == "pendiente":
                self._enviar(n)

    def bandeja(self, usuario):
        return [dict(n) for n in reversed(self._notificaciones) if n["usuario"] == usuario]

    def marcar_leida(self, usuario, nid):
        for n in self._notificaciones:
            if n["id"] == int(nid) and n["usuario"] == usuario:
                n["leida"] = True
                return dict(n)
        raise NoEncontrado("Notificación inexistente")

    def _enviar(self, n):
        try:
            self._proveedor.enviar(self._correo_de(n["usuario"]), n["asunto"], n["cuerpo"])
            n["envio"] = "enviado"
        except ConnectionError:
            n["envio"] = "pendiente"
