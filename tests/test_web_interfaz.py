"""Capa de presentacion: pagina del portal y rutas que la interfaz necesita.

Se agrego despues de la etiqueta v1.2.1, junto con la interfaz web. No cubre logica
de negocio nueva: verifica que la pagina se sirva, que las preferencias se puedan leer
y que los documentos PDF sigan exigiendo sesion.
"""
import unittest

from tests.utilidades import ServidorDePrueba


class TestInterfazWeb(unittest.TestCase):
    def test_la_raiz_sirve_la_pagina_del_portal(self):
        with ServidorDePrueba() as s:
            codigo, cuerpo = s.pedir("GET", "/")
            self.assertEqual(codigo, 200)
            self.assertIn("Portal de Servicios Estudiantiles", cuerpo.decode("utf-8"))

    def test_preferencias_de_notificacion_se_leen_y_se_guardan(self):
        with ServidorDePrueba() as s:
            t = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            self.assertEqual(s.pedir("GET", "/api/notificaciones/preferencias", token=t)[1]["correo"], True)
            s.pedir("PUT", "/api/notificaciones/preferencias", {"correo": False, "tipos": ["pago_confirmado"]}, token=t)
            pref = s.pedir("GET", "/api/notificaciones/preferencias", token=t)[1]
            self.assertEqual((pref["correo"], pref["tipos"]), (False, ["pago_confirmado"]))

    def test_los_documentos_pdf_exigen_sesion(self):
        with ServidorDePrueba() as s:
            self.assertEqual(s.pedir("GET", "/api/consultas/historial.pdf")[0], 401)

    def test_la_simulacion_de_la_pasarela_cierra_el_pago(self):
        with ServidorDePrueba() as s:
            t = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            ini = s.pedir("POST", "/api/pagos", {"id_deuda": "D-1002"}, token=t)[1]
            codigo, r = s.pedir("POST", "/api/simulacion/pasarela", {"referencia": ini["referencia"]}, token=t)
            self.assertEqual((codigo, r["estado"]), (200, "aprobado"))


if __name__ == "__main__":
    unittest.main()
