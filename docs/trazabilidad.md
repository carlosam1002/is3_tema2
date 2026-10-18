# Matriz de trazabilidad de la entrega (Unidades 2 a 9)

TP 2 · Portal de Servicios Estudiantiles. Cada fila cruza lo que pide la unidad, dónde está resuelto en
el informe, qué artefacto de este repositorio lo evidencia y con qué criterio se verifica.

| Unidad | Decisión o actividad | Artefacto o enlace | Criterio de aceptación |
|---|---|---|---|
| 2 | Selección y justificación del modelo incremental | Secciones 2.1 y 2.2 del informe; DEC-01 | Cada condición del caso tiene una implicancia explícita en el enfoque |
| 2 | Definición de incrementos y mapa de versiones | Secciones 2.3 y 2.4; `docs/mapa-de-versiones.md`; etiquetas v1.0.0 a v1.2.0 | Cada incremento tiene contenido, valor, dependencias y criterio de aceptación |
| 3 | Alcance global y por incremento; EDT | Secciones 3.1 a 3.3; figura 1; `docs/alcance-funciones.md`; `docs/edt.md` | El 100 % de las funciones está asignado a un incremento y a un paquete de la EDT |
| 3 | Dependencias, plan de releases y regla R-MA | Secciones 3.4 y 3.5; `docs/dependencias.md`; `docs/registro-cambios-alcance.md` | Todo movimiento de alcance registrado con causa, impacto y aprobación |
| 4 | Estimación de tamaño, esfuerzo, duración y costo | Secciones 4.1 a 4.4; `tools/estimacion.py` | Los resultados se reproducen al ejecutar el script |
| 4 | Cronograma, hitos, solapamientos y recalibración | Secciones 4.5 y 4.6; figura 2 | Pronóstico actualizado y comparado con la línea base |
| 5 | Equipo, roles, RACI y liderazgo | Secciones 5.1 a 5.3 | Un único responsable que aprueba (A) por actividad |
| 5 | Comunicación, dependencias externas y resolución del conflicto | Secciones 5.4 a 5.7; DEC-09 | Conflicto resuelto con criterios explícitos y decisión registrada |
| 6 | Identificación, análisis y respuesta a los riesgos | Secciones 6.1 a 6.4; figura 3; `docs/registro-riesgos.md` | Trece entradas con causa-evento-efecto, categoría, exposición, respuesta, responsable y disparador |
| 6 | Monitoreo de riesgos y reducción anticipada | Secciones 6.5 y 6.6; DEC-06, DEC-10 y DEC-11 | Cada entrada tiene indicador, estado, riesgo residual y riesgo secundario |
| 7 | Matriz de calidad, criterios de aceptación, regresión y deuda técnica | Secciones 7.1 a 7.5; `docs/plan-de-pruebas.md`; suite de 60 pruebas | Cada atributo tiene métrica, umbral y forma de verificación; cada deuda, plan de pago |
| 8 | Configuración, versionado, ambientes, pipeline y compatibilidad | Secciones 8.1 a 8.6; `docs/configuracion-y-entrega.md`; `.github/workflows/ci.yml`; etiquetas v1.0.0 a v1.2.1 | Trazabilidad reproducible de requisito a release; cada versión convive con la anterior |
| 9 | Tablero, fichas de métrica, revisión de cierre y control integrado | Secciones 9.1 a 9.5; `docs/metricas.md` | Cada métrica conduce a una decisión; cada lección, a un ajuste verificado |
| 7 a 9 | Evento de cambio y actualización de las cuatro dimensiones | Sección 10; DEC-15; RCA-04; etiqueta v1.2.1 | Riesgos, estimaciones, configuración y métricas actualizados con la misma decisión |

## Cadena de trazabilidad técnica

Para cualquier función entregada, la cadena completa es: **función (F1.xx – F3.xx) → commit que la
implementa → prueba automatizada que la cubre → etiqueta que la liberó → nota de versión**. Se recorre en
los dos sentidos: desde un requisito hasta la versión que lo entregó, y desde un defecto hasta el cambio
que lo introdujo.
