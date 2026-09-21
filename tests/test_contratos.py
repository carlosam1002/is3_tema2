"""Pruebas de contrato de interfaz con los servicios institucionales.

Se ejecutan contra los adaptadores simulados en el pipeline y contra los
adaptadores reales en el ambiente de integracion (misma suite, otro adaptador).
"""
import unittest

from portal.adaptadores.academico import SistemaAcademicoSimulado
from portal.adaptadores.arancelario import SistemaArancelarioSimulado
from portal.adaptadores.expedientes import ExpedientesSimulado
from portal.adaptadores.pasarela import PasarelaSimulada
from portal.adaptadores.proveedor_correo import ProveedorCorreoSimulado
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


class ContratoExpedientes(unittest.TestCase):
    adaptador = ExpedientesSimulado

    def test_numero_con_formato_acordado(self):
        numero = self.adaptador().registrar("CONST-AR", "est001", "resumen")
        self.assertRegex(numero, r"^EXP-\d{4}-\d{6}$")

    def test_no_disponible_lanza_connectionerror(self):
        a = self.adaptador()
        a.disponible = False
        with self.assertRaises(ConnectionError):
            a.registrar("CONST-AR", "est001", "resumen")


class ContratoPasarela(unittest.TestCase):
    adaptador = PasarelaSimulada

    def test_orden_y_confirmacion_firmada(self):
        a = self.adaptador()
        orden = a.crear_orden("PAG-000001", 350_000)
        self.assertEqual(set(orden), {"id_orden", "url_pago"})
        conf = a.simular_pago(orden["id_orden"])
        self.assertEqual(set(conf), {"id_orden", "referencia", "monto", "estado", "firma"})
        self.assertTrue(a.verificar(conf))
        self.assertFalse(a.verificar(dict(conf, estado="rechazado")))


class ContratoArancelario(unittest.TestCase):
    adaptador = SistemaArancelarioSimulado

    def test_deudas_y_registro_de_pago(self):
        a = self.adaptador()
        deuda = a.deudas("est001")[0]
        self.assertEqual(set(deuda), {"id", "concepto", "monto", "vencimiento"})
        with self.assertRaises(ValueError):
            a.registrar_pago(deuda["id"], "PAG-1", deuda["monto"] - 1)
        self.assertRegex(a.registrar_pago(deuda["id"], "PAG-1", deuda["monto"]), r"^REC-\d{6}$")


class ContratoProveedorCorreo(unittest.TestCase):
    adaptador = ProveedorCorreoSimulado

    def test_envio_y_error_de_disponibilidad(self):
        a = self.adaptador()
        self.assertTrue(a.enviar("x@ejemplo.edu.py", "asunto", "cuerpo"))
        a.disponible = False
        with self.assertRaises(ConnectionError):
            a.enviar("x@ejemplo.edu.py", "asunto", "cuerpo")


if __name__ == "__main__":
    unittest.main()
