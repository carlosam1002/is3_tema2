"""Adaptador de la pasarela de pagos (archivo externo F3.09).

El pago se realiza en la pagina alojada por la pasarela: el portal NUNCA recibe ni
almacena datos de tarjetas. Contrato de interfaz:
    crear_orden(referencia: str, monto: int) -> dict {id_orden, url_pago}
    verificar(notificacion: dict) -> bool   valida la firma HMAC de la confirmacion
La confirmacion (callback) contiene: id_orden, referencia, monto, estado ('aprobado'|'rechazado'), firma.
"""
import hashlib
import hmac
import itertools
import json


class PasarelaSimulada:
    def __init__(self, secreto=b"secreto-de-prueba"):
        self._secreto = secreto
        self._ordenes = {}
        self._ids = itertools.count(1)

    def crear_orden(self, referencia, monto):
        id_orden = f"ORD-{next(self._ids):06d}"
        self._ordenes[id_orden] = {"referencia": referencia, "monto": monto}
        return {"id_orden": id_orden, "url_pago": f"https://pasarela.ejemplo/pagar/{id_orden}"}

    def _firmar(self, datos):
        mensaje = json.dumps(datos, sort_keys=True).encode()
        return hmac.new(self._secreto, mensaje, hashlib.sha256).hexdigest()

    def verificar(self, notificacion):
        datos = {k: v for k, v in notificacion.items() if k != "firma"}
        return hmac.compare_digest(self._firmar(datos), str(notificacion.get("firma", "")))

    # --- solo para pruebas: simula que el estudiante completa el pago en la pasarela
    def simular_pago(self, id_orden, aprobado=True):
        orden = self._ordenes[id_orden]
        datos = {"id_orden": id_orden, "referencia": orden["referencia"], "monto": orden["monto"],
                 "estado": "aprobado" if aprobado else "rechazado"}
        return dict(datos, firma=self._firmar(datos))
