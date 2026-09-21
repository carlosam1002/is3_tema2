"""Pagos en linea de aranceles (Incremento 3).

Funciones: estado de cuenta (F3.01), iniciar pago (F3.02), confirmacion por callback firmado
(F3.03), comprobante (F3.04), historial (F3.05) y transacciones (archivo interno F3.07).
El portal no recibe ni almacena datos de tarjetas: el pago ocurre en la pasarela.
"""
import itertools
import time

from .errores import DatosInvalidos, NoAutorizado, NoEncontrado
from .pdf import generar_pdf


class ServicioPagos:
    def __init__(self, pasarela, arancelario, notificaciones, auditoria, reloj=time.time):
        self._pasarela = pasarela
        self._arancelario = arancelario
        self._notificaciones = notificaciones
        self._auditoria = auditoria
        self._reloj = reloj
        self._transacciones = {}  # referencia -> transaccion
        self._ids = itertools.count(1)

    def estado_cuenta(self, usuario):
        deudas = self._arancelario.deudas(usuario)
        return {"deudas": deudas, "total": sum(d["monto"] for d in deudas)}

    def iniciar_pago(self, usuario, id_deuda):
        deuda = next((d for d in self._arancelario.deudas(usuario) if d["id"] == id_deuda), None)
        if not deuda:
            raise NoEncontrado("Deuda inexistente o ya pagada")
        referencia = f"PAG-{next(self._ids):06d}"
        orden = self._pasarela.crear_orden(referencia, deuda["monto"])
        self._transacciones[referencia] = {
            "referencia": referencia, "usuario": usuario, "id_deuda": id_deuda, "concepto": deuda["concepto"],
            "monto": deuda["monto"], "id_orden": orden["id_orden"], "estado": "iniciado",
            "recibo": None, "iniciado": self._reloj(), "confirmado": None}
        self._auditoria.registrar(usuario, "pago_iniciado", referencia)
        return {"referencia": referencia, "url_pago": orden["url_pago"], "monto": deuda["monto"]}

    def confirmar(self, notificacion):
        """Callback de la pasarela. Idempotente: una confirmacion repetida no duplica el pago."""
        if not self._pasarela.verificar(notificacion):
            raise NoAutorizado("Firma de la pasarela inválida")
        t = self._transacciones.get(notificacion.get("referencia"))
        if not t or t["id_orden"] != notificacion.get("id_orden"):
            raise NoEncontrado("Transacción inexistente")
        if notificacion.get("monto") != t["monto"]:
            raise DatosInvalidos("El monto confirmado no coincide con la orden")
        if t["estado"] != "iniciado":
            return dict(t)
        if notificacion.get("estado") == "aprobado":
            t["recibo"] = self._arancelario.registrar_pago(t["id_deuda"], t["referencia"], t["monto"])
            t["estado"] = "aprobado"
            self._notificaciones.notificar(
                t["usuario"], "pago_confirmado", "Pago confirmado",
                f"Recibimos tu pago de Gs. {t['monto']:,} por {t['concepto']}. Recibo {t['recibo']}.".replace(",", "."))
        else:
            t["estado"] = "rechazado"
        t["confirmado"] = self._reloj()
        self._auditoria.registrar(t["usuario"], "pago_" + t["estado"], t["referencia"])
        return dict(t)

    def historial(self, usuario):
        return [dict(t) for t in self._transacciones.values() if t["usuario"] == usuario]

    def transacciones(self):
        return [dict(t) for t in self._transacciones.values()]

    def comprobante_pdf(self, usuario, referencia):
        t = self._transacciones.get(referencia)
        if not t or t["usuario"] != usuario:
            raise NoEncontrado("Transacción inexistente")
        if t["estado"] != "aprobado":
            raise DatosInvalidos("Solo los pagos aprobados tienen comprobante")
        return generar_pdf("Comprobante de pago", [
            f"Referencia: {t['referencia']} - Recibo: {t['recibo']}", f"Concepto: {t['concepto']}",
            f"Monto: Gs. {t['monto']:,}".replace(",", "."), "Medio: pasarela de pagos (sin datos de tarjeta en el portal)"])
