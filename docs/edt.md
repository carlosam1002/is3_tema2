# EDT orientada a incrementos

Unidad 3 del TP 2 · Portal de Servicios Estudiantiles.
La estructura se organiza por incrementos y no por fases: cada rama de incremento contiene su propio
análisis, construcción, pruebas y release, de modo que termina en una versión desplegable. Las ramas
transversales agrupan el trabajo que no pertenece a un único incremento.

```
1. Portal de Servicios Estudiantiles
├── 1.0 Gestión del proyecto
│   ├── 1.0.1 Planificación y línea base
│   ├── 1.0.2 Seguimiento y pronóstico
│   ├── 1.0.3 Control de cambios (regla R-MA y RCA)
│   └── 1.0.4 Comunicación y dependencias
├── 1.1 Plataforma base
│   ├── 1.1.1 Arquitectura y ADR
│   ├── 1.1.2 Ambientes y pipeline CI/CD
│   └── 1.1.3 Contratos de interfaz de I1 y prueba de concepto de SSO
├── 1.2 Incremento 1 · v1.0.0
│   ├── 1.2.1 Análisis y diseño de I1
│   ├── 1.2.2 Autenticación e identidad
│   ├── 1.2.3 Perfil del estudiante
│   ├── 1.2.4 Consultas académicas
│   ├── 1.2.5 Pruebas, regresión y UAT
│   └── 1.2.6 Release v1.0.0 y demostración
├── 1.3 Incremento 2 · v1.1.0
│   ├── 1.3.1 Análisis, diseño y contrato de expedientes
│   ├── 1.3.2 Catálogo de trámites
│   ├── 1.3.3 Solicitudes del estudiante
│   ├── 1.3.4 Gestión por funcionarios
│   ├── 1.3.5 Integración con expedientes
│   ├── 1.3.6 Pruebas, regresión I1+I2 y UAT
│   └── 1.3.7 Release v1.1.0, capacitación y demostración
├── 1.4 Incremento 3 · v1.2.0
│   ├── 1.4.1 Análisis, diseño y prueba de concepto de la pasarela
│   ├── 1.4.2 Estado de cuenta y pagos
│   ├── 1.4.3 Notificaciones
│   ├── 1.4.4 Reportes
│   ├── 1.4.5 Pruebas, regresión I1+I2+I3 y UAT
│   └── 1.4.6 Release v1.2.0, capacitación y demostración
└── 1.5 Transición y cierre
    ├── 1.5.1 Manuales de usuario y de operación
    ├── 1.5.2 Traspaso a la Dirección TIC
    └── 1.5.3 Informe y acta de cierre
```

## Diccionario de los paquetes de trabajo

| Código | Paquete | Resultado verificable | Depende de | Criterio de aceptación |
|---|---|---|---|---|
| 1.0 | Gestión del proyecto | Plan integrado, línea base, informes semanales, RCA y registro de decisiones | — | Informe semanal publicado; RCA y pronóstico actualizados |
| 1.1.1 – 1.1.3 | Plataforma base y contratos de interfaz de I1 | ADR-001 a ADR-003, cuatro ambientes, pipeline y contratos firmados | D-02, D-03 | Despliegue automatizado a los cuatro ambientes (HI-0) e inicio de sesión real en QA (HI-1) |
| 1.2.1 | Análisis y diseño de I1 | Especificación de F1.01–F1.13 y prototipos de pantalla | 1.1.1 | Validado por el PO |
| 1.2.2 – 1.2.4 | Identidad, perfil y consultas | Funciones F1.01–F1.11 | 1.1.2, 1.1.3 | DoD cumplida por función; pruebas automatizadas en verde |
| 1.2.5 – 1.2.6 | Pruebas, regresión, UAT y release v1.0.0 | Informe de pruebas, acta de UAT, etiqueta y notas de versión | 1.2.2 – 1.2.4 | Criterio de aceptación de I1 y despliegue sin rollback (H1) |
| 1.3.1 | Análisis, diseño y contrato de expedientes | Especificación de F2.xx y contrato firmado | 1.2.1, D-05 | Validado por el PO y Mesa de Entrada |
| 1.3.2 – 1.3.5 | Catálogo, solicitudes, gestión e integración con expedientes | Funciones F2.01–F2.13 | 1.3.1, 1.2.3 | DoD por función; expedientes integrado en QA (HI-2) |
| 1.3.6 – 1.3.7 | Pruebas, regresión I1+I2, UAT y release v1.1.0 | Acta de UAT, etiqueta y capacitación | 1.3.2 – 1.3.5 | Criterio de aceptación de I2 (H2) |
| 1.4.1 | Análisis, diseño y PoC de la pasarela | Especificación de F3.xx, PoC y contratos | D-06, D-07 | Flujo de pago completo en el entorno de pruebas |
| 1.4.2 – 1.4.4 | Pagos, notificaciones y reportes | Funciones F3.01–F3.15 | 1.4.1, 1.3.3 | Pasarela (HI-3) y correo (HI-4) integrados |
| 1.4.5 – 1.4.6 | Pruebas, regresión completa, UAT y release v1.2.0 | Acta de UAT, etiqueta y capacitación | 1.4.2 – 1.4.4 | Criterio de aceptación de I3 (H3) |
| 1.5 | Transición y cierre | Manual de operación, traspaso y informe de cierre | 1.4.6 | Acta de aceptación final firmada por el Sponsor |
