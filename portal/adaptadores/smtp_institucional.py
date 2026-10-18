"""Adaptador alternativo de notificaciones: servidor de correo institucional.

Respeta el mismo contrato de interfaz que el proveedor externo (F3.10):
    enviar(destinatario, asunto, cuerpo) -> str   identificador del envio
    ConnectionError cuando el servidor no esta disponible.

Se incorpora como respuesta al evento de cambio registrado antes de I2: el
proveedor externo informo que su API no estaria disponible por cuatro semanas
(riesgo R-12). El servicio de notificaciones no cambia: solo se le inyecta otro
adaptador, lo que mantiene compatible la API publica del portal.

En el prototipo el envio se simula; en produccion este adaptador usa smtplib
contra el servidor institucional, con el limite de envios por hora acordado con
la Direccion TIC.
"""


class CorreoInstitucionalSimulado:
    LIMITE_POR_HORA = 200

    def __init__(self, servidor="smtp.ejemplo.edu.py", remitente="no-responder@ejemplo.edu.py"):
        self.servidor = servidor
        self.remitente = remitente
        self.disponible = True
        self.enviados = []

    def enviar(self, destinatario, asunto, cuerpo):
        if not self.disponible:
            raise ConnectionError("Servidor de correo institucional no disponible")
        if len(self.enviados) >= self.LIMITE_POR_HORA:
            raise ConnectionError("Límite de envíos por hora alcanzado; el envío queda pendiente")
        self.enviados.append({"destinatario": destinatario, "asunto": asunto, "cuerpo": cuerpo,
                              "remitente": self.remitente})
        return f"SMTP-{len(self.enviados):06d}"
