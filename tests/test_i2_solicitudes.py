"""I2 - Solicitudes de tramites y seguimiento (regresion permanente desde v1.1.0)."""
import unittest

from portal.adaptadores.expedientes import ExpedientesSimulado
from portal.auditoria import RegistroAuditoria
from portal.errores import DatosInvalidos, NoAutorizado, NoEncontrado
from portal.solicitudes import DIA, ServicioSolicitudes
from tests.utilidades import ServidorDePrueba

PDF_OK = {"nombre": "examen.pdf", "tamano": 120_000}


class Reloj:
    def __init__(self):
        self.t = 1_000_000.0

    def __call__(self):
        return self.t


class TestSolicitudes(unittest.TestCase):
    def setUp(self):
        self.reloj = Reloj()
        self.exp = ExpedientesSimulado()
        self.s = ServicioSolicitudes(self.exp, RegistroAuditoria(), self.reloj)

    def test_catalogo_tiene_al_menos_cinco_tramites(self):
        self.assertGreaterEqual(len(self.s.catalogo()), 5)

    def test_crear_asigna_expediente_y_linea_de_tiempo(self):
        sol = self.s.crear("est001", "CONST-AR", "Para presentar en el trabajo")
        self.assertEqual(sol["expediente"], "EXP-2026-000001")
        self.assertEqual(sol["estado"], "recibida")
        self.assertEqual(len(sol["linea_tiempo"]), 1)

    def test_validaciones_de_adjuntos(self):
        with self.assertRaises(DatosInvalidos):
            self.s.crear("est001", "REV-EXA", "Revisión del parcial")  # requiere adjunto
        with self.assertRaises(DatosInvalidos):
            self.s.crear("est001", "REV-EXA", "x", [{"nombre": "virus.exe", "tamano": 10}])
        with self.assertRaises(DatosInvalidos):
            self.s.crear("est001", "REV-EXA", "x", [{"nombre": "grande.pdf", "tamano": 6 * 1024 * 1024}])
        self.assertEqual(len(self.s.crear("est001", "REV-EXA", "x", [PDF_OK])["adjuntos"]), 1)

    def test_tramite_inexistente(self):
        with self.assertRaises(NoEncontrado):
            self.s.crear("est001", "NO-EXISTE", "x")

    def test_estudiante_no_ve_solicitudes_ajenas(self):
        sol = self.s.crear("est001", "CONST-AR", "x")
        with self.assertRaises(NoAutorizado):
            self.s.detalle("est002", sol["id"])
        self.assertEqual(self.s.detalle("fun001", sol["id"], rol="funcionario")["id"], sol["id"])

    def test_flujo_de_estados_y_observaciones(self):
        sid = self.s.crear("est001", "CERT-EST", "x")["id"]
        self.s.cambiar_estado("fun001", sid, "en_revision")
        with self.assertRaises(DatosInvalidos):
            self.s.cambiar_estado("fun001", sid, "observada")  # sin observacion
        self.s.cambiar_estado("fun001", sid, "observada", "Falta foto carnet")
        self.s.cambiar_estado("fun001", sid, "en_revision")
        final = self.s.cambiar_estado("fun001", sid, "resuelta")
        self.assertEqual([e["estado"] for e in final["linea_tiempo"]],
                         ["recibida", "en_revision", "observada", "en_revision", "resuelta"])
        with self.assertRaises(DatosInvalidos):
            self.s.cambiar_estado("fun001", sid, "en_revision")  # estado final

    def test_bandeja_ordena_por_vencimiento_y_marca_vencidas(self):
        a = self.s.crear("est001", "HOM-MAT", "x", [PDF_OK])["id"]  # 15 dias
        b = self.s.crear("est001", "CONST-AR", "x")["id"]  # 2 dias
        self.reloj.t += 3 * DIA
        bandeja = self.s.bandeja()
        self.assertEqual([x["id"] for x in bandeja], [b, a])
        self.assertTrue(bandeja[0]["vencida"])
        self.assertFalse(bandeja[1]["vencida"])

    def test_contingencia_expedientes_no_disponible(self):
        self.exp.disponible = False
        sid = self.s.crear("est001", "CONST-AR", "x")["id"]
        self.assertIsNone(self.s.detalle("est001", sid)["expediente"])
        self.exp.disponible = True
        self.s.reintentar_expedientes()
        self.assertIsNotNone(self.s.detalle("est001", sid)["expediente"])

    def test_comprobante_pdf(self):
        sid = self.s.crear("est001", "CONST-AR", "x")["id"]
        self.assertTrue(self.s.comprobante_pdf("est001", sid).startswith(b"%PDF"))


class TestAPIIncremento2(unittest.TestCase):
    def test_flujo_estudiante_funcionario(self):
        with ServidorDePrueba() as s:
            te = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            tf = s.pedir("POST", "/api/sesion", {"usuario": "fun001", "clave": "clave-fun001"})[1]["token"]
            codigo, sol = s.pedir("POST", "/api/solicitudes", {"tramite": "CONST-AR", "descripcion": "Trabajo"}, token=te)
            self.assertEqual(codigo, 200)
            self.assertEqual(s.pedir("GET", "/api/bandeja", token=te)[0], 403)
            self.assertEqual(len(s.pedir("GET", "/api/bandeja", token=tf)[1]), 1)
            codigo, _ = s.pedir("POST", f"/api/solicitudes/{sol['id']}/estado", {"estado": "en_revision"}, token=tf)
            self.assertEqual(codigo, 200)
            self.assertEqual(s.pedir("GET", f"/api/solicitudes/{sol['id']}", token=te)[1]["estado"], "en_revision")
            self.assertEqual(s.pedir("GET", f"/api/solicitudes/{sol['id']}/comprobante.pdf", token=te)[0], 200)


if __name__ == "__main__":
    unittest.main()
