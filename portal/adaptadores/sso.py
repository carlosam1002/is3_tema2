"""Adaptador del directorio institucional / SSO (archivo externo F1.11).

Contrato de interfaz (acordado con la Direccion TIC):
    autenticar(usuario: str, clave: str) -> dict | None
    El dict contiene: usuario, nombre, rol ('estudiante' | 'funcionario'), correo.
"""
import hashlib
import hmac


def _hash(clave):
    return hashlib.sha256(clave.encode()).hexdigest()


class DirectorioSimulado:
    def __init__(self):
        self._cuentas = {
            "est001": {"clave": _hash("clave-est001"), "nombre": "Estudiante Uno", "rol": "estudiante",
                       "correo": "est001@alumnos.ejemplo.edu.py"},
            "est002": {"clave": _hash("clave-est002"), "nombre": "Estudiante Dos", "rol": "estudiante",
                       "correo": "est002@alumnos.ejemplo.edu.py"},
            "fun001": {"clave": _hash("clave-fun001"), "nombre": "Funcionario Uno", "rol": "funcionario",
                       "correo": "fun001@ejemplo.edu.py"},
        }

    def autenticar(self, usuario, clave):
        cuenta = self._cuentas.get(usuario)
        if not cuenta or not hmac.compare_digest(cuenta["clave"], _hash(clave or "")):
            return None
        return {"usuario": usuario, "nombre": cuenta["nombre"], "rol": cuenta["rol"], "correo": cuenta["correo"]}
