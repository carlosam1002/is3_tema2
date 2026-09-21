"""I3 - Integracion solicitudes -> notificaciones y cancelacion (F2.14, RCA-02)."""
import unittest

from portal.app import Portal
from portal.errores import DatosInvalidos, NoAutorizado


class TestEventosSolicitudes(unittest.TestCase):
    def setUp(self):
        self.p = Portal()
        self.sid = self.p.solicitudes.crear("est001", "CERT-EST", "Para beca")["id"]

    def test_cambio_de_estado_notifica_por_correo(self):
        self.p.solicitudes.cambiar_estado("fun001", self.sid, "en_revision")
        bandeja = self.p.notificaciones.bandeja("est001")
        self.assertEqual(bandeja[0]["tipo"], "solicitud_estado")
        self.assertEqual(self.p.correo.enviados[0]["destinatario"], "est001@alumnos.ejemplo.edu.py")

    def test_cancelar_desde_recibida_sin_autonotificacion(self):
        self.assertEqual(self.p.solicitudes.cancelar("est001", self.sid)["estado"], "cancelada")
        self.assertEqual(self.p.notificaciones.bandeja("est001"), [])
        self.assertNotIn(self.sid, [x["id"] for x in self.p.solicitudes.bandeja()])

    def test_no_cancela_en_revision_ni_ajena(self):
        with self.assertRaises(NoAutorizado):
            self.p.solicitudes.cancelar("est002", self.sid)
        self.p.solicitudes.cambiar_estado("fun001", self.sid, "en_revision")
        with self.assertRaises(DatosInvalidos):
            self.p.solicitudes.cancelar("est001", self.sid)


if __name__ == "__main__":
    unittest.main()
