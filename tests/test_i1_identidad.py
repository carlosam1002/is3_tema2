"""I1 - Autenticacion SSO y auditoria de accesos (regresion permanente)."""
import unittest

from portal.adaptadores.sso import DirectorioSimulado
from portal.auditoria import RegistroAuditoria
from portal.errores import NoAutenticado, NoAutorizado
from portal.identidad import ServicioIdentidad


class Reloj:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


class TestIdentidad(unittest.TestCase):
    def setUp(self):
        self.reloj = Reloj()
        self.aud = RegistroAuditoria(self.reloj)
        self.idn = ServicioIdentidad(DirectorioSimulado(), self.aud, self.reloj)

    def test_login_correcto_devuelve_token_y_audita(self):
        token = self.idn.iniciar_sesion("est001", "clave-est001")
        self.assertEqual(self.idn.usuario(token)["rol"], "estudiante")
        self.assertEqual(len(self.aud.eventos("est001", "login")), 1)

    def test_login_incorrecto_rechaza_y_audita(self):
        with self.assertRaises(NoAutenticado):
            self.idn.iniciar_sesion("est001", "mala")
        self.assertEqual(len(self.aud.eventos("est001", "login_fallido")), 1)

    def test_sesion_expira(self):
        token = self.idn.iniciar_sesion("est001", "clave-est001")
        self.reloj.t += ServicioIdentidad.DURACION_SESION + 1
        with self.assertRaises(NoAutenticado):
            self.idn.usuario(token)

    def test_logout_invalida_token(self):
        token = self.idn.iniciar_sesion("est001", "clave-est001")
        self.idn.cerrar_sesion(token)
        with self.assertRaises(NoAutenticado):
            self.idn.usuario(token)

    def test_control_de_rol(self):
        token = self.idn.iniciar_sesion("est001", "clave-est001")
        with self.assertRaises(NoAutorizado):
            self.idn.exigir_rol(token, "funcionario")


if __name__ == "__main__":
    unittest.main()
