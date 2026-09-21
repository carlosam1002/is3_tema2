"""Solicitudes de tramites y seguimiento (Incremento 2).

Funciones: catalogo (F2.01, F2.10), crear solicitud con adjuntos (F2.02, F2.03, F2.08, F2.09),
consulta y linea de tiempo (F2.04, F2.05), gestion por funcionarios (F2.06, F2.07),
integracion con expedientes (F2.11), comprobante PDF (F2.12) y bandeja con plazos (F2.13).
"""
import itertools
import time

from .errores import DatosInvalidos, NoAutorizado, NoEncontrado
from .pdf import generar_pdf

DIA = 24 * 3600
TIPOS_ADJUNTO = {"pdf", "jpg", "png"}
TAMANO_MAX_ADJUNTO = 5 * 1024 * 1024

TRANSICIONES = {
    "recibida": {"en_revision", "rechazada"},
    "en_revision": {"observada", "resuelta", "rechazada"},
    "observada": {"en_revision"},
    "resuelta": set(),
    "rechazada": set(),
}

CATALOGO = [
    {"codigo": "CONST-AR", "nombre": "Constancia de alumno regular", "plazo_dias": 2, "requiere_adjunto": False},
    {"codigo": "CERT-EST", "nombre": "Certificado de estudios", "plazo_dias": 5, "requiere_adjunto": False},
    {"codigo": "REV-EXA", "nombre": "Revisión de examen", "plazo_dias": 3, "requiere_adjunto": True},
    {"codigo": "HOM-MAT", "nombre": "Homologación de materias", "plazo_dias": 15, "requiere_adjunto": True},
    {"codigo": "CAMB-SEC", "nombre": "Cambio de sección", "plazo_dias": 3, "requiere_adjunto": False},
]


class ServicioSolicitudes:
    def __init__(self, expedientes, auditoria, reloj=time.time, catalogo=None):
        self._expedientes = expedientes
        self._auditoria = auditoria
        self._reloj = reloj
        self._catalogo = {t["codigo"]: dict(t) for t in (catalogo or CATALOGO)}
        self._solicitudes = {}
        self._ids = itertools.count(1)

    # ---- catalogo
    def catalogo(self):
        return list(self._catalogo.values())

    # ---- estudiante
    def crear(self, usuario, tramite, descripcion, adjuntos=()):
        if tramite not in self._catalogo:
            raise NoEncontrado("Trámite inexistente")
        if not descripcion or len(descripcion) > 1000:
            raise DatosInvalidos("La descripción es obligatoria (máximo 1000 caracteres)")
        adjuntos = [self._validar_adjunto(a) for a in adjuntos]
        if self._catalogo[tramite]["requiere_adjunto"] and not adjuntos:
            raise DatosInvalidos("Este trámite requiere al menos un adjunto")
        ahora = self._reloj()
        sid = next(self._ids)
        s = {"id": sid, "usuario": usuario, "tramite": tramite, "descripcion": descripcion,
             "adjuntos": adjuntos, "estado": "recibida", "creada": ahora,
             "vence": ahora + self._catalogo[tramite]["plazo_dias"] * DIA,
             "expediente": None, "linea_tiempo": []}
        self._solicitudes[sid] = s
        self._registrar_evento(s, "recibida", usuario)
        self._registrar_expediente(s)
        self._auditoria.registrar(usuario, "solicitud_creada", sid)
        return self._vista(s)

    def mis_solicitudes(self, usuario):
        return [self._vista(s) for s in self._solicitudes.values() if s["usuario"] == usuario]

    def detalle(self, usuario, sid, rol="estudiante"):
        s = self._obtener(sid)
        if rol != "funcionario" and s["usuario"] != usuario:
            raise NoAutorizado("La solicitud pertenece a otro usuario")
        return self._vista(s)

    def comprobante_pdf(self, usuario, sid):
        s = self.detalle(usuario, sid)
        t = self._catalogo[s["tramite"]]
        return generar_pdf("Comprobante de solicitud", [
            f"Solicitud Nro. {s['id']} - {t['nombre']}",
            f"Expediente: {s['expediente'] or 'pendiente de asignación'}",
            f"Estado actual: {s['estado']}", f"Plazo comprometido: {t['plazo_dias']} días hábiles"])

    # ---- funcionario
    def cambiar_estado(self, funcionario, sid, nuevo, observacion=None):
        s = self._obtener(sid)
        if nuevo not in TRANSICIONES.get(s["estado"], set()):
            raise DatosInvalidos(f"Transición no permitida: {s['estado']} -> {nuevo}")
        if nuevo in ("observada", "rechazada") and not observacion:
            raise DatosInvalidos("Debe registrar una observación")
        s["estado"] = nuevo
        self._registrar_evento(s, nuevo, funcionario, observacion)
        self._auditoria.registrar(funcionario, "solicitud_estado", (sid, nuevo))
        return self._vista(s)

    def bandeja(self):
        """Pendientes ordenadas por vencimiento, con control de plazos (SLA)."""
        ahora = self._reloj()
        pendientes = [s for s in self._solicitudes.values() if TRANSICIONES[s["estado"]]]
        return [dict(self._vista(s), dias_restantes=round((s["vence"] - ahora) / DIA, 1),
                     vencida=s["vence"] < ahora)
                for s in sorted(pendientes, key=lambda s: s["vence"])]

    def reintentar_expedientes(self):
        """Contingencia: asigna expediente a solicitudes registradas durante una caida."""
        for s in self._solicitudes.values():
            if s["expediente"] is None:
                self._registrar_expediente(s)

    # ---- internos
    def _validar_adjunto(self, a):
        nombre, tamano = a.get("nombre", ""), int(a.get("tamano", 0))
        extension = nombre.rsplit(".", 1)[-1].lower() if "." in nombre else ""
        if extension not in TIPOS_ADJUNTO:
            raise DatosInvalidos(f"Tipo de adjunto no permitido: {nombre}")
        if not 0 < tamano <= TAMANO_MAX_ADJUNTO:
            raise DatosInvalidos(f"Tamaño de adjunto inválido: {nombre}")
        return {"nombre": nombre, "tamano": tamano}

    def _registrar_expediente(self, s):
        try:
            s["expediente"] = self._expedientes.registrar(s["tramite"], s["usuario"], s["descripcion"][:80])
        except ConnectionError:
            s["expediente"] = None  # se reintenta luego; la solicitud no se pierde

    def _registrar_evento(self, s, estado, por, observacion=None):
        s["linea_tiempo"].append({"momento": self._reloj(), "estado": estado, "por": por, "observacion": observacion})

    def _obtener(self, sid):
        try:
            return self._solicitudes[int(sid)]
        except (KeyError, ValueError):
            raise NoEncontrado("Solicitud inexistente")

    @staticmethod
    def _vista(s):
        return {k: (list(v) if isinstance(v, list) else v) for k, v in s.items()}
