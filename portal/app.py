"""Fachada del portal y API HTTP (solo biblioteca estandar).

Ejecutar:  python -m portal.app  (escucha en http://127.0.0.1:8080)
"""
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import __version__
from .adaptadores.academico import SistemaAcademicoSimulado
from .adaptadores.arancelario import SistemaArancelarioSimulado
from .adaptadores.expedientes import ExpedientesSimulado
from .adaptadores.pasarela import PasarelaSimulada
from .adaptadores.proveedor_correo import ProveedorCorreoSimulado
from .adaptadores.sso import DirectorioSimulado
from .auditoria import RegistroAuditoria
from .consultas import ServicioConsultas
from .errores import ErrorPortal
from .identidad import ServicioIdentidad
from .notificaciones import ServicioNotificaciones
from .pagos import ServicioPagos
from .perfil import ServicioPerfil
from .solicitudes import ServicioSolicitudes


class Portal:
    """Punto unico de composicion: aqui se conectan servicios y adaptadores."""

    def __init__(self, directorio=None, academico=None, expedientes=None, correo=None,
                 pasarela=None, arancelario=None):
        self.version = __version__
        self.auditoria = RegistroAuditoria()
        self.identidad = ServicioIdentidad(directorio or DirectorioSimulado(), self.auditoria)
        academico = academico or SistemaAcademicoSimulado()
        self.perfil = ServicioPerfil(academico, self.auditoria)
        self.consultas = ServicioConsultas(academico)
        self.expedientes = expedientes or ExpedientesSimulado()
        self.solicitudes = ServicioSolicitudes(self.expedientes, self.auditoria)
        # I3 - notificaciones (servicio comun para solicitudes y pagos, decision DEC-09)
        self.correo = correo or ProveedorCorreoSimulado()
        self.notificaciones = ServicioNotificaciones(
            self.correo, lambda usuario: academico.estudiante(usuario)["correo_institucional"])
        self.solicitudes.suscribir(self._notificar_cambio_de_estado)
        # I3 - pagos
        self.pasarela = pasarela or PasarelaSimulada()
        self.pagos = ServicioPagos(self.pasarela, arancelario or SistemaArancelarioSimulado(),
                                   self.notificaciones, self.auditoria)

    def _notificar_cambio_de_estado(self, solicitud, estado):
        if solicitud["usuario"] == solicitud["linea_tiempo"][-1]["por"]:
            return  # el propio estudiante hizo el cambio (p. ej., cancelacion)
        self.notificaciones.notificar(
            solicitud["usuario"], "solicitud_estado", f"Solicitud {solicitud['id']}: {estado.replace('_', ' ')}",
            f"Tu solicitud ({solicitud['tramite']}, expediente {solicitud['expediente']}) cambió a '{estado}'.")

    def salud(self):
        return {"estado": "ok", "version": self.version}


def _campos(c, *nombres):
    return {k: c["json"][k] for k in nombres if k in c["json"]}


def _publico(transaccion):
    """Respuesta minima al callback publico de la pasarela (no expone datos del estudiante)."""
    return {"referencia": transaccion["referencia"], "estado": transaccion["estado"]}


def construir_rutas(p):
    """Tabla de rutas: (metodo, patron, funcion(ctx) -> respuesta)."""
    idn = p.identidad

    def u(c):  # usuario autenticado
        return idn.usuario(c["token"])["usuario"]

    def f(c):  # funcionario autenticado
        return idn.exigir_rol(c["token"], "funcionario")["usuario"]

    return [
        ("GET", r"/salud", lambda c: p.salud()),
        # I1 - identidad
        ("POST", r"/api/sesion", lambda c: {"token": idn.iniciar_sesion(c["json"].get("usuario"), c["json"].get("clave"))}),
        ("GET", r"/api/sesion", lambda c: idn.usuario(c["token"])),
        ("POST", r"/api/sesion/cerrar", lambda c: idn.cerrar_sesion(c["token"]) or {"cerrada": True}),
        # I1 - perfil y consultas
        ("GET", r"/api/perfil", lambda c: p.perfil.consultar(u(c))),
        ("PUT", r"/api/perfil/contacto", lambda c: p.perfil.actualizar_contacto(u(c), **_campos(c, "telefono", "correo_alternativo"))),
        ("GET", r"/api/consultas/(?P<recurso>calificaciones|horario|historial|inscripcion)",
         lambda c: getattr(p.consultas, c["params"]["recurso"])(u(c))),
        # I2 - alcance movido desde I1 (RCA-01)
        ("PUT", r"/api/perfil/preferencias", lambda c: p.perfil.actualizar_preferencias(u(c), **_campos(c, "idioma", "vista_inicio"))),
        ("GET", r"/api/consultas/historial.pdf", lambda c: p.consultas.historial_pdf(u(c))),
        # I2 - solicitudes y seguimiento
        ("GET", r"/api/tramites", lambda c: p.solicitudes.catalogo()),
        ("POST", r"/api/solicitudes", lambda c: p.solicitudes.crear(
            u(c), c["json"].get("tramite"), c["json"].get("descripcion"), c["json"].get("adjuntos", []))),
        ("GET", r"/api/solicitudes", lambda c: p.solicitudes.mis_solicitudes(u(c))),
        ("GET", r"/api/solicitudes/(?P<id>\d+)", lambda c: p.solicitudes.detalle(
            u(c), c["params"]["id"], idn.usuario(c["token"])["rol"])),
        ("GET", r"/api/solicitudes/(?P<id>\d+)/comprobante.pdf", lambda c: p.solicitudes.comprobante_pdf(u(c), c["params"]["id"])),
        ("POST", r"/api/solicitudes/(?P<id>\d+)/estado", lambda c: p.solicitudes.cambiar_estado(
            f(c), c["params"]["id"], c["json"].get("estado"), c["json"].get("observacion"))),
        ("GET", r"/api/bandeja", lambda c: f(c) and p.solicitudes.bandeja()),
        ("POST", r"/api/solicitudes/(?P<id>\d+)/cancelar", lambda c: p.solicitudes.cancelar(u(c), c["params"]["id"])),
        # I3 - notificaciones
        ("GET", r"/api/notificaciones", lambda c: p.notificaciones.bandeja(u(c))),
        ("PUT", r"/api/notificaciones/preferencias", lambda c: p.notificaciones.actualizar_preferencias(
            u(c), **_campos(c, "correo", "tipos"))),
        # I3 - pagos
        ("GET", r"/api/pagos/estado-cuenta", lambda c: p.pagos.estado_cuenta(u(c))),
        ("POST", r"/api/pagos", lambda c: p.pagos.iniciar_pago(u(c), c["json"].get("id_deuda"))),
        ("POST", r"/api/pagos/confirmacion", lambda c: _publico(p.pagos.confirmar(c["json"]))),
        ("GET", r"/api/pagos", lambda c: p.pagos.historial(u(c))),
        ("GET", r"/api/pagos/(?P<ref>PAG-\d+)/comprobante.pdf", lambda c: p.pagos.comprobante_pdf(u(c), c["params"]["ref"])),
        ("POST", r"/api/notificaciones/(?P<id>\d+)/leida", lambda c: p.notificaciones.marcar_leida(u(c), c["params"]["id"])),
    ]


def crear_servidor(portal=None, host="127.0.0.1", puerto=8080):
    portal = portal or Portal()
    rutas = [(m, re.compile(f"^{patron}$"), fn) for m, patron, fn in construir_rutas(portal)]

    class Manejador(BaseHTTPRequestHandler):
        def _despachar(self, metodo):
            for m, patron, fn in rutas:
                coincide = patron.match(self.path.split("?")[0])
                if m == metodo and coincide:
                    largo = int(self.headers.get("Content-Length") or 0)
                    cuerpo = json.loads(self.rfile.read(largo) or b"{}") if largo else {}
                    auth = self.headers.get("Authorization", "")
                    ctx = {"params": coincide.groupdict(), "json": cuerpo,
                           "token": auth[7:] if auth.startswith("Bearer ") else None}
                    try:
                        return self._responder(200, fn(ctx))
                    except ErrorPortal as e:
                        return self._responder(e.codigo_http, {"error": str(e)})
            return self._responder(404, {"error": "ruta no encontrada"})

        def _responder(self, codigo, datos):
            if isinstance(datos, (bytes, bytearray)):
                cuerpo, tipo = bytes(datos), "application/pdf"
            else:
                cuerpo, tipo = json.dumps(datos, ensure_ascii=False).encode(), "application/json; charset=utf-8"
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def do_GET(self):
            self._despachar("GET")

        def do_POST(self):
            self._despachar("POST")

        def do_PUT(self):
            self._despachar("PUT")

        def log_message(self, *args):
            pass

    return ThreadingHTTPServer((host, puerto), Manejador)


if __name__ == "__main__":
    srv = crear_servidor()
    print(f"Portal {__version__} en http://{srv.server_address[0]}:{srv.server_address[1]}")
    srv.serve_forever()
