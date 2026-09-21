"""Perfil del estudiante (F1.02, F1.03) - datos propios del portal (archivo interno F1.08)."""
import re

from .errores import DatosInvalidos, NoEncontrado

_TELEFONO = re.compile(r"^\+?\d{9,13}$")
_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ServicioPerfil:
    def __init__(self, academico, auditoria):
        self._academico = academico
        self._auditoria = auditoria
        self._contactos = {}  # usuario -> {telefono, correo_alternativo}

    def consultar(self, usuario):
        try:
            base = self._academico.estudiante(usuario)
        except KeyError:
            raise NoEncontrado("El usuario no tiene registro académico")
        return dict(base, contacto=dict(self._contactos.get(usuario, {})))

    def actualizar_contacto(self, usuario, telefono=None, correo_alternativo=None):
        if telefono is not None and not _TELEFONO.match(telefono):
            raise DatosInvalidos("Teléfono inválido")
        if correo_alternativo is not None and not _CORREO.match(correo_alternativo):
            raise DatosInvalidos("Correo alternativo inválido")
        contacto = self._contactos.setdefault(usuario, {})
        if telefono is not None:
            contacto["telefono"] = telefono
        if correo_alternativo is not None:
            contacto["correo_alternativo"] = correo_alternativo
        self._auditoria.registrar(usuario, "perfil_actualizado", sorted(contacto))
        return self.consultar(usuario)
