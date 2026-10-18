# Registro de dependencias

Unidad 3 del TP 2 · Portal de Servicios Estudiantiles.
Las dependencias técnicas ocurren dentro del proyecto; las de incremento indican que una versión usa
capacidades de otra anterior; las externas dependen de otras áreas de la institución y son las que más
condicionan las fechas, por eso tienen responsable de seguimiento y disparador de escalamiento.

| ID | Dependencia | Tipo | Origen → destino | Se necesita en | Seguimiento | Riesgo |
|---|---|---|---|---|---|---|
| D-01 | Plataforma base antes de cualquier módulo | Técnica (fin-inicio) | 1.1 → 1.2.x | S2 | Arquitecto | — |
| D-02 | Contrato de interfaz y credenciales del SSO | Externa | Dirección TIC → 1.2.2 | S2 | Líder | R-02 |
| D-03 | Acceso de lectura al sistema académico | Externa | Dirección Académica y TIC → 1.2.4 | S2 | Líder | — |
| D-04 y D-08 | Identidad y perfil de I1 para las solicitudes de I2; eventos de cambio de estado de I2 para las notificaciones de I3 | Entre incrementos | 1.2.2, 1.2.3 → 1.3.3 → 1.4.3 | S7 y S13 | Arquitecto | — |
| D-05 | API del sistema de expedientes | Externa | Mesa de Entrada y TIC → 1.3.5 | S6 | Líder | R-03 |
| D-06 | Convenio firmado con la pasarela de pagos | Externa administrativa | Dirección Financiera → 1.4.2 | S10 | Líder | R-01 |
| D-07 | API del sistema arancelario | Externa | Dirección Financiera y TIC → 1.4.2 | S11 | Integración | — |
| D-09 | Cuenta y credenciales del proveedor de notificaciones | Externa | Proveedor y TIC → 1.4.3 | S13 | Integración | R-12 |
| D-10 | Datos de solicitudes y pagos para los reportes | Entre incrementos | 1.3.3, 1.4.2 → 1.4.4 | S16 | Arquitecto | — |

## Planes alternativos de las dependencias externas

| Dependencia | Disparador de escalamiento | Plan alternativo |
|---|---|---|
| D-02 · SSO | Sin credenciales de prueba al final de S1 | Autenticación local solo en QA; I1 no se libera sin SSO real |
| D-03 · Sistema académico | Sin acceso de lectura al final de S1 | Réplica de solo lectura con extracción nocturna |
| D-05 · Expedientes | Contrato sin firmar en S4 | Registro interno con asignación diferida del número (implementado en v1.1.0) |
| D-06 · Pasarela | Sin firma en S8 | Reordenar I3: notificaciones y reportes primero; pagos en una versión posterior |
| D-07 · Sistema arancelario | Sin API en S9 | Conciliación mediante archivo diario |
| D-09 · Proveedor de correo | Credenciales no disponibles en S11 o tasa de entrega menor al 95 % | Servidor de correo institucional con el mismo adaptador intercambiable (ejecutado en S7, v1.2.1) |
