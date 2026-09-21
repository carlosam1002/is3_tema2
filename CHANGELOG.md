# Registro de cambios

Formato basado en *Keep a Changelog*; versionado semántico.

## [1.2.0] - Incremento 3: pagos, notificaciones y reportes

### Agregado
- Servicio común de notificaciones por correo, con preferencias y bandeja en el portal (F3.06, F3.08, F3.10, F3.12, F3.13).
- Estado de cuenta, pago en línea mediante pasarela con confirmación firmada e idempotente, comprobante e historial (F3.01–F3.05, F3.07, F3.09, F3.11).
- Notificación automática de cada cambio de estado de una solicitud.
- Cancelación de solicitudes por el estudiante (F2.14, movido desde I2 por RCA-02).
- Reportes de trámites por estado y tiempos, y de recaudación (F3.14, F3.15).
- Pruebas de contrato de pasarela, sistema arancelario y proveedor de correo.

### Movido (RCA-03)
- F3.16 Reporte de uso del portal pasa a v1.3.0 (alcance *Could*).

### Seguridad
- El portal no recibe ni almacena datos de tarjetas; la confirmación de pago se valida con firma HMAC.

## [1.1.0] - Incremento 2: solicitudes y seguimiento

### Agregado
- Catálogo de trámites (F2.01, F2.10).
- Creación de solicitudes con adjuntos validados (PDF/JPG/PNG, máximo 5 MB) (F2.02, F2.03).
- Consulta de solicitudes propias y línea de tiempo de estados (F2.04, F2.05).
- Gestión por funcionarios: cambio de estado, derivación y observaciones (F2.06, F2.07).
- Integración con el sistema de expedientes, con reintento ante indisponibilidad (F2.11).
- Comprobante de solicitud en PDF y bandeja con control de plazos (F2.12, F2.13).
- Alcance movido desde I1 (RCA-01): preferencias del usuario (F1.12) e historial en PDF (F1.13).

### Movido (RCA-02)
- F2.14 Cancelar solicitud pasa a I3 (alcance *Could*).

### Compatibilidad
- Las rutas de la API de v1.0.0 no cambian; el perfil agrega el campo `preferencias` (cambio compatible, por eso sube la versión MENOR).

## [1.0.0] - Incremento 1: autenticación, perfil y consultas

### Agregado
- Plataforma base: estructura del proyecto, API HTTP, pipeline de integración continua y script de estimación.
- Inicio y cierre de sesión con el SSO institucional; sesiones con expiración (F1.01).
- Registro de auditoría de accesos y operaciones (F1.09).
- Consulta de perfil y actualización de datos de contacto (F1.02, F1.03).
- Consultas de calificaciones, horario, historial con avance de malla y estado de inscripción (F1.04–F1.07).
- Pruebas de contrato con SSO y sistema académico.

### Movido (RCA-01)
- F1.12 Preferencias del usuario y F1.13 Historial en PDF pasan a I2 (alcance *Should*).
