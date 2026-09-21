"""Errores de dominio. Cada error conoce el codigo HTTP con el que se expone."""


class ErrorPortal(Exception):
    codigo_http = 400


class NoAutenticado(ErrorPortal):
    codigo_http = 401


class NoAutorizado(ErrorPortal):
    codigo_http = 403


class NoEncontrado(ErrorPortal):
    codigo_http = 404


class DatosInvalidos(ErrorPortal):
    codigo_http = 422


class ServicioExternoNoDisponible(ErrorPortal):
    codigo_http = 503
