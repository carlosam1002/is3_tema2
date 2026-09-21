"""Utilidades de prueba: levanta el servidor HTTP en un puerto libre."""
import json
import threading
import urllib.error
import urllib.request

from portal.app import Portal, crear_servidor


class ServidorDePrueba:
    def __init__(self, portal=None):
        self.portal = portal or Portal()
        self.srv = crear_servidor(self.portal, puerto=0)
        self.base = f"http://127.0.0.1:{self.srv.server_address[1]}"
        self.hilo = threading.Thread(target=self.srv.serve_forever, daemon=True)

    def __enter__(self):
        self.hilo.start()
        return self

    def __exit__(self, *exc):
        self.srv.shutdown()
        self.srv.server_close()

    def pedir(self, metodo, ruta, datos=None, token=None):
        cuerpo = json.dumps(datos).encode() if datos is not None else None
        req = urllib.request.Request(self.base + ruta, data=cuerpo, method=metodo)
        req.add_header("Content-Type", "application/json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                crudo = r.read()
                es_json = r.headers.get("Content-Type", "").startswith("application/json")
                return r.status, (json.loads(crudo) if es_json else crudo)
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())
