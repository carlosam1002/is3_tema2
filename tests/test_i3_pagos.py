"""I3 - Pagos en linea: estado de cuenta, pago, confirmacion firmada, comprobante e historial."""
import unittest

from portal.adaptadores.arancelario import SistemaArancelarioSimulado
from portal.adaptadores.pasarela import PasarelaSimulada
from portal.adaptadores.proveedor_correo import ProveedorCorreoSimulado
from portal.auditoria import RegistroAuditoria
from portal.errores import DatosInvalidos, NoAutorizado, NoEncontrado
from portal.notificaciones import ServicioNotificaciones
from portal.pagos import ServicioPagos
from tests.utilidades import ServidorDePrueba


class TestPagos(unittest.TestCase):
    def setUp(self):
        self.pas = PasarelaSimulada()
        self.correo = ProveedorCorreoSimulado()
        self.notif = ServicioNotificaciones(self.correo, lambda u: f"{u}@alumnos.ejemplo.edu.py")
        self.p = ServicioPagos(self.pas, SistemaArancelarioSimulado(), self.notif, RegistroAuditoria())

    def _pagar(self, aprobado=True):
        ini = self.p.iniciar_pago("est001", "D-1001")
        orden = self.p.historial("est001")[0]["id_orden"]
        return ini, self.pas.simular_pago(orden, aprobado)

    def test_estado_de_cuenta(self):
        self.assertEqual(self.p.estado_cuenta("est001")["total"], 470_000)

    def test_pago_aprobado_registra_recibo_notifica_y_reduce_deuda(self):
        ini, conf = self._pagar()
        t = self.p.confirmar(conf)
        self.assertEqual((t["estado"], t["recibo"]), ("aprobado", "REC-000001"))
        self.assertEqual(self.p.estado_cuenta("est001")["total"], 120_000)
        self.assertIn("Gs. 350.000", self.correo.enviados[0]["cuerpo"])
        self.assertTrue(self.p.comprobante_pdf("est001", ini["referencia"]).startswith(b"%PDF"))

    def test_confirmacion_idempotente(self):
        _, conf = self._pagar()
        self.p.confirmar(conf)
        self.p.confirmar(conf)
        self.assertEqual(len(self.correo.enviados), 1)

    def test_firma_invalida_y_monto_alterado_se_rechazan(self):
        _, conf = self._pagar()
        with self.assertRaises(NoAutorizado):
            self.p.confirmar(dict(conf, firma="falsa"))
        with self.assertRaises(NoAutorizado):
            self.p.confirmar(dict(conf, monto=1))  # cambia el contenido firmado

    def test_pago_rechazado_no_genera_comprobante(self):
        ini, conf = self._pagar(aprobado=False)
        self.assertEqual(self.p.confirmar(conf)["estado"], "rechazado")
        with self.assertRaises(DatosInvalidos):
            self.p.comprobante_pdf("est001", ini["referencia"])

    def test_deuda_inexistente(self):
        with self.assertRaises(NoEncontrado):
            self.p.iniciar_pago("est001", "D-9999")

    def test_no_almacena_datos_de_tarjeta(self):
        _, conf = self._pagar()
        t = self.p.confirmar(conf)
        self.assertFalse({"tarjeta", "numero_tarjeta", "cvv", "pan"} & set(t))


class TestAPIPagos(unittest.TestCase):
    def test_flujo_de_pago_por_api(self):
        with ServidorDePrueba() as s:
            t = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            codigo, ini = s.pedir("POST", "/api/pagos", {"id_deuda": "D-1002"}, token=t)
            self.assertEqual(codigo, 200)
            orden = s.pedir("GET", "/api/pagos", token=t)[1][0]["id_orden"]
            conf = s.portal.pasarela.simular_pago(orden)
            codigo, r = s.pedir("POST", "/api/pagos/confirmacion", conf)
            self.assertEqual((codigo, r), (200, {"referencia": ini["referencia"], "estado": "aprobado"}))
            self.assertEqual(s.pedir("GET", f"/api/pagos/{ini['referencia']}/comprobante.pdf", token=t)[0], 200)
            self.assertEqual(s.pedir("GET", "/api/notificaciones", token=t)[1][0]["tipo"], "pago_confirmado")


if __name__ == "__main__":
    unittest.main()
