# Calidad: matriz, criterios de aceptación y plan de pruebas

Unidad 7 del TP 2 · Portal de Servicios Estudiantiles.

## 1. Matriz de calidad del producto (ISO/IEC 25010)

| Atributo | Requisito de calidad | Métrica y umbral | Verificación | Responsable | Evidencia |
|---|---|---|---|---|---|
| Adecuación funcional | Las funciones Must del incremento hacen lo que el criterio de aceptación define | 100 % de las funciones Must con criterios verificados | Pruebas automatizadas y UAT | QA | Suite en verde y acta de UAT |
| Eficiencia de desempeño | Las consultas responden sin degradar la experiencia | p95 ≤ 2 s con 200 usuarios concurrentes | Prueba de carga antes de cada release | Integración | Informe de carga |
| Compatibilidad | Cada versión convive con lo entregado antes y con los sistemas institucionales | 100 % de la regresión acumulada y de las pruebas de contrato en verde | Pipeline en cada cambio | QA e Integración | Resultado del pipeline |
| Fiabilidad | El portal opera sin fallas que impidan el trámite | 0 defectos críticos o altos abiertos al liberar | Gestión de defectos y pruebas de resiliencia | QA | Registro de defectos |
| Seguridad | El acceso se controla por rol y no se almacenan datos de tarjeta | 0 hallazgos de severidad alta abiertos; firma válida en el 100 % de las confirmaciones de pago | Revisión de seguridad por release y pruebas automatizadas | Arquitecto | Informe de revisión |
| Mantenibilidad | El producto se puede modificar con bajo riesgo | Cobertura de regresión del 100 % de las funciones Must; deuda registrada y priorizada | Revisión técnica por incremento | Arquitecto | Registro de deuda técnica |

## 2. Criterios de aceptación y umbrales de defectos por incremento

| Incremento | Criterios de aceptación | Umbral para liberar |
|---|---|---|
| I1 · v1.0.0 | SSO operativo con cuentas reales en preproducción; datos coincidentes con el sistema académico en una muestra de 50 estudiantes; p95 ≤ 2 s con 200 concurrentes; despliegue y rollback ejecutados desde el pipeline | 0 críticos, 0 altos, hasta 3 medios con fecha de corrección comprometida |
| I2 · v1.1.0 | Al menos 5 tipos de trámite de punta a punta; 100 % de las solicitudes con número de expediente en una prueba de 100; cambio de estado visible en menos de 1 minuto; regresión de I1 al 100 % | 0 críticos, 0 altos, hasta 3 medios |
| I3 · v1.2.0 | Pagos exitosos en sandbox y producción controlada con conciliación del 100 % en 100 transacciones; 95 % de las notificaciones en menos de 5 minutos; reportes que cuadran con las fuentes; regresión de I1 e I2 al 100 % | 0 críticos, 0 altos, hasta 2 medios; ningún defecto de seguridad abierto |

## 3. Estrategia de pruebas y regresión acumulativa

| Nivel | Qué cubre | Cuándo se ejecuta | Evidencia |
|---|---|---|---|
| Unitarias y de servicio | Reglas de negocio de cada módulo | En cada cambio, en el pipeline | 60 pruebas en v1.2.1 |
| Contrato de interfaz | Formato y errores acordados con SSO, sistema académico, expedientes, pasarela, sistema arancelario y proveedores de correo | En cada cambio; en el ambiente de integración contra los servicios reales | `tests/test_contratos.py` |
| Regresión acumulativa | Todas las funciones Must de los incrementos anteriores | Antes del congelamiento y en cada etiqueta | 19 pruebas en v1.0.0, 35 en v1.1.0, 60 en v1.2.1 |
| Humo de la API | El producto completo arranca y responde | En cada cambio | `tests/test_smoke_api.py` |
| Aceptación (UAT) | Criterios de aceptación del incremento, ejecutados por el PO | En la semana de cierre del incremento | Acta de UAT |

La suite crece con cada versión y nunca se reduce: una función entregada queda cubierta mientras exista.
Si la regresión no está en verde, no se libera, aunque la funcionalidad nueva esté terminada.

## 4. Verificación de interfaces

Cada integración tiene un contrato acordado con el área dueña del sistema y una prueba automatizada que
lo verifica. La misma suite corre contra los adaptadores simulados en el pipeline y contra los servicios
reales en el ambiente de integración, de modo que un cambio del proveedor se detecta antes de llegar a
producción. El caso de v1.2.1 muestra el valor de la práctica: al reemplazar el proveedor de correo, el
servicio de notificaciones no cambió porque el adaptador nuevo cumple el mismo contrato.

## 5. Registro de deuda técnica

| ID | Deuda | Origen | Interés que paga el proyecto | Plan de pago | Estado |
|---|---|---|---|---|---|
| DT-01 | El adaptador de SSO resuelve la renovación de sesión con una espera fija en lugar de refrescar el token | Decisión rápida de I1 para llegar al hito H1 | Sesiones que expiran durante un trámite largo y consultas repetidas al directorio | Refactorizar en I2 con la reserva del 10 % | Pagada en I2 |
| DT-02 | La validación de adjuntos usa la extensión del archivo y no su tipo real | Decisión rápida de I2 ante la falta de acuerdo sobre la biblioteca | Riesgo de archivos maliciosos y retrabajo en la revisión de seguridad | Validar el tipo real en I3, antes de la revisión de seguridad del release | Pagada en I3 |
| DT-03 | Los reportes repiten consultas que ya hace la bandeja de funcionarios | Entrega rápida de los reportes al cierre de I3 | Tiempos de respuesta mayores y doble mantenimiento de la misma consulta | Unificar la consulta en v1.3.0 | Pendiente |

**Reserva explícita:** cada incremento aparta el 10 % de su capacidad para pagar deuda técnica (decisión
DEC-11 del informe). No es tiempo libre: se planifica, se estima y se revisa como cualquier otro trabajo.
