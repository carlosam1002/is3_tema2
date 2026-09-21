"""Estimacion reproducible - TP2 Enfoque Incremental - Portal de Servicios Estudiantiles.

Tecnica: Puntos de Funcion no ajustados (IFPUG simplificado, complejidad media)
         + productividad en tres puntos (PERT) + capacidad semanal del equipo.

Esfuerzo_i = (PF_i + f_reg * PF_acumulado_entregado_previo) * Productividad + Base_i
PERT       = (O + 4M + P) / 6        sigma = (P - O) / 6
Duracion   = Esfuerzo_PERT / Capacidad_semanal
Costo      = Esfuerzo_PERT * tarifa + infraestructura_semanal * duracion

Ejecutar:  python3 tools/estimacion.py
"""
import math

PESOS = {"EI": 4, "EO": 5, "EQ": 4, "ILF": 10, "EIF": 7}

# (incremento, codigo, funcion, tipo, prioridad MoSCoW)
FUNCIONES = [
    # ---------------- I1: autenticacion, perfil y consultas
    ("I1", "F1.01", "Iniciar/cerrar sesion con SSO institucional", "EI", "M"),
    ("I1", "F1.02", "Consultar perfil del estudiante", "EQ", "M"),
    ("I1", "F1.03", "Actualizar datos de contacto", "EI", "M"),
    ("I1", "F1.04", "Consultar calificaciones", "EQ", "M"),
    ("I1", "F1.05", "Consultar horario de clases", "EQ", "M"),
    ("I1", "F1.06", "Consultar historial y avance de malla", "EQ", "M"),
    ("I1", "F1.07", "Consultar estado de inscripcion", "EQ", "M"),
    ("I1", "F1.08", "Datos de perfil y preferencias (archivo interno)", "ILF", "M"),
    ("I1", "F1.09", "Registro de auditoria de accesos (archivo interno)", "ILF", "M"),
    ("I1", "F1.10", "Sistema academico institucional (archivo externo)", "EIF", "M"),
    ("I1", "F1.11", "Directorio institucional / SSO (archivo externo)", "EIF", "M"),
    ("I1", "F1.12", "Gestionar preferencias del usuario", "EI", "S"),
    ("I1", "F1.13", "Descargar historial academico en PDF (no oficial)", "EO", "S"),
    # ---------------- I2: solicitudes y seguimiento
    ("I2", "F2.01", "Consultar catalogo de tramites", "EQ", "M"),
    ("I2", "F2.02", "Crear solicitud de tramite", "EI", "M"),
    ("I2", "F2.03", "Adjuntar documentos a la solicitud", "EI", "M"),
    ("I2", "F2.04", "Consultar mis solicitudes", "EQ", "M"),
    ("I2", "F2.05", "Ver detalle y linea de tiempo de la solicitud", "EQ", "M"),
    ("I2", "F2.06", "Cambiar estado / derivar solicitud (funcionario)", "EI", "M"),
    ("I2", "F2.07", "Registrar observacion o respuesta (funcionario)", "EI", "M"),
    ("I2", "F2.08", "Solicitudes (archivo interno)", "ILF", "M"),
    ("I2", "F2.09", "Adjuntos (archivo interno)", "ILF", "M"),
    ("I2", "F2.10", "Catalogo de tramites y flujos (archivo interno)", "ILF", "M"),
    ("I2", "F2.11", "Sistema de expedientes / mesa de entrada (archivo externo)", "EIF", "M"),
    ("I2", "F2.12", "Emitir comprobante de solicitud en PDF", "EO", "S"),
    ("I2", "F2.13", "Bandeja del funcionario con control de plazos (SLA)", "EO", "S"),
    ("I2", "F2.14", "Cancelar solicitud", "EI", "C"),
    # ---------------- I3: pagos, notificaciones y reportes
    ("I3", "F3.01", "Consultar estado de cuenta (aranceles)", "EQ", "M"),
    ("I3", "F3.02", "Iniciar pago en linea", "EI", "M"),
    ("I3", "F3.03", "Confirmar pago (callback de la pasarela)", "EI", "M"),
    ("I3", "F3.04", "Emitir comprobante de pago", "EO", "M"),
    ("I3", "F3.05", "Consultar historial de pagos", "EQ", "M"),
    ("I3", "F3.06", "Enviar notificaciones por correo", "EO", "M"),
    ("I3", "F3.07", "Transacciones de pago (archivo interno)", "ILF", "M"),
    ("I3", "F3.08", "Notificaciones (archivo interno)", "ILF", "M"),
    ("I3", "F3.09", "Pasarela de pagos (archivo externo)", "EIF", "M"),
    ("I3", "F3.10", "Proveedor de notificaciones (archivo externo)", "EIF", "M"),
    ("I3", "F3.11", "Sistema arancelario / financiero (archivo externo)", "EIF", "M"),
    ("I3", "F3.12", "Configurar preferencias de notificacion", "EI", "S"),
    ("I3", "F3.13", "Bandeja de notificaciones en el portal", "EQ", "S"),
    ("I3", "F3.14", "Reporte de tramites por estado y tiempos", "EO", "S"),
    ("I3", "F3.15", "Reporte de recaudacion", "EO", "S"),
    ("I3", "F3.16", "Reporte de uso del portal", "EO", "C"),
]

# ---------------- Supuestos de la linea base (plan original)
PROD = {"O": 6.0, "M": 8.0, "P": 12.0}   # horas por PF (todo el ciclo del incremento)
F_REG = 0.10                              # integracion/regresion: 10% del PF acumulado previo
BASE = {"I1": 120.0, "I2": 0.0, "I3": 0.0}  # plataforma base (arquitectura, ambientes, pipeline)
CAPACIDAD = 120.0                         # h efectivas/semana (6 personas x 25 h x 0,80)
TARIFA = 75_000                           # Gs por hora (costo cargado promedio, supuesto)
INFRA_SEM = 600_000                       # Gs por semana (ambientes y herramientas, supuesto)

# ---------------- Datos reales (simulados) de I1 y parametros recalibrados
REAL_I1 = {"pf_entregados": 62, "horas_base": 150.0, "horas_construccion": 540.0,
           "semanas": 6, "capacidad_real": 115.0}
PROD_RECAL = {"O": 7.0, "M": 8.7, "P": 11.0}


def pf(inc, prios=("M", "S", "C"), excluir=(), incluir=()):
    total = sum(PESOS[t] for i, c, _, t, p in FUNCIONES if i == inc and p in prios and c not in excluir)
    total += sum(PESOS[t] for i, c, _, t, p in FUNCIONES if c in incluir)
    return total


def conteo(inc):
    res = {k: 0 for k in PESOS}
    for i, _, _, t, _ in FUNCIONES:
        if i == inc:
            res[t] += 1
    return res


def pert(pf_ef, base, prod):
    o, m, p = (pf_ef * prod[k] + base for k in ("O", "M", "P"))
    e = (o + 4 * m + p) / 6
    s = (p - o) / 6
    return o, m, p, e, s


def fila(nombre, pf_nuevo, pf_prev, base, prod, cap):
    pf_ef = pf_nuevo + F_REG * pf_prev
    o, m, p, e, s = pert(pf_ef, base, prod)
    sem = e / cap
    costo = e * TARIFA + INFRA_SEM * sem
    return dict(inc=nombre, pf=pf_nuevo, reg=F_REG * pf_prev, pf_ef=pf_ef, base=base,
                O=o, M=m, P=p, E=e, S=s, P84=e + s, sem=sem, sem84=(e + s) / cap, costo=costo)


def imprimir(titulo, filas, cap):
    print(f"\n=== {titulo} (capacidad {cap} h/sem) ===")
    print(f"{'Inc':4}{'PF':>5}{'Reg':>6}{'PFef':>7}{'Base':>6}{'O':>8}{'M':>8}{'P':>8}{'PERT':>8}{'sigma':>7}{'P84':>8}{'sem':>6}{'sem84':>6}{'Costo MGs':>11}")
    for f in filas:
        print(f"{f['inc']:4}{f['pf']:>5}{f['reg']:>6.1f}{f['pf_ef']:>7.1f}{f['base']:>6.0f}{f['O']:>8.1f}{f['M']:>8.1f}{f['P']:>8.1f}"
              f"{f['E']:>8.1f}{f['S']:>7.1f}{f['P84']:>8.1f}{f['sem']:>6.2f}{f['sem84']:>6.2f}{f['costo']/1e6:>11.1f}")
    te = sum(f["E"] for f in filas)
    ts = math.sqrt(sum(f["S"] ** 2 for f in filas))
    tc = sum(f["costo"] for f in filas)
    print(f"TOTAL PERT={te:.1f} h  sigma_proyecto={ts:.1f} h  P84={te+ts:.1f} h  semanas={te/cap:.2f}  costo={tc/1e6:.1f} MGs"
          f"  reserva(1 sigma)={ts*TARIFA/1e6:.1f} MGs")
    return te, ts, tc


if __name__ == "__main__":
    for inc in ("I1", "I2", "I3"):
        print(inc, conteo(inc), "PF total", pf(inc), "Must", pf(inc, ("M",)), "Should", pf(inc, ("S",)), "Could", pf(inc, ("C",)))

    # Linea base original (alcance completo)
    lb = [fila("I1", pf("I1"), 0, BASE["I1"], PROD, CAPACIDAD),
          fila("I2", pf("I2"), pf("I1"), 0, PROD, CAPACIDAD),
          fila("I3", pf("I3"), pf("I1") + pf("I2"), 0, PROD, CAPACIDAD)]
    imprimir("LINEA BASE ORIGINAL", lb, CAPACIDAD)
    # Nucleo comprometido de I1 (solo Must)
    imprimir("I1 NUCLEO COMPROMETIDO (Must)", [fila("I1-M", pf("I1", ("M",)), 0, BASE["I1"], PROD, CAPACIDAD)], CAPACIDAD)

    # Real I1
    prod_real = REAL_I1["horas_construccion"] / REAL_I1["pf_entregados"]
    total_real = REAL_I1["horas_base"] + REAL_I1["horas_construccion"]
    print(f"\nI1 real: PF={REAL_I1['pf_entregados']} prod={prod_real:.2f} h/PF total={total_real} h "
          f"capacidad real={total_real/REAL_I1['semanas']:.1f} h/sem")

    cap2 = REAL_I1["capacidad_real"]
    # Recalibracion sin aplicar regla (I2 recibe los 9 PF Should movidos de I1)
    i2_sin = fila("I2", pf("I2") + pf("I1", ("S",)), 62, 0, PROD_RECAL, cap2)
    i3_sin = fila("I3", pf("I3"), 62 + pf("I2") + pf("I1", ("S",)), 0, PROD_RECAL, cap2)
    imprimir("RECALIBRADO SIN REGLA", [i2_sin, i3_sin], cap2)
    # Aplicando regla: F2.14 (Could, 4 PF) pasa a I3; F3.16 (Could, 5 PF) pasa a v1.3.0
    pf_i2 = pf("I2", excluir=("F2.14",)) + pf("I1", ("S",))
    pf_i3 = pf("I3", excluir=("F3.16",), incluir=("F2.14",))
    i2 = fila("I2", pf_i2, 62, 0, PROD_RECAL, cap2)
    i3 = fila("I3", pf_i3, 62 + pf_i2, 0, PROD_RECAL, cap2)
    imprimir("RECALIBRADO CON REGLA R-MA", [i2, i3], cap2)
    print(f"Capacidad I2 7 sem = {7*cap2} h ; I3 8 sem = {8*cap2} h")
    v13 = fila("v1.3", 5, 0, 0, PROD_RECAL, cap2)
    print(f"v1.3.0 reporte de uso: PERT={v13['E']:.1f} h sem={v13['sem']:.2f}")
    # incertidumbre relativa
    for a, b in ((lb[1], i2), (lb[2], i3)):
        print(f"{a['inc']}: sigma/PERT original={a['S']/a['E']*100:.1f}%  recalibrado={b['S']/b['E']*100:.1f}%")
    costo_total_recal = (total_real * TARIFA + INFRA_SEM * 6) + i2["costo"] + i3["costo"]
    print(f"Costo total recalibrado (I1 real + I2 + I3) = {costo_total_recal/1e6:.1f} MGs")
