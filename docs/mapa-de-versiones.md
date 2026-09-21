# Mapa de versiones

Leyenda: **N** nuevo · **M** modificado · **R** sin cambios, cubierto por regresión · — no existe.

| Componente | v1.0.0 (I1) | v1.1.0 (I2) | v1.2.0 (I3) |
|---|---|---|---|
| Frontend web (PWA) | N | M | M |
| API Gateway / BFF (`portal/app.py`) | N | M | M |
| Identidad y adaptador SSO (`identidad.py`, `adaptadores/sso.py`) | N | R | R |
| Perfil del estudiante (`perfil.py`) | N | M | M |
| Consultas académicas (`consultas.py`, `adaptadores/academico.py`) | N | M | R |
| Auditoría de accesos (`auditoria.py`) | N | M | M |
| Base de datos del portal | N | M | M |
| Solicitudes y flujo de trámites (`solicitudes.py`) | — | N | M |
| Almacenamiento de adjuntos | — | N | R |
| Adaptador de expedientes (`adaptadores/expedientes.py`) | — | N | R |
| Pagos y adaptador de pasarela (`pagos.py`, `adaptadores/pasarela.py`) | — | — | N |
| Adaptador del sistema arancelario (`adaptadores/arancelario.py`) | — | — | N |
| Notificaciones y adaptador de proveedor (`notificaciones.py`) | — | — | N |
| Reportes (`reportes.py`) | — | — | N |
| Pipeline CI/CD e infraestructura | N | M | M |

En el prototipo, el frontend y la base de datos se representan por la API HTTP y
por repositorios en memoria, respectivamente.
