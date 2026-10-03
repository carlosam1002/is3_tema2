# Alcance detallado por incremento

Lista de funciones que sirve de base al conteo de Puntos de Función de la Unidad 4 del informe.
Se mantiene aquí, y no en el documento, para que cualquier cambio de alcance quede versionado
junto con el cálculo que depende de él: los mismos datos están en `tools/estimacion.py`, que
reproduce las estimaciones al ejecutarse.

Tipos de función (IFPUG, complejidad media): EI = entrada externa (4) · EO = salida externa (5) ·
EQ = consulta externa (4) · ILF = archivo lógico interno (10) · EIF = archivo de interfaz externo (7).
Prioridad MoSCoW: Must es condición de aceptación del incremento; Should puede moverse según la
regla R-MA; Could es lo primero que se mueve.

## Incremento 1 — v1.0.0 — 13 funciones, 71 PF

Must 62 PF · Should 9 PF.

| Código | Función | Tipo | PF | Prioridad |
|---|---|---|---|---|
| F1.01 | Iniciar/cerrar sesión con SSO institucional | EI | 4 | Must |
| F1.02 | Consultar perfil del estudiante | EQ | 4 | Must |
| F1.03 | Actualizar datos de contacto | EI | 4 | Must |
| F1.04 | Consultar calificaciones | EQ | 4 | Must |
| F1.05 | Consultar horario de clases | EQ | 4 | Must |
| F1.06 | Consultar historial y avance de malla | EQ | 4 | Must |
| F1.07 | Consultar estado de inscripción | EQ | 4 | Must |
| F1.08 | Datos de perfil y preferencias (archivo interno) | ILF | 10 | Must |
| F1.09 | Registro de auditoría de accesos (archivo interno) | ILF | 10 | Must |
| F1.10 | Sistema académico institucional (archivo externo) | EIF | 7 | Must |
| F1.11 | Directorio institucional / SSO (archivo externo) | EIF | 7 | Must |
| F1.12 | Gestionar preferencias del usuario | EI | 4 | Should |
| F1.13 | Descargar historial académico en PDF (no oficial) | EO | 5 | Should |

## Incremento 2 — v1.1.0 — 14 funciones, 79 PF

Must 65 PF · Should 10 PF · Could 4 PF.

| Código | Función | Tipo | PF | Prioridad |
|---|---|---|---|---|
| F2.01 | Consultar catálogo de trámites | EQ | 4 | Must |
| F2.02 | Crear solicitud de trámite | EI | 4 | Must |
| F2.03 | Adjuntar documentos a la solicitud | EI | 4 | Must |
| F2.04 | Consultar mis solicitudes | EQ | 4 | Must |
| F2.05 | Ver detalle y línea de tiempo de la solicitud | EQ | 4 | Must |
| F2.06 | Cambiar estado / derivar solicitud (funcionario) | EI | 4 | Must |
| F2.07 | Registrar observación o respuesta (funcionario) | EI | 4 | Must |
| F2.08 | Solicitudes (archivo interno) | ILF | 10 | Must |
| F2.09 | Adjuntos (archivo interno) | ILF | 10 | Must |
| F2.10 | Catálogo de trámites y flujos (archivo interno) | ILF | 10 | Must |
| F2.11 | Sistema de expedientes / Mesa de Entrada (archivo externo) | EIF | 7 | Must |
| F2.12 | Emitir comprobante de solicitud en PDF | EO | 5 | Should |
| F2.13 | Bandeja del funcionario con control de plazos (SLA) | EO | 5 | Should |
| F2.14 | Cancelar solicitud | EI | 4 | Could |

## Incremento 3 — v1.2.0 — 16 funciones, 90 PF

Must 67 PF · Should 18 PF · Could 5 PF.

| Código | Función | Tipo | PF | Prioridad |
|---|---|---|---|---|
| F3.01 | Consultar estado de cuenta (aranceles) | EQ | 4 | Must |
| F3.02 | Iniciar pago en línea | EI | 4 | Must |
| F3.03 | Confirmar pago (notificación de la pasarela) | EI | 4 | Must |
| F3.04 | Emitir comprobante de pago | EO | 5 | Must |
| F3.05 | Consultar historial de pagos | EQ | 4 | Must |
| F3.06 | Enviar notificaciones por correo | EO | 5 | Must |
| F3.07 | Transacciones de pago (archivo interno) | ILF | 10 | Must |
| F3.08 | Notificaciones (archivo interno) | ILF | 10 | Must |
| F3.09 | Pasarela de pagos (archivo externo) | EIF | 7 | Must |
| F3.10 | Proveedor de notificaciones (archivo externo) | EIF | 7 | Must |
| F3.11 | Sistema arancelario / financiero (archivo externo) | EIF | 7 | Must |
| F3.12 | Configurar preferencias de notificación | EI | 4 | Should |
| F3.13 | Bandeja de notificaciones en el portal | EQ | 4 | Should |
| F3.14 | Reporte de trámites por estado y tiempos | EO | 5 | Should |
| F3.15 | Reporte de recaudación | EO | 5 | Should |
| F3.16 | Reporte de uso del portal | EO | 5 | Could |

## Total

43 funciones y 240 PF: 71 PF en I1, 79 PF en I2 y 90 PF en I3.
Los movimientos de alcance entre incrementos están en `registro-cambios-alcance.md`.
