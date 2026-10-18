"""Evento de cambio (Unidad 9): el proveedor externo de correo deja de estar disponible.

El servicio de notificaciones no se modifica: se le inyecta el adaptador del correo
institucional, que cumple el mismo contrato de interfaz.
"""
import unittest

from portal.adaptadores.smtp_institucional import CorreoInstitucionalSimulado
from portal.app import Portal
from portal.notificaciones import ServicioNotificaciones


class ContratoCorreoInstitucional(unittest.TestCase):
    """Mismo contrato que el proveedor externo (ver tests/test_contratos.py)."""

    def test_envio_y_error_de_disponibilidad(self):
        a = CorreoInstitucionalSimulado()
        self.assertRegex(a.enviar("x@ejemplo.edu.py", "asunto", "cuerpo"), r"^SMTP-\d{6}$")
        a.disponible = False
        with self.assertRaises(ConnectionError):
            a.enviar("x@ejemplo.edu.py", "asunto", "cuerpo")

    def test_limite_de_envios_por_hora(self):
        a = CorreoInstitucionalSimulado()
        for _ in range(a.LIMITE_POR_HORA):
            a.enviar("x@ejemplo.edu.py", "a", "b")
        with self.assertRaises(ConnectionError):
            a.enviar("x@ejemplo.edu.py", "a", "b")


class ConmutacionDeProveedor(unittest.TestCase):
    def test_el_portal_notifica_con_el_correo_institucional(self):
        p = Portal(correo=CorreoInstitucionalSimulado())
        sid = p.solicitudes.crear("est001", "CERT-EST", "Para beca")["id"]
        p.solicitudes.cambiar_estado("fun001", sid, "en_revision")
        self.assertEqual(p.correo.enviados[0]["destinatario"], "est001@alumnos.ejemplo.edu.py")
        self.assertEqual(p.notificaciones.bandeja("est001")[0]["envio"], "enviado")

    def test_caida_del_proveedor_deja_pendiente_y_el_reintento_usa_el_nuevo_adaptador(self):
        externo = Portal().correo
        externo.disponible = False
        notif = ServicioNotificaciones(externo, lambda u: f"{u}@alumnos.ejemplo.edu.py")
        self.assertEqual(notif.notificar("est001", "pago_confirmado", "a", "b")["envio"], "pendiente")
        notif._proveedor = CorreoInstitucionalSimulado()  # conmutación del adaptador
        notif.reintentar_pendientes()
        self.assertEqual(notif.bandeja("est001")[0]["envio"], "enviado")


if __name__ == "__main__":
    unittest.main()
