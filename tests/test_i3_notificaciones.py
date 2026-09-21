"""I3 - Notificaciones por correo, preferencias y bandeja."""
import unittest

from portal.adaptadores.proveedor_correo import ProveedorCorreoSimulado
from portal.errores import DatosInvalidos
from portal.notificaciones import ServicioNotificaciones


class TestNotificaciones(unittest.TestCase):
    def setUp(self):
        self.prov = ProveedorCorreoSimulado()
        self.n = ServicioNotificaciones(self.prov, lambda u: f"{u}@alumnos.ejemplo.edu.py")

    def test_notifica_y_envia_correo(self):
        r = self.n.notificar("est001", "solicitud_estado", "Tu solicitud avanzó", "Estado: en revisión")
        self.assertEqual(r["envio"], "enviado")
        self.assertEqual(self.prov.enviados[0]["destinatario"], "est001@alumnos.ejemplo.edu.py")
        self.assertEqual(len(self.n.bandeja("est001")), 1)

    def test_respeta_preferencias(self):
        self.n.actualizar_preferencias("est001", tipos=["pago_confirmado"])
        r = self.n.notificar("est001", "solicitud_estado", "a", "b")
        self.assertEqual(r["envio"], "no_requerido")
        self.assertEqual(self.prov.enviados, [])
        self.assertEqual(len(self.n.bandeja("est001")), 1)  # queda en la bandeja del portal
        with self.assertRaises(DatosInvalidos):
            self.n.actualizar_preferencias("est001", tipos=["spam"])

    def test_proveedor_caido_deja_pendiente_y_reintenta(self):
        self.prov.disponible = False
        self.assertEqual(self.n.notificar("est001", "pago_confirmado", "a", "b")["envio"], "pendiente")
        self.prov.disponible = True
        self.n.reintentar_pendientes()
        self.assertEqual(self.n.bandeja("est001")[0]["envio"], "enviado")

    def test_marcar_leida(self):
        nid = self.n.notificar("est001", "pago_confirmado", "a", "b")["id"]
        self.assertTrue(self.n.marcar_leida("est001", nid)["leida"])


if __name__ == "__main__":
    unittest.main()
