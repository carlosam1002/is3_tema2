# Registro de cambios de alcance (RCA)

Regla R-MA (resumen): solo se mueve alcance *Should* o *Could*; se mueve primero lo
de menor prioridad y valor; cada ítem se mueve automáticamente una sola vez; todo
movimiento se registra aquí con causa, impacto y aprobación, y se informa en la
demostración del incremento. Mover alcance no oculta retrasos: si cambia la fecha
de un hito, se reporta como desvío.

| ID | Semana | Ítem | PF | De → A | Causa | Impacto | Aprobó |
|---|---|---|---|---|---|---|---|
| RCA-01 | S5 (congelamiento I1) | F1.12 Preferencias; F1.13 Historial en PDF | 9 | I1 → I2 | La plataforma base insumió 150 h frente a 120 h previstas (integración SSO) | I1 entrega 62 de 71 PF; H1 se mantiene en S6 | PO |
| RCA-02 | S6 (recalibración) | F2.14 Cancelar solicitud | 4 | I2 → I3 | El pronóstico recalibrado de I2 (829 h) supera la capacidad de 7 semanas (805 h) | I2 queda en 84 PF; H2 se reporta en S13 (+1 semana) | PO |
| RCA-03 | S6 (recalibración) | F3.16 Reporte de uso del portal | 5 | I3 → v1.3.0 | El pronóstico recalibrado de I3 supera 8 semanas | H3 se reporta en S21 (+1 semana); v1.3.0 en S22 | PO + Comité |
| RCA-04 | S7 (evento de cambio) | F3.13 Bandeja de notificaciones en el portal | 4 | I3 → v1.3.0 | El adaptador al correo institucional agrega 3 PF a I3 y la ventana de 8 semanas no admite ambos | I3 queda en 88 PF y 902,9 h (7,85 semanas); v1.3.0 pasa a 9 PF | PO |
