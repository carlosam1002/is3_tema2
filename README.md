# Portal de Servicios Estudiantiles

Prototipo verificable del **TP 2 — Enfoque Incremental** (Ingeniería de Software III, LCIK).
El repositorio materializa el plan de releases del informe: cada incremento es una
versión desplegable, etiquetada y probada junto con todo lo entregado antes.

## Plan de releases

| Release | Incremento | Capacidad nueva | Estado |
|---|---|---|---|
| `v1.0.0` | I1 | Autenticación SSO, perfil y consultas académicas | Liberado |
| `v1.1.0` | I2 | Solicitudes de trámites y seguimiento | Liberado |
| `v1.2.0` | I3 | Pagos, notificaciones y reportes | Liberado |
| `v1.2.1` | I3 | Notificaciones por el correo institucional (evento de cambio, R-12) | Liberado |
| `v1.3.0` | — | Reporte de uso del portal y bandeja de notificaciones (RCA-03 y RCA-04) | Planificado |

Detalle de componentes nuevos y afectados por versión: [`docs/mapa-de-versiones.md`](docs/mapa-de-versiones.md).
Movimientos de alcance entre incrementos: [`docs/registro-cambios-alcance.md`](docs/registro-cambios-alcance.md).
Registro de riesgos del proyecto: [`docs/registro-riesgos.md`](docs/registro-riesgos.md).
Alcance detallado por incremento: [`docs/alcance-funciones.md`](docs/alcance-funciones.md).

## Cómo ejecutar

Requiere Python 3.10 o superior. No tiene dependencias externas.

```bash
python -m unittest discover -s tests -t . -v   # suite completa (regresión acumulativa)
python tools/estimacion.py                     # reproduce las estimaciones del informe
python -m portal.app                           # API en http://127.0.0.1:8080/salud
```

Para ver una versión concreta: `git checkout v1.0.0` (o `v1.1.0`, `v1.2.0`) y ejecutar las pruebas.

## Estrategia de ramas y versionado

- `main` contiene siempre la última versión liberable; cada release se marca con una etiqueta anotada `vMAYOR.MENOR.PARCHE` (versionado semántico 2.0.0).
- Como cada incremento agrega capacidad **sin romper** la API ya entregada, los incrementos incrementan la versión MENOR (`v1.0.0` → `v1.1.0` → `v1.2.0`); una versión MAYOR solo se usaría ante un cambio incompatible y las correcciones incrementan el PARCHE.
- Cada funcionalidad se desarrolla en una rama `feature/<incremento>-<tema>` y se integra en `main` mediante merge sin fast-forward, para conservar la trazabilidad.
- El pipeline (`.github/workflows/ci.yml`) compila y prueba el **producto completo** en cada push; en las etiquetas verifica que la versión del código coincide con la etiqueta y publica el artefacto.
- Rollback: se vuelve a desplegar el artefacto de la etiqueta anterior (`git checkout vX.Y.Z`).

## Usuarios de prueba (servicios simulados)

| Usuario | Clave | Rol |
|---|---|---|
| `est001` | `clave-est001` | estudiante |
| `est002` | `clave-est002` | estudiante |
| `fun001` | `clave-fun001` | funcionario |

Los servicios institucionales (SSO, sistema académico, etc.) se simulan en memoria
mediante adaptadores que respetan el contrato de interfaz; no contienen datos reales.
