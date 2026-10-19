# Portal de Servicios Estudiantiles

Prototipo verificable del **TP 2 — Enfoque Incremental** (Ingeniería de Software III, LCIK),
entrega de las **Unidades 2 a 9**. El repositorio materializa el plan de releases del informe:
cada incremento es una versión desplegable, etiquetada y probada junto con todo lo entregado
antes, y cada unidad deja aquí el artefacto con el que se verifica lo que el informe afirma.

Integrantes: Carlos Francisco Arguello Monges y Rodney Rodriguez.

## Plan de releases

| Release | Incremento | Capacidad nueva | Estado |
|---|---|---|---|
| `v1.0.0` | I1 | Autenticación SSO, perfil y consultas académicas | Liberado |
| `v1.1.0` | I2 | Solicitudes de trámites y seguimiento | Liberado |
| `v1.2.0` | I3 | Pagos, notificaciones y reportes | Liberado |
| `v1.2.1` | I3 | Notificaciones por el correo institucional (evento de cambio, R-12) | Liberado |
| `v1.3.0` | — | Reporte de uso del portal y bandeja de notificaciones (RCA-03 y RCA-04) | Planificado |

## Documentación por unidad

| Unidad | Qué aporta | Artefacto |
|---|---|---|
| 2 · Enfoque | Componentes nuevos y afectados por versión | [`docs/mapa-de-versiones.md`](docs/mapa-de-versiones.md) |
| 3 · Planificación | Alcance por función (43 ítems) | [`docs/alcance-funciones.md`](docs/alcance-funciones.md) |
| 3 · Planificación | EDT con su diccionario y dependencias | [`docs/edt.md`](docs/edt.md) · [`docs/dependencias.md`](docs/dependencias.md) |
| 3 · Planificación | Movimientos de alcance entre incrementos (RCA-01 a RCA-04) | [`docs/registro-cambios-alcance.md`](docs/registro-cambios-alcance.md) |
| 4 · Estimación | Script que reproduce todas las cifras del informe | [`tools/estimacion.py`](tools/estimacion.py) |
| 6 · Riesgos | Registro de 13 entradas con respuesta, disparador e indicador | [`docs/registro-riesgos.md`](docs/registro-riesgos.md) |
| 7 · Calidad | Plan de pruebas, matriz de calidad y deuda técnica | [`docs/plan-de-pruebas.md`](docs/plan-de-pruebas.md) |
| 8 · Configuración y DevOps | Líneas base, versionado, ambientes y pipeline | [`docs/configuracion-y-entrega.md`](docs/configuracion-y-entrega.md) |
| 9 · Monitoreo y mejora | Tablero, fichas de métrica y lecciones convertidas en ajustes | [`docs/metricas.md`](docs/metricas.md) |
| 2 a 9 | Trazabilidad unidad → sección del informe → evidencia | [`docs/trazabilidad.md`](docs/trazabilidad.md) |

La Unidad 5 (personas y comunicación) no deja artefacto de código: se resuelve íntegramente en el informe.
Para contrastar el informe contra las estimaciones: `python tools/verificar_informe.py <informe.pdf>`
(requiere `pdftotext`); compara 16 cifras clave y falla si alguna difiere.

## Cómo ejecutar

Requiere Python 3.10 o superior. No tiene dependencias externas.

```bash
python -m unittest discover -s tests -t . -v   # suite completa (regresión acumulativa)
python tools/estimacion.py                     # reproduce las estimaciones del informe
python -m portal.app                           # portal en http://127.0.0.1:8080
```

Con el servidor levantado, `http://127.0.0.1:8080` abre la **interfaz web** del portal y
`http://127.0.0.1:8080/salud` responde el estado y la versión. La interfaz es la capa de
presentación: no tiene lógica propia, consume la misma API que verifica la suite de pruebas.
Se agregó después de la etiqueta `v1.2.1` para la demostración, por lo que la suite verificada
de esa versión sigue siendo de 60 pruebas. Los datos viven en memoria: al reiniciar el servidor
el portal vuelve al estado inicial.

Como la pasarela de pagos está simulada, la página de pago que alojaría el proveedor se
reemplaza por la ruta `POST /api/simulacion/pasarela`, que genera la notificación firmada y la
entrega al mismo callback público `POST /api/pagos/confirmacion`, sin saltear ninguna validación.

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
