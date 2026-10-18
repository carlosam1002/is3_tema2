# Tablero de seguimiento, fichas de métrica y mejora

Unidad 9 del TP 2 · Portal de Servicios Estudiantiles.
Los datos de I1 e I2 son los registrados al cierre de cada incremento (simulados para el trabajo
práctico); los de I3 son el pronóstico vigente después del evento de cambio de S7.

## 1. Tablero comparativo I1 – I3

| Métrica | Meta o umbral | I1 (real) | I2 (real) | I3 (pronóstico) | Lectura |
|---|---|---|---|---|---|
| Cumplimiento de alcance comprometido | 100 % | 100 % (62 de 62 PF Must) | 100 % (84 de 84 PF) | 88 PF comprometidos | El compromiso se cumple; lo que se mueve es alcance flexible y queda registrado |
| Cumplimiento del alcance planificado original | ≥ 85 % | 87 % (62 de 71 PF) | 100 % | — | I1 movió 9 PF por RCA-01 |
| Esfuerzo frente a lo estimado | ±10 % | +8,4 % (690 h) | +2,3 % (812 h) | 902,9 h | La recalibración tras I1 corrigió el sesgo de la estimación |
| Productividad | Estabilizar | 8,71 h/PF | 9,0 h/PF | 8,8 h/PF (PERT) | Estable; la diferencia de I2 se explica por la integración con expedientes |
| Defectos nuevos (altos / medios) | 0 altos al liberar | 9 (3 / 6) | 11 (3 / 8) | — | Crece con el tamaño del producto, no con la tasa de error |
| Defectos reabiertos | ≤ 2 por incremento | 3 | 2 | — | Mejora tras reforzar la revisión cruzada |
| Cobertura de regresión de funciones Must | 100 % | 100 % (19 pruebas) | 100 % (35) | 100 % (60 en v1.2.1) | La suite nunca se reduce |
| Predictibilidad de release | 0 días de desvío | 0 días | 0 días | — | Las fechas se sostienen moviendo alcance flexible, no ocultando retrasos |
| Uso de funciones | ≥ 30 % de trámites en línea a las 4 semanas | 62 % de estudiantes activos usó el portal | 41 % de trámites iniciados en línea | — | La adopción (R-11) deja de ser conjetura y pasa a medirse |
| Frecuencia de despliegue a producción | 1 por incremento como mínimo | 1 | 2 (v1.1.0 y v1.2.1) | 1 prevista | El pipeline permite liberar más seguido de lo que exige la gobernanza |
| Tiempo de entrega de un cambio | ≤ 3 días | 3,5 días | 2,1 días | — | Mejoró al habilitar un segundo revisor |
| Tasa de fallos de cambio | ≤ 15 % | 12,5 % (1 de 8) | 0 % (0 de 11) | — | Ningún despliegue requirió rollback en I2 |
| Tiempo de recuperación (MTTR) | ≤ 2 h | 45 min | sin incidentes | — | El rollback ensayado funcionó cuando hizo falta |

## 2. Fichas de métrica

### Cumplimiento de alcance comprometido

| Campo | Contenido |
|---|---|
| Propósito | Saber si el equipo entrega lo que se comprometió a entregar en el incremento |
| Pregunta de gestión | ¿Podemos confiar en el compromiso del próximo incremento? |
| Definición y fórmula | PF con DoD cumplida ÷ PF comprometidos al inicio del incremento × 100 |
| Unidad y fuente | Porcentaje; backlog del incremento y registro de cambios de alcance |
| Frecuencia y responsable | Semanal durante el incremento y al cierre; líder de proyecto |
| Línea base y meta | 100 % comprometido en I1; meta 100 % |
| Interpretación | Por debajo del 95 % se revisa si el problema es estimación, capacidad o alcance mal definido |
| Limitaciones | No dice nada sobre la calidad de lo entregado: se lee junto con defectos y regresión |
| Acción ante desviación | Aplicar la regla R-MA y recalibrar el pronóstico del incremento siguiente |
| Evidencia | RCA-01 a RCA-04 y la recalibración documentada en el informe |

### Defectos reabiertos

| Campo | Contenido |
|---|---|
| Propósito | Detectar correcciones que no resuelven la causa |
| Pregunta de gestión | ¿La revisión y las pruebas están haciendo su trabajo? |
| Definición y fórmula | Cantidad de defectos que vuelven a abrirse después de marcarse como resueltos, por incremento |
| Unidad y fuente | Cantidad; registro de defectos |
| Frecuencia y responsable | Semanal; analista de QA |
| Línea base y meta | 3 en I1; meta ≤ 2 por incremento |
| Interpretación | Dos reaperturas sobre el mismo módulo indican deuda técnica o criterios de aceptación ambiguos |
| Limitaciones | Un número bajo puede esconder defectos que nunca se detectaron |
| Acción ante desviación | Revisión técnica del módulo y, si corresponde, alta de deuda técnica con plan de pago |
| Evidencia | DT-01 y DT-02 del registro de deuda técnica |

### Predictibilidad de release

| Campo | Contenido |
|---|---|
| Propósito | Medir si las fechas comprometidas se sostienen |
| Pregunta de gestión | ¿La institución puede planificar sobre nuestras fechas? |
| Definición y fórmula | Días hábiles entre la fecha comprometida del hito y la fecha real de despliegue |
| Unidad y fuente | Días; plan integrado y etiquetas del repositorio |
| Frecuencia y responsable | Por release; líder de proyecto |
| Línea base y meta | 0 días en I1 y en I2; meta 0 |
| Interpretación | Se lee junto con el cumplimiento de alcance: una fecha cumplida con alcance recortado no es un éxito |
| Limitaciones | Con tres releases la serie es corta; sirve como señal, no como tendencia |
| Acción ante desviación | Reportar el desvío en el Comité con causa y nuevo pronóstico, nunca absorberlo en silencio |
| Evidencia | Fechas de las etiquetas v1.0.0, v1.1.0, v1.2.0 y v1.2.1 |

## 3. Revisión de cierre de I1: lecciones convertidas en ajustes verificables

| Lección | Causa | Ajuste acordado para I2 | Cómo se verifica | Resultado en I2 |
|---|---|---|---|---|
| La plataforma base se subestimó en un 25 % | Se estimó en bloque, sin descomponer | Estimar por tareas con tres puntos y validar con el arquitecto | Desvío de esfuerzo del incremento ≤ 10 % | Cumplido: +2,3 % |
| El alcance flexible se definió tarde, ya con la fecha encima | La prioridad MoSCoW se asignó después de comprometer | Clasificar MoSCoW en el refinamiento, antes de comprometer el incremento | 100 % de las funciones con prioridad antes del inicio | Cumplido; el único movimiento de I2 (RCA-04) vino de un evento externo |
| La revisión cruzada se concentró en una sola persona | No había segundo revisor habilitado | Habilitar un segundo revisor y aplicar «reviso antes de tomar trabajo nuevo» | Tiempo medio en revisión ≤ 1 día | Cumplido: 0,8 días; reaperturas bajaron de 3 a 2 |
| Las pruebas de contrato se escribieron después de integrar | El contrato se firmaba en paralelo a la construcción | Firmar el contrato y escribir su prueba antes del primer commit de la integración | Prueba de contrato existente antes de construir | Cumplido en la integración con expedientes |

## 4. Control integrado

Las decisiones no se toman por dimensión aislada. El evento de cambio de S7 lo muestra: afectó alcance
(F3.13 pasa a v1.3.0), cronograma (H3 se sostiene en S21), costo (−8,8 h en I3), calidad (una prueba de
contrato nueva), riesgos (R-12 se materializa y se cierra) y configuración (versión v1.2.1 con nota de
versión). Todo quedó registrado en el mismo juego de artefactos, que es lo que permite explicar la
decisión meses después.
