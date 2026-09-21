"""I1 - Perfil y consultas academicas (regresion permanente)."""
import unittest

from portal.adaptadores.academico import SistemaAcademicoSimulado
from portal.auditoria import RegistroAuditoria
from portal.consultas import ServicioConsultas
from portal.errores import DatosInvalidos, NoEncontrado
from portal.perfil import ServicioPerfil
from tests.utilidades import ServidorDePrueba


class TestPerfil(unittest.TestCase):
    def setUp(self):
        self.aud = RegistroAuditoria()
        self.perfil = ServicioPerfil(SistemaAcademicoSimulado(), self.aud)

    def test_consultar_perfil_combina_datos_academicos(self):
        p = self.perfil.consultar("est001")
        self.assertEqual(p["matricula"], "2023-0001")
        self.assertEqual(p["contacto"], {})

    def test_actualizar_contacto_valido(self):
        p = self.perfil.actualizar_contacto("est001", telefono="+595981000111")
        self.assertEqual(p["contacto"]["telefono"], "+595981000111")
        self.assertEqual(len(self.aud.eventos("est001", "perfil_actualizado")), 1)

    def test_rechaza_datos_invalidos(self):
        with self.assertRaises(DatosInvalidos):
            self.perfil.actualizar_contacto("est001", telefono="abc")
        with self.assertRaises(DatosInvalidos):
            self.perfil.actualizar_contacto("est001", correo_alternativo="sin-arroba")

    def test_funcionario_sin_registro_academico(self):
        with self.assertRaises(NoEncontrado):
            self.perfil.consultar("fun001")


class TestConsultas(unittest.TestCase):
    def setUp(self):
        self.c = ServicioConsultas(SistemaAcademicoSimulado())

    def test_calificaciones_y_horario(self):
        self.assertEqual(len(self.c.calificaciones("est001")), 3)
        self.assertEqual(self.c.horario("est001")[0]["dia"], "lunes")

    def test_historial_calcula_avance(self):
        self.assertEqual(self.c.historial("est001")["avance_porcentaje"], 15.0)
        self.assertEqual(self.c.historial("est002")["avance_porcentaje"], 0.0)

    def test_estado_de_inscripcion(self):
        self.assertEqual(self.c.inscripcion("est001")["estado"], "confirmada")


class TestAPIIncremento1(unittest.TestCase):
    """Flujo de punta a punta de I1 a traves de la API."""

    def test_flujo_login_perfil_consultas(self):
        with ServidorDePrueba() as s:
            codigo, r = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})
            self.assertEqual(codigo, 200)
            t = r["token"]
            self.assertEqual(s.pedir("GET", "/api/perfil", token=t)[1]["nombre"], "Estudiante Uno")
            codigo, p = s.pedir("PUT", "/api/perfil/contacto", {"telefono": "+595981000111"}, token=t)
            self.assertEqual((codigo, p["contacto"]["telefono"]), (200, "+595981000111"))
            for recurso in ("calificaciones", "horario", "historial", "inscripcion"):
                self.assertEqual(s.pedir("GET", f"/api/consultas/{recurso}", token=t)[0], 200, recurso)
            self.assertEqual(s.pedir("GET", "/api/perfil")[0], 401)


if __name__ == "__main__":
    unittest.main()
