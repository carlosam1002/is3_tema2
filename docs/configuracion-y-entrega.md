# Gestión de configuración, DevOps y entrega

Unidad 8 del TP 2 · Portal de Servicios Estudiantiles.

## 1. Elementos de configuración

| Elemento | Dónde vive | Responsable | Estado | Identificación |
|---|---|---|---|---|
| Alcance y funciones (43 ítems) | `docs/alcance-funciones.md` | Product Owner | Aprobado | Códigos F1.xx a F3.xx |
| Código fuente del portal | `portal/` | Arquitecto | Liberado | Etiquetas v1.0.0 a v1.2.1 |
| Suite de pruebas | `tests/` | Analista de QA | Liberado | Misma etiqueta que el código |
| Contratos de interfaz | Docstring de cada adaptador y `tests/test_contratos.py` | Integración | Aprobado | Nombre del adaptador |
| Documentación de gestión | `docs/` | Líder de proyecto | Vigente | Commit que la modifica |
| Pipeline y ambientes | `.github/workflows/ci.yml` | Integración | Operativo | Versión del flujo |
| Artefactos de release | Artefacto publicado por el pipeline en cada etiqueta | Integración | Liberado | `portal-vX.Y.Z.zip` |
| Registros de gestión | `registro-riesgos.md`, `registro-cambios-alcance.md` | Líder de proyecto | Vigente | Fila con ID propio |

## 2. Líneas base

| Línea base | Qué congela | Cuándo se aprueba | Quién aprueba |
|---|---|---|---|
| Requisitos | Alcance global y contenido comprometido de cada incremento | Fin de S2 y al inicio de cada incremento | Product Owner |
| Diseño | Arquitectura, modelo de datos y contratos de interfaz | Fin de S2 (ADR-001 a ADR-003) | Arquitecto y Dirección TIC |
| Construcción | Código que entra al congelamiento del incremento | Semana de freeze de cada incremento | Integración |
| Release | Versión etiquetada y desplegada | Al liberar v1.0.0, v1.1.0, v1.2.0 y v1.2.1 | Product Owner con informe de QA |

## 3. Ramas, commits y control de cambios

- `main` siempre contiene la última versión liberable; nadie trabaja directamente sobre ella.
- Cada función se desarrolla en `feature/<incremento>-<tema>` y se integra con merge sin fast-forward,
  de modo que el historial muestra qué cambios entraron juntos y por qué.
- Los commits siguen Conventional Commits (`feat`, `fix`, `docs`, `test`, `chore`, `release`) y citan el
  código de la función o el registro que los origina.
- El flujo de cambio es el mismo que usa el proyecto para el alcance: solicitud, análisis de impacto,
  aprobación del PO, implementación y verificación. Queda trazado en `registro-cambios-alcance.md`.
- Trazabilidad completa: función (F1.xx) → commit → prueba → etiqueta → nota de versión.

## 4. Versionado y etiquetado

Versionado semántico 2.0.0. Cada incremento agrega capacidad compatible, así que sube la versión MENOR;
el cambio de proveedor de correo solo reemplazó una implementación y subió el PARCHE.

| Etiqueta | Contenido | Tipo de cambio |
|---|---|---|
| `v1.0.0` | Primera versión en producción: identidad, perfil y consultas | Versión inicial |
| `v1.1.0` | Solicitudes y seguimiento | MENOR: capacidad nueva compatible |
| `v1.2.0` | Pagos, notificaciones y reportes | MENOR: capacidad nueva compatible |
| `v1.2.1` | Notificaciones por el correo institucional | PARCHE: cambia la implementación, no la API |
| `v1.3.0` | Reporte de uso y bandeja de notificaciones | MENOR, planificada |

## 5. Matriz de compatibilidad

| Consumidor | v1.0.0 | v1.1.0 | v1.2.0 | v1.2.1 |
|---|---|---|---|---|
| Frontend web del portal | Compatible | Compatible | Compatible | Compatible |
| Integración con el sistema académico (lectura) | Compatible | Compatible | Compatible | Compatible |
| Integración con expedientes | No aplica | Compatible | Compatible | Compatible |
| Pasarela de pagos (confirmación firmada) | No aplica | No aplica | Compatible | Compatible |
| Notificaciones por correo | No aplica | No aplica | Proveedor externo | Correo institucional |

Las rutas de la API entregadas en v1.0.0 siguen respondiendo igual en v1.2.1: lo único que cambió en el
perfil es un campo agregado, que los clientes anteriores ignoran.

## 6. Ambientes, despliegue y rollback

| Ambiente | Propósito | Datos | Despliegue | Aprueba |
|---|---|---|---|---|
| Desarrollo | Trabajo diario del equipo | Ficticios | Automático en cada push | — |
| QA | Pruebas automatizadas e integración con servicios de prueba | Ficticios | Automático al integrar en `main` | Integración |
| Preproducción | Regresión completa, carga y UAT | Copia anonimizada | Manual desde una etiqueta | Analista de QA |
| Producción | Uso real | Reales | Manual desde la misma etiqueta probada | Product Owner con informe de QA |

El rollback consiste en volver a desplegar el artefacto de la etiqueta anterior, que el pipeline conserva.
Se ensaya en preproducción antes de cada release, y las migraciones de datos son reversibles.

## 7. Pipeline

| Etapa | Qué hace | Criterio de corte |
|---|---|---|
| Compilación | Compila el producto completo en dos versiones de Python | Cualquier error detiene el flujo |
| Pruebas | Unitarias, de contrato, de humo y regresión acumulada | Una prueba en rojo detiene el flujo |
| Reproducción de estimaciones | Ejecuta `tools/estimacion.py` | Debe correr sin errores |
| Verificación de etiqueta | Comprueba que la versión del código coincida con la etiqueta | Una diferencia detiene la publicación |
| Publicación | Empaqueta y publica el artefacto de la versión | — |

El pipeline prueba **el producto completo**, no solo el código del incremento nuevo: es lo que sostiene la
compatibilidad entre versiones que exige el enfoque incremental.

## 8. Controles de seguridad en el flujo (DevSecOps)

- Secretos y credenciales fuera del repositorio, inyectados como variables del pipeline por ambiente.
- Revisión de dependencias y análisis estático previstos como etapa del pipeline antes de cada release.
- Revisión de seguridad obligatoria antes de liberar: un hallazgo de severidad alta bloquea la entrega.
- El punto público de confirmación de pagos se valida con firma y es idempotente (riesgo R-06).
- El portal no almacena datos de tarjetas: el pago ocurre en la página de la pasarela.
