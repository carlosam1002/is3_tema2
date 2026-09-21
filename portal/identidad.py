"""Autenticacion con el SSO institucional y manejo de sesiones (F1.01)."""
import secrets
import time

from .errores import NoAutenticado, NoAutorizado


class ServicioIdentidad:
    DURACION_SESION = 30 * 60  # segundos

    def __init__(self, directorio, auditoria, reloj=time.time):
        self._directorio = directorio
        self._auditoria = auditoria
        self._reloj = reloj
        self._sesiones = {}

    def iniciar_sesion(self, usuario, clave):
        datos = self._directorio.autenticar(usuario, clave)
        if not datos:
            self._auditoria.registrar(usuario, "login_fallido")
            raise NoAutenticado("Credenciales inválidas")
        token = secrets.token_urlsafe(24)
        self._sesiones[token] = dict(datos, expira=self._reloj() + self.DURACION_SESION)
        self._auditoria.registrar(usuario, "login")
        return token

    def usuario(self, token):
        sesion = self._sesiones.get(token or "")
        if not sesion or sesion["expira"] < self._reloj():
            self._sesiones.pop(token or "", None)
            raise NoAutenticado("Sesión inexistente o expirada")
        return {k: v for k, v in sesion.items() if k != "expira"}

    def exigir_rol(self, token, rol):
        datos = self.usuario(token)
        if datos["rol"] != rol:
            raise NoAutorizado(f"Operación reservada al rol '{rol}'")
        return datos

    def cerrar_sesion(self, token):
        datos = self.usuario(token)
        del self._sesiones[token]
        self._auditoria.registrar(datos["usuario"], "logout")
