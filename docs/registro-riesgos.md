# Registro de riesgos

Portal de Servicios Estudiantiles · Unidad 6 del TP 2 (Ingeniería de Software III, LCIK).

Este registro está vivo: se revisa como punto fijo de la reunión semanal y se actualiza
formalmente al cierre de cada incremento. Cada cambio queda en el historial del repositorio,
de modo que puede verse qué sabía el equipo en cada momento del proyecto.

**Escalas.** Probabilidad e impacto se miden en tres niveles (1 bajo, 2 medio, 3 alto). La
exposición es el producto de ambos: 9 crítica, 6 alta, 3 o 4 media, 1 o 2 baja. La escala ordena,
pero no decide sola: urgencia, proximidad, dificultad de detección y dependencias críticas pueden
elevar un riesgo de categoría, como ocurre con R-07.

**Estados posibles.** Activo · Cerrado · Materializado · Nuevo · Revaluado.

**Redacción.** Debido a *[causa]*, podría ocurrir *[evento]*, lo que produciría *[impacto]* sobre
*[objetivo]*.

## Resumen

| ID | Riesgo | Categoría | P | I | Exp. | Prioridad | Respuesta | Responsable | Incremento | Estado |
|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Convenio con la pasarela de pagos sin firmar a tiempo | Dependencia externa · proveedor | 3 | 3 | 9 | Crítica | Mitigar y transferir | Líder | Se reduce en I2; se materializaría al inicio de I3 | Activo |
| R-02 | Demora en la integración del SSO institucional | Integración · técnico | 3 | 3 | 9 | Crítica | Mitigar | Arquitecto | Materializado en I1 | Cerrado |
| R-03 | Interfaz de expedientes no disponible o con cambios | Integración · proveedor | 2 | 3 | 6 | Alta | Mitigar | Integración | Se reduce en I2 | Activo |
| R-04 | Migración de esquema que daña datos en producción | Compatibilidad | 2 | 3 | 6 | Alta | Mitigar | Arquitecto | Se reduce en I2 y en I3 | Activo |
| R-05 | Deuda técnica acumulada por la presión de la fecha de I1 | Deuda técnica | 3 | 2 | 6 | Alta | Mitigar | Analista de QA | Se controla en cada incremento | Activo |
| R-06 | Confirmación de pago falsificada o repetida | Seguridad | 2 | 3 | 6 | Alta | Mitigar | Arquitecto | Se reduce en I3 | Activo |
| R-07 | Exposición de datos por falla del control de acceso | Seguridad · privacidad | 1 | 3 | 3 | Alta (DEC-10) | Mitigar | Arquitecto | Se controla desde I1 | Activo |
| R-08 | Crecimiento del alcance durante el piloto | Requisitos · alcance | 3 | 2 | 6 | Alta | Mitigar | Líder y PO | Se controla con la regla R-MA | Activo |
| R-09 | Estimaciones cortas por productividad supuesta | Gestión · estimación | 3 | 2 | 6 | Alta | Mitigar | Líder | Materializado en I1; recalibrado | Materializado |
| R-10 | Ausencia prolongada de un rol clave | Organizacional · personas | 2 | 3 | 6 | Alta | Mitigar | Líder | Se controla en los tres incrementos | Activo |
| R-11 | Baja adopción: se sigue usando la ventanilla | Adopción | 3 | 2 | 6 | Alta | Mitigar | Líder | Se mide desde I1; crítico en I2 | Activo |
| R-12 | Indisponibilidad del proveedor de correo | Dependencia externa | 2 | 2 | 4 | Media | Transferir y mitigar | Integración | Se reduce en I3 | Activo |
| O-01 | Oportunidad: reutilizar las notificaciones para avisos académicos | Oportunidad | 2 | 2 | 4 | Media | Explotar | Arquitecto | Se evalúa al cierre de I3 | Abierta |

## Fichas de los riesgos de prioridad crítica y alta

### R-01 · Convenio con la pasarela de pagos

- **Descripción:** debido a que el convenio con la pasarela depende de un trámite ajeno al equipo, podría no firmarse antes de S10, lo que impediría integrar pagos y retrasaría v1.2.0.
- **Acciones preventivas:** seguimiento semanal con la Dirección Financiera; prueba de concepto contra el entorno de pruebas de la pasarela sin esperar la firma; adaptador de pasarela intercambiable.
- **Disparador:** convenio sin firma al cierre de S8.
- **Contingencia:** reordenar I3 (notificaciones y reportes primero) y mover pagos a una versión posterior.
- **Indicador:** estado del convenio informado cada semana y días restantes hasta S10.
- **Riesgo residual:** medio; aun firmado, la habilitación en producción puede demorar.
- **Riesgo secundario:** reordenar I3 posterga el reporte de recaudación y tensiona la relación con Finanzas.

### R-02 · Integración del SSO institucional

- **Descripción:** debido a que el directorio institucional no tiene un ambiente de pruebas documentado, podría demorarse la integración del inicio de sesión, lo que consumiría la holgura de I1 y pondría en riesgo H1.
- **Acciones preventivas:** prueba de concepto en las semanas 1 y 2; contrato de interfaz firmado antes de construir.
- **Disparador:** sin credenciales de prueba al cierre de S1.
- **Contingencia:** autenticación local solo en QA; I1 no se libera sin SSO real.
- **Indicador:** fecha del primer inicio de sesión real en QA (hito HI-1).
- **Estado:** materializado en I1 y cerrado. La plataforma base consumió 150 h frente a 120 h previstas; el alcance flexible de I1 (9 PF) se movió a I2 por la regla R-MA (RCA-01).
- **Riesgo residual:** bajo; la integración quedó operativa y cubierta por regresión.

### R-03 · Interfaz del sistema de expedientes

- **Descripción:** debido a que la interfaz de expedientes puede cambiar o no estar disponible, podría fallar la asignación del número de expediente, lo que dejaría solicitudes sin trazabilidad formal.
- **Acciones preventivas:** contrato de interfaz firmado en S6; prueba de contrato automatizada en el pipeline; reintento de asignación implementado en v1.1.0.
- **Disparador:** contrato sin firmar en S4, o prueba de contrato en rojo dos días seguidos.
- **Contingencia:** registro interno de la solicitud con asignación diferida del número.
- **Indicador:** porcentaje de solicitudes con número de expediente asignado (meta: 100 %).
- **Riesgo residual:** bajo. **Secundario:** las solicitudes con número diferido exigen un control manual de conciliación.

### R-04 · Migraciones de esquema entre versiones

- **Descripción:** debido a que cada incremento modifica el esquema de datos, una migración podría dañar información en producción, lo que obligaría a un rollback y afectaría la confianza.
- **Acciones preventivas:** migraciones reversibles ensayadas en preproducción con copia anonimizada; regresión acumulativa antes de cada release.
- **Disparador:** un ensayo de migración fallido o regresión por debajo del 100 % de las funciones Must.
- **Contingencia:** rollback al artefacto de la etiqueta anterior y nueva ventana de despliegue.
- **Indicador:** resultado del ensayo de migración y porcentaje de regresión en verde.

### R-05 · Deuda técnica

- **Descripción:** debido a la presión de la fecha fija de I1, el equipo podría postergar pruebas y refactorizaciones, lo que encarecería la regresión y reduciría la capacidad de los incrementos siguientes.
- **Acciones preventivas:** reserva del 10 % de la capacidad de cada incremento para deuda técnica (DEC-11); no se libera con la suite en rojo.
- **Disparador:** cobertura de regresión de funciones Must menor al 100 %, o más de dos defectos reabiertos en un incremento.
- **Contingencia:** congelar alcance nuevo durante una semana y dedicarla a saldar deuda.
- **Indicador:** pruebas automatizadas por versión (19 en v1.0.0, 35 en v1.1.0, 56 en v1.2.0) y defectos reabiertos.

### R-06 · Confirmación de pago falsificada o repetida

- **Descripción:** debido a que la confirmación de pagos se expone en un punto público, podría recibirse una notificación falsificada o repetida, lo que registraría pagos inexistentes.
- **Acciones preventivas:** validación de firma, idempotencia por referencia, conciliación diaria y pruebas de seguridad.
- **Disparador:** una confirmación con firma inválida o una diferencia de conciliación en el día.
- **Contingencia:** suspender el canal en línea, conciliar manualmente y reabrir con la corrección desplegada.
- **Indicador:** confirmaciones rechazadas por firma y diferencias de conciliación.

### R-07 · Exposición de datos por falla del control de acceso

- **Descripción:** debido a que el portal concentra datos académicos y de pago, una falla del control de acceso por rol podría exponer información de otros estudiantes, con consecuencias normativas.
- **Por qué es prioritario pese a su exposición 3:** un incidente de privacidad no se revierte con una corrección posterior (DEC-10).
- **Acciones preventivas:** control de acceso por rol cubierto por la regresión; auditoría de accesos desde v1.0.0; revisión de seguridad antes de cada release; sin datos de tarjeta en el portal.
- **Disparador:** un hallazgo de severidad alta en la revisión o un patrón de accesos anómalo en la auditoría.
- **Contingencia:** bloquear la función afectada, avisar a la Dirección TIC y corregir fuera de ciclo.
- **Indicador:** hallazgos de severidad alta abiertos y accesos fallidos por usuario.

### R-08 · Crecimiento del alcance durante el piloto

- **Descripción:** debido a que los requisitos se conocen a nivel macro, podrían ingresar pedidos nuevos durante el piloto, lo que desplazaría las fechas de H2 y H3.
- **Acciones preventivas:** regla R-MA y backlog de incrementos futuros; el cambio urgente se intercambia por alcance equivalente.
- **Disparador:** más de 10 PF de pedidos nuevos sobre un incremento en curso.
- **Contingencia:** el Comité decide entre nueva línea base o postergación.
- **Indicador:** puntos de función solicitados frente a intercambiados y movimientos del RCA.

### R-09 · Estimaciones cortas

- **Descripción:** debido a que la productividad inicial se basó en un supuesto, las estimaciones de I2 e I3 podrían quedar cortas, lo que acumularía retrasos sin señal temprana.
- **Estado:** materializado en I1. La productividad real fue de 8,71 h/PF frente a 8,0 h/PF previstas (+8,9 %) y la capacidad efectiva, de 115 h/semana frente a 120. Se recalibró el pronóstico de I2 e I3 (DEC-07) y se reportó una semana de desvío en H2 y H3.
- **Acciones preventivas:** recalibración al cierre de cada incremento; reserva de contingencia de un desvío estándar.
- **Disparador:** desvío de esfuerzo mayor al 10 % a mitad de incremento.
- **Indicador:** horas por punto de función reales y consumo de la reserva.

### R-10 · Ausencia de un rol clave

- **Descripción:** debido a que el equipo es pequeño y con dedicación parcial, la ausencia prolongada de un rol clave podría detener la integración o la liberación.
- **Acciones preventivas:** suplente designado por rol; revisión cruzada obligatoria; decisiones técnicas en ADR.
- **Disparador:** ausencia prevista de más de una semana en un rol cuyo suplente no esté al día.
- **Contingencia:** reasignar responsabilidades y reducir alcance flexible del incremento en curso.
- **Indicador:** capacidad real frente a la planificada (115 h frente a 120 h por semana).

### R-11 · Baja adopción

- **Descripción:** debido a que el portal reemplaza trámites presenciales, estudiantes y funcionarios podrían seguir usando la ventanilla, lo que reduciría el valor de cada incremento.
- **Acciones preventivas:** comunicación por release con guía rápida; piloto controlado de dos días; capacitación de funcionarios antes de v1.1.0 y v1.2.0.
- **Disparador:** menos del 30 % de trámites iniciados en línea a las cuatro semanas de v1.1.0.
- **Contingencia:** campaña con el Centro de Estudiantes y acompañamiento en ventanilla por dos semanas.
- **Indicador:** porcentaje de trámites iniciados en línea y consultas resueltas en el portal.

## Riesgos adelantados a incrementos previos

| Riesgo | Mecanismo | Cuándo | Evidencia |
|---|---|---|---|
| R-02 · SSO | Prueba de concepto y contrato de interfaz | S1 – S3, antes de construir identidad | Inicio de sesión real en QA (HI-1) |
| R-03 · Expedientes | Contrato firmado y prueba de contrato automatizada | S5 – S6, un incremento antes de usarlo | 100 solicitudes con número de expediente (HI-2) |
| R-01 · Pasarela | Prueba de concepto en el entorno de pruebas y contrato con el sistema arancelario | S10 – S11, durante I2 | Flujo de pago completo con conciliación (HI-3) |

## Historial de revisiones

| Fecha | Revisión | Cambios |
|---|---|---|
| Cierre de I1 (S6) | 1.0 | Alta del registro con 12 riesgos y 1 oportunidad. R-02 y R-09 pasan a materializados; se recalibra el pronóstico y se registran RCA-01 a RCA-03. |
