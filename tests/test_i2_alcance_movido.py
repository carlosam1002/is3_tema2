"""I2 - Alcance movido desde I1 por RCA-01: preferencias (F1.12) e historial en PDF (F1.13)."""
import unittest

from portal.adaptadores.academico import SistemaAcademicoSimulado
from portal.auditoria import RegistroAuditoria
from portal.consultas import ServicioConsultas
from portal.errores import DatosInvalidos
from portal.perfil import ServicioPerfil
from tests.utilidades import ServidorDePrueba


class TestPreferencias(unittest.TestCase):
    def setUp(self):
        self.perfil = ServicioPerfil(SistemaAcademicoSimulado(), RegistroAuditoria())

    def test_valores_por_defecto_y_actualizacion(self):
        self.assertEqual(self.perfil.preferencias("est001")["idioma"], "es")
        self.assertEqual(self.perfil.actualizar_preferencias("est001", idioma="gn")["idioma"], "gn")
        self.assertEqual(self.perfil.consultar("est001")["preferencias"]["idioma"], "gn")

    def test_rechaza_preferencia_invalida(self):
        with self.assertRaises(DatosInvalidos):
            self.perfil.actualizar_preferencias("est001", idioma="fr")


class TestHistorialPDF(unittest.TestCase):
    def test_genera_pdf_valido(self):
        pdf = ServicioConsultas(SistemaAcademicoSimulado()).historial_pdf("est001")
        self.assertTrue(pdf.startswith(b"%PDF-1.4"))
        self.assertTrue(pdf.rstrip().endswith(b"%%EOF"))

    def test_descarga_por_api(self):
        with ServidorDePrueba() as s:
            t = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            codigo, cuerpo = s.pedir("GET", "/api/consultas/historial.pdf", token=t)
        self.assertEqual(codigo, 200)
        self.assertTrue(cuerpo.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
