"""Adaptador del proveedor de notificaciones por correo (archivo externo F3.10).

Contrato de interfaz:
    enviar(destinatario: str, asunto: str, cuerpo: str) -> str  identificador del envio
    Si el proveedor no esta disponible lanza ConnectionError.
El adaptador es intercambiable (p. ej., por el SMTP institucional) sin cambiar el servicio.
"""


class ProveedorCorreoSimulado:
    def __init__(self):
        self.disponible = True
        self.enviados = []

    def enviar(self, destinatario, asunto, cuerpo):
        if not self.disponible:
            raise ConnectionError("Proveedor de correo no disponible")
        self.enviados.append({"destinatario": destinatario, "asunto": asunto, "cuerpo": cuerpo})
        return f"MSG-{len(self.enviados):06d}"
