"""Prueba de humo de la API: el producto completo arranca y responde."""
import unittest

import portal
from tests.utilidades import ServidorDePrueba


class TestHumoAPI(unittest.TestCase):
    def test_salud_informa_version(self):
        with ServidorDePrueba() as s:
            codigo, datos = s.pedir("GET", "/salud")
        self.assertEqual(codigo, 200)
        self.assertEqual(datos, {"estado": "ok", "version": portal.__version__})

    def test_ruta_inexistente_devuelve_404(self):
        with ServidorDePrueba() as s:
            codigo, _ = s.pedir("GET", "/no-existe")
        self.assertEqual(codigo, 404)


if __name__ == "__main__":
    unittest.main()
