"""I3 - Reportes de tramites y recaudacion."""
import unittest

from portal.app import Portal
from tests.utilidades import ServidorDePrueba


class TestReportes(unittest.TestCase):
    def test_reporte_de_tramites(self):
        p = Portal()
        a = p.solicitudes.crear("est001", "CONST-AR", "x")["id"]
        p.solicitudes.crear("est002", "CAMB-SEC", "y")
        p.solicitudes.cambiar_estado("fun001", a, "en_revision")
        p.solicitudes.cambiar_estado("fun001", a, "resuelta")
        r = p.reportes.tramites()
        self.assertEqual(r["total"], 2)
        self.assertEqual(r["por_estado"], {"recibida": 1, "resuelta": 1})
        self.assertIn("CONST-AR", r["dias_promedio_resolucion"])

    def test_reporte_de_recaudacion_cuadra_con_pagos_aprobados(self):
        p = Portal()
        for usuario, deuda, aprobado in (("est001", "D-1001", True), ("est002", "D-2001", True), ("est001", "D-1002", False)):
            p.pagos.iniciar_pago(usuario, deuda)
            orden = p.pagos.historial(usuario)[-1]["id_orden"]
            p.pagos.confirmar(p.pasarela.simular_pago(orden, aprobado))
        r = p.reportes.recaudacion()
        self.assertEqual((r["cantidad_pagos"], r["total"]), (2, 700_000))

    def test_reportes_restringidos_a_funcionarios(self):
        with ServidorDePrueba() as s:
            te = s.pedir("POST", "/api/sesion", {"usuario": "est001", "clave": "clave-est001"})[1]["token"]
            tf = s.pedir("POST", "/api/sesion", {"usuario": "fun001", "clave": "clave-fun001"})[1]["token"]
            self.assertEqual(s.pedir("GET", "/api/reportes/recaudacion", token=te)[0], 403)
            self.assertEqual(s.pedir("GET", "/api/reportes/tramites", token=tf)[0], 200)


if __name__ == "__main__":
    unittest.main()
