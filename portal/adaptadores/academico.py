"""Adaptador del sistema academico institucional (archivo externo F1.10, solo lectura).

Contrato de interfaz (acordado con la Direccion Academica y la Direccion TIC):
    estudiante(usuario) -> dict {matricula, nombre, carrera, correo_institucional}
    calificaciones(usuario) -> list[dict {materia, periodo, nota}]
    horario(usuario) -> list[dict {materia, dia, desde, hasta, aula}]
    historial(usuario) -> dict {aprobadas: list[str], total_malla: int}
    inscripcion(usuario) -> dict {periodo, estado, materias: list[str]}
Si el usuario no existe se lanza KeyError.
"""


class SistemaAcademicoSimulado:
    def __init__(self):
        self._datos = {
            "est001": {
                "estudiante": {"matricula": "2023-0001", "nombre": "Estudiante Uno",
                               "carrera": "Licenciatura en Ciencias Informáticas",
                               "correo_institucional": "est001@alumnos.ejemplo.edu.py"},
                "calificaciones": [
                    {"materia": "Ingeniería de Software II", "periodo": "2026-1", "nota": 4},
                    {"materia": "Base de Datos II", "periodo": "2026-1", "nota": 5},
                    {"materia": "Redes de Computadoras", "periodo": "2026-1", "nota": 3},
                ],
                "horario": [
                    {"materia": "Ingeniería de Software III", "dia": "lunes", "desde": "18:00", "hasta": "20:15", "aula": "A-12"},
                    {"materia": "Sistemas Distribuidos", "dia": "miércoles", "desde": "18:00", "hasta": "20:15", "aula": "B-03"},
                ],
                "historial": {"aprobadas": ["Algoritmos I", "Algoritmos II", "Base de Datos I", "Base de Datos II",
                                            "Ingeniería de Software I", "Ingeniería de Software II"],
                              "total_malla": 40},
                "inscripcion": {"periodo": "2026-2", "estado": "confirmada",
                                "materias": ["Ingeniería de Software III", "Sistemas Distribuidos"]},
            },
            "est002": {
                "estudiante": {"matricula": "2024-0002", "nombre": "Estudiante Dos",
                               "carrera": "Licenciatura en Ciencias Informáticas",
                               "correo_institucional": "est002@alumnos.ejemplo.edu.py"},
                "calificaciones": [],
                "horario": [],
                "historial": {"aprobadas": [], "total_malla": 40},
                "inscripcion": {"periodo": "2026-2", "estado": "pendiente", "materias": []},
            },
        }

    def _de(self, usuario, clave):
        return self._datos[usuario][clave]

    def estudiante(self, usuario):
        return dict(self._de(usuario, "estudiante"))

    def calificaciones(self, usuario):
        return list(self._de(usuario, "calificaciones"))

    def horario(self, usuario):
        return list(self._de(usuario, "horario"))

    def historial(self, usuario):
        return dict(self._de(usuario, "historial"))

    def inscripcion(self, usuario):
        return dict(self._de(usuario, "inscripcion"))
