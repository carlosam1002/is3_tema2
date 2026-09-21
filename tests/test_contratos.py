"""Pruebas de contrato de interfaz con los servicios institucionales.

Se ejecutan contra los adaptadores simulados en el pipeline y contra los
adaptadores reales en el ambiente de integracion (misma suite, otro adaptador).
"""
import unittest

from portal.adaptadores.academico import SistemaAcademicoSimulado
from portal.adaptadores.sso import DirectorioSimulado


class ContratoSSO(unittest.TestCase):
    adaptador = DirectorioSimulado

    def test_autenticar_devuelve_campos_acordados(self):
        datos = self.adaptador().autenticar("est001", "clave-est001")
        self.assertEqual(set(datos), {"usuario", "nombre", "rol", "correo"})
        self.assertIn(datos["rol"], {"estudiante", "funcionario"})

    def test_credencial_invalida_devuelve_none(self):
        self.assertIsNone(self.adaptador().autenticar("est001", "incorrecta"))


class ContratoAcademico(unittest.TestCase):
    adaptador = SistemaAcademicoSimulado

    def test_estructura_de_respuestas(self):
        a = self.adaptador()
        self.assertTrue({"matricula", "nombre", "carrera", "correo_institucional"} <= set(a.estudiante("est001")))
        for fila in a.calificaciones("est001"):
            self.assertEqual(set(fila), {"materia", "periodo", "nota"})
        for fila in a.horario("est001"):
            self.assertEqual(set(fila), {"materia", "dia", "desde", "hasta", "aula"})
        self.assertEqual(set(a.historial("est001")), {"aprobadas", "total_malla"})
        self.assertEqual(set(a.inscripcion("est001")), {"periodo", "estado", "materias"})

    def test_usuario_inexistente_lanza_keyerror(self):
        with self.assertRaises(KeyError):
            self.adaptador().estudiante("no-existe")


if __name__ == "__main__":
    unittest.main()
