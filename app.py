"""
╔══════════════════════════════════════════════════════════════════════╗
║      GEMELO DIGITAL – LÍNEA DE PRODUCCIÓN DE 3 ESTACIONES            ║
║      Mini Reto III | Simulación, Análisis y Diseño                   ║
║      Motor: GLC propio + SimPy + Transformada Inversa Exponencial    ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import simpy
import math
import pandas as pd
import numpy as np
import scipy.stats as st_stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ══════════════════════════════════════════════════════════════════════
# 0. CONFIGURACIÓN DE PÁGINA (debe ser el PRIMER comando de Streamlit)
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Gemelo Digital | Mini Reto III",
    layout="wide",
    page_icon="🏭",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
# 0b. CSS PERSONALIZADO – Tema Claro / Simple / Académico
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fuentes ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans:wght@300;400;600&display=swap');

/* ── Variables de color (TEMA CLARO) ─────────────────────────────── */
:root {
    --bg-deep:      #f4f6f8;
    --bg-card:      #ffffff;
    --bg-card2:     #ffffff;
    --accent-blue:  #0969da;
    --accent-amber: #b05c0f;
    --accent-green: #1a7f37;
    --accent-red:   #d1242f;
    --text-main:    #24292f;
    --text-dim:     #57606a;
    --border:       #d0d7de;
    --border-glow:  rgba(9,105,218,0.25);
}

/* ── Fondo global ────────────────────────────────────────────────── */
.stApp { background-color: var(--bg-deep); }
section[data-testid="stSidebar"] { background-color: var(--bg-card); border-right: 1px solid var(--border); }

/* ── Tipografía global ───────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Noto Sans', sans-serif; color: var(--text-main); }
h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 0.04em; }
code, pre, .stCode { font-family: 'IBM Plex Mono', monospace !important; color: var(--text-main) !important;}

/* ── Títulos de pestañas ─────────────────────────────────────────── */
.stTabs [role="tab"] {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: var(--text-dim);
    border-bottom: 2px solid transparent;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}

/* ── Tarjetas métricas ───────────────────────────────────────────── */
.metric-card {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    margin: 0.3rem 0;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-card:hover { border-color: var(--border-glow); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent-blue);
    border-radius: 2px 0 0 2px;
}
.metric-card.amber::before { background: var(--accent-amber); }
.metric-card.green::before { background: var(--accent-green); }
.metric-card.red::before   { background: var(--accent-red);   }

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.25rem;
}
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-main);
    line-height: 1.1;
}
.metric-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
    margin-top: 0.2rem;
}
.metric-delta-pos { color: var(--accent-green); font-weight: 600; }
.metric-delta-neg { color: var(--accent-red);   font-weight: 600; }

/* ── Sección de resultados estadísticos ──────────────────────────── */
.stat-box {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin: 0.4rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.stat-box.success { border-left: 4px solid var(--accent-green); }
.stat-box.error   { border-left: 4px solid var(--accent-red);   }
.stat-box.info    { border-left: 4px solid var(--accent-blue);  }

/* ── Header de sección ───────────────────────────────────────────── */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: var(--accent-blue);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin: 1.2rem 0 0.8rem 0;
}

/* ── Botón principal ─────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0969da 0%, #0353a4 100%) !important;
    color: white !important;
    border: none !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── Sidebar – Textos legibles en modo claro ────────────── */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: #24292f !important;
}
/* Títulos del sidebar */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .section-header {
    color: #0969da !important;
}
/* Labels de inputs y sliders */
section[data-testid="stSidebar"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #57606a !important;
}
/* Valor actual del slider */
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
    color: #57606a !important;
}
/* Input numérico – texto dentro del campo */
section[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #24292f !important;
    border: 1px solid #d0d7de !important;
    border-radius: 6px !important;
}
/* Checkbox */
section[data-testid="stSidebar"] .stCheckbox label {
    color: #24292f !important;
    font-size: 0.85rem !important;
}
/* Número al lado del slider */
section[data-testid="stSidebar"] .stSlider span {
    color: #0969da !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
/* Expander */
section[data-testid="stSidebar"] details summary {
    color: #57606a !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}
/* Divider */
section[data-testid="stSidebar"] hr { border-color: #d0d7de !important; }

/* ── Tabla de datos ──────────────────────────────────────────────── */
.stDataFrame { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; }

/* ── Spinner ─────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--accent-blue) !important; }

/* ── Badge de estado ─────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    margin-left: 0.5rem;
}
.badge-blue  { background: rgba(9,105,218,0.15); color: var(--accent-blue);  border: 1px solid rgba(9,105,218,0.3); }
.badge-amber { background: rgba(176,92,15,0.15); color: var(--accent-amber); border: 1px solid rgba(176,92,15,0.3); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# 1. MOTOR MATEMÁTICO – GLC + Transformada Inversa Exponencial
# ══════════════════════════════════════════════════════════════════════
class GeneradorCongruencialLineal:
    """
    Generador Congruencial Lineal (GLC) – Parámetros de Numerical Recipes.
    Ecuación de recurrencia:  X_{n+1} = (a · X_n + c) mod m
    Parámetros:
        m = 2^32  (módulo, potencia de 2 → facilita operaciones bit a bit)
        a = 1664525  (multiplicador, satisface criterio de Hull-Dobell)
        c = 1013904223  (incremento, coprimo con m)
    Periodo completo: m = 4,294,967,296 (Hull-Dobell garantizado)
    """
    def __init__(self, semilla: int):
        self.X = int(semilla) & 0xFFFFFFFF  # Asegurar rango [0, 2^32)
        self.m = 2**32
        self.a = 1664525
        self.c = 1013904223
        self._contador = 0

    def uniforme(self) -> float:
        """Genera U ∈ [0,1) usando GLC puro."""
        self.X = (self.a * self.X + self.c) % self.m
        self._contador += 1
        return self.X / self.m

    def exponencial(self, media: float) -> float:
        """
        Transformada Inversa para distribución Exponencial:
            X = -media · ln(1 - U),  U ~ Uniforme(0,1)
        Se evitan U = 0 y U = 1 para estabilidad numérica.
        """
        U = self.uniforme()
        while U == 0.0 or U == 1.0:          # Garantía numérica
            U = self.uniforme()
        return -media * math.log(1.0 - U)

    def generar_secuencia_uniforme(self, n: int) -> list:
        """Genera una lista de n números U ~ Uniforme(0,1)."""
        return [self.uniforme() for _ in range(n)]


# ══════════════════════════════════════════════════════════════════════
# 2. ENTIDADES Y PROCESOS DE SIMULACIÓN (SimPy)
# ══════════════════════════════════════════════════════════════════════
class Pieza:
    """Entidad que fluye por el sistema; registra tiempos clave."""
    def __init__(self, id_pieza: int, t_inicio: float):
        self.id          = id_pieza
        self.t_inicio    = t_inicio      # Entrada al sistema (inicio proceso E1)
        self.t_fin_e1    = None
        self.t_fin_e2    = None
        self.t_fin_e3    = None          # Salida del sistema
        self.t_bloqueo_e1 = 0.0          # Tiempo acumulado de bloqueo en E1
        self.t_bloqueo_e2 = 0.0
        self.t_espera_b1  = 0.0          # Tiempo en buffer B1 (hambre para E2)
        self.t_espera_b2  = 0.0


def proceso_estacion_1(env, buffer1, rng, media, stats, sim_time):
    """
    Estación 1: genera piezas con tiempo exponencial.
    Bloqueo: si B1 está lleno al terminar, espera hasta que haya espacio.
    """
    id_pieza = 0
    while env.now < sim_time:
        id_pieza += 1
        t_entrada = env.now
        pieza = Pieza(id_pieza, t_entrada)

        # Procesar pieza (tiempo exponencial propio)
        yield env.timeout(rng.exponencial(media))
        pieza.t_fin_e1 = env.now

        # ─── BLOQUEO: intentar poner en B1 ──────────────────────────
        t_bloqueo_ini = env.now
        yield buffer1.put(pieza)
        duracion_bloqueo = env.now - t_bloqueo_ini
        pieza.t_bloqueo_e1 = duracion_bloqueo
        stats['E1_bloqueado'] += duracion_bloqueo
        stats['eventos_bloqueo_E1'].append((t_bloqueo_ini, env.now))


def proceso_estacion_2(env, buffer1, buffer2, rng, media, stats, sim_time):
    """
    Estación 2: toma de B1, procesa, deja en B2.
    Hambre: si B1 vacío, espera.
    Bloqueo: si B2 lleno al terminar, espera.
    """
    while True:
        # ─── HAMBRE: esperar pieza en B1 ────────────────────────────
        t_hambre_ini = env.now
        pieza = yield buffer1.get()
        duracion_hambre = env.now - t_hambre_ini
        stats['E2_hambre']    += duracion_hambre
        pieza.t_espera_b1      = duracion_hambre

        # Procesar
        yield env.timeout(rng.exponencial(media))
        pieza.t_fin_e2 = env.now

        # ─── BLOQUEO: intentar poner en B2 ──────────────────────────
        t_bloqueo_ini = env.now
        yield buffer2.put(pieza)
        duracion_bloqueo = env.now - t_bloqueo_ini
        pieza.t_bloqueo_e2 = duracion_bloqueo
        stats['E2_bloqueado'] += duracion_bloqueo
        stats['eventos_bloqueo_E2'].append((t_bloqueo_ini, env.now))


def proceso_estacion_3(env, buffer2, rng, media, stats):
    """
    Estación 3: toma de B2, procesa, pieza sale del sistema.
    Hambre: si B2 vacío, espera.
    """
    while True:
        # ─── HAMBRE: esperar pieza en B2 ────────────────────────────
        t_hambre_ini = env.now
        pieza = yield buffer2.get()
        duracion_hambre = env.now - t_hambre_ini
        stats['E3_hambre']   += duracion_hambre
        pieza.t_espera_b2     = duracion_hambre

        # Procesar
        yield env.timeout(rng.exponencial(media))
        pieza.t_fin_e3 = env.now

        # Registrar pieza completada
        stats['piezas_completadas'].append(pieza)


def rastreador_wip(env, buffer1, buffer2, stats, intervalo=1.0):
    """Registra el WIP (B1+B2) cada `intervalo` minutos."""
    while True:
        wip_actual = len(buffer1.items) + len(buffer2.items)
        stats['wip_historia'].append((env.now, wip_actual, len(buffer1.items), len(buffer2.items)))
        yield env.timeout(intervalo)


# ══════════════════════════════════════════════════════════════════════
# 3. FUNCIÓN PRINCIPAL DE SIMULACIÓN
# ══════════════════════════════════════════════════════════════════════
def ejecutar_simulacion(semilla: int, k1: int, k2: int,
                        tiempo_sim: float, media: float = 4.0) -> dict:
    """
    Ejecuta UNA réplica de simulación.
    Retorna diccionario completo de métricas y datos crudos.
    """
    env  = simpy.Environment()
    rng  = GeneradorCongruencialLineal(semilla)
    b1   = simpy.Store(env, capacity=k1)
    b2   = simpy.Store(env, capacity=k2)

    stats = {
        'E1_bloqueado': 0.0,
        'E2_bloqueado': 0.0,
        'E2_hambre':    0.0,
        'E3_hambre':    0.0,
        'piezas_completadas': [],
        'wip_historia':       [],
        'eventos_bloqueo_E1': [],
        'eventos_bloqueo_E2': [],
    }

    env.process(proceso_estacion_1(env, b1, rng, media, stats, tiempo_sim))
    env.process(proceso_estacion_2(env, b1, b2, rng, media, stats, tiempo_sim))
    env.process(proceso_estacion_3(env, b2, rng, media, stats))
    env.process(rastreador_wip(env, b1, b2, stats))

    env.run(until=tiempo_sim)

    # ── Cálculos derivados ──────────────────────────────────────────
    completadas   = len(stats['piezas_completadas'])
    throughput_hr = (completadas / tiempo_sim) * 60 if tiempo_sim > 0 else 0

    tiempos_flujo = [p.t_fin_e3 - p.t_inicio
                     for p in stats['piezas_completadas']]
    tiempo_flujo_prom = float(np.mean(tiempos_flujo)) if tiempos_flujo else 0.0

    wip_vals = [w for _, w, _, _ in stats['wip_historia']]
    b1_vals  = [b1v for _, _, b1v, _ in stats['wip_historia']]
    b2_vals  = [b2v for _, _, _, b2v in stats['wip_historia']]
    wip_prom = float(np.mean(wip_vals)) if wip_vals else 0.0

    # Bloqueo/hambre como % del tiempo total
    e1_bloq_pct = (stats['E1_bloqueado'] / tiempo_sim) * 100
    e2_bloq_pct = (stats['E2_bloqueado'] / tiempo_sim) * 100
    e2_hamb_pct = (stats['E2_hambre']    / tiempo_sim) * 100
    e3_hamb_pct = (stats['E3_hambre']    / tiempo_sim) * 100

    return {
        'throughput_hr':    throughput_hr,
        'tiempo_flujo':     tiempo_flujo_prom,
        'wip_prom':         wip_prom,
        'E1_bloq_pct':      e1_bloq_pct,
        'E2_bloq_pct':      e2_bloq_pct,
        'E2_hamb_pct':      e2_hamb_pct,
        'E3_hamb_pct':      e3_hamb_pct,
        'n_completadas':    completadas,
        'tiempos_flujo_raw': tiempos_flujo,
        'wip_historia_raw':  stats['wip_historia'],
        'b1_historia':       b1_vals,
        'b2_historia':       b2_vals,
        'piezas':            stats['piezas_completadas'],
    }


# ══════════════════════════════════════════════════════════════════════
# 4. FUNCIONES ESTADÍSTICAS
# ══════════════════════════════════════════════════════════════════════
def intervalo_confianza(datos: list, alpha: float = 0.05) -> tuple:
    """Retorna (media, margen_error) con IC (1-alpha)%."""
    n    = len(datos)
    if n < 2:
        return float(np.mean(datos)) if datos else 0.0, 0.0
    media = float(np.mean(datos))
    se    = st_stats.sem(datos)
    t_crit = st_stats.t.ppf(1 - alpha / 2, df=n - 1)
    margen = t_crit * se
    return media, margen


def prueba_uniformidad_chi2(datos_u: list, k: int = 10) -> dict:
    """
    Prueba Chi-cuadrado de uniformidad para los números U del GLC.
    H0: los números siguen U(0,1).
    """
    n          = len(datos_u)
    observados, bordes = np.histogram(datos_u, bins=k, range=(0, 1))
    esperados  = np.full(k, n / k)
    chi2_stat  = float(np.sum((observados - esperados)**2 / esperados))
    gl         = k - 1
    p_valor    = float(1 - st_stats.chi2.cdf(chi2_stat, df=gl))
    chi2_crit  = float(st_stats.chi2.ppf(0.95, df=gl))
    return {
        'chi2_stat': chi2_stat,
        'chi2_crit': chi2_crit,
        'gl':        gl,
        'p_valor':   p_valor,
        'rechaza':   chi2_stat > chi2_crit,
        'observados': observados.tolist(),
        'esperados':  esperados.tolist(),
        'bordes':     bordes.tolist(),
    }


# ══════════════════════════════════════════════════════════════════════
# 5. HELPERS DE VISUALIZACIÓN (Plotly Tema Claro)
# ══════════════════════════════════════════════════════════════════════
_PLOTLY_BASE = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',
    font=dict(family='IBM Plex Mono, monospace', color='#57606a', size=11),
    xaxis=dict(gridcolor='#e1e4e8', linecolor='#d0d7de', zerolinecolor='#e1e4e8'),
    yaxis=dict(gridcolor='#e1e4e8', linecolor='#d0d7de', zerolinecolor='#e1e4e8'),
    legend=dict(bgcolor='rgba(255,255,255,0.8)', bordercolor='#d0d7de',
                borderwidth=1, font=dict(size=11)),
    margin=dict(t=55, b=40, l=50, r=20),
)

def apply_layout(fig, title: str = '', height: int = None, extra: dict = None):
    """Aplica el tema claro a una figura Plotly sin duplicar keywords."""
    kw = dict(**_PLOTLY_BASE)
    if title:
        kw['title'] = dict(
            text=title,
            font=dict(family='Rajdhani, sans-serif', color='#24292f', size=16)
        )
    if height:
        kw['height'] = height
    if extra:
        kw.update(extra)
    fig.update_layout(**kw)

COLOR_A     = '#0969da'
COLOR_B     = '#b05c0f'
COLOR_GREEN = '#1a7f37'
COLOR_RED   = '#d1242f'


def card_metrica(label: str, valor: str, sub: str = '', acento: str = 'blue',
                 delta: str = '', delta_positivo: bool = True) -> str:
    delta_html = ''
    if delta:
        cls  = 'metric-delta-pos' if delta_positivo else 'metric-delta-neg'
        sign = '▲' if delta_positivo else '▼'
        delta_html = f'<div class="{cls}">{sign} {delta}</div>'
    return f"""
    <div class="metric-card {acento}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{valor}</div>
        <div class="metric-sub">{sub}</div>
        {delta_html}
    </div>"""


# ══════════════════════════════════════════════════════════════════════
# 6. SIDEBAR – PANEL DE CONTROL
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1rem 0;'>
        <span style='font-family: Rajdhani, sans-serif; font-size: 1.6rem;
                     font-weight: 700; color: #0969da; letter-spacing: 0.1em;'>
            🏭 GEMELO DIGITAL
        </span><br>
        <span style='font-family: IBM Plex Mono, monospace; font-size: 0.72rem;
                     color: #57606a;'>LÍNEA DE 3 ESTACIONES</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">⚙️ PARÁMETROS GLOBALES</div>', unsafe_allow_html=True)
    semilla    = st.number_input("Semilla GLC (X₀)", value=12345, step=1, min_value=1,
                                 help="Valor inicial del Generador Congruencial Lineal")
    tiempo_sim = st.number_input("Horizonte de simulación (min)", min_value=500,
                                 value=960, step=60,
                                 help="960 min = 16 horas (recomendado para estabilidad)")
    num_replicas = st.slider("Réplicas por escenario", min_value=2, max_value=20, value=10,
                             help="Más réplicas → IC más preciso")
    media_proceso = st.number_input("Media de proceso (min/pieza)", value=4.0,
                                    min_value=1.0, max_value=20.0, step=0.5,
                                    help="Media exponencial λ=1/media")

    st.markdown('<div class="section-header">🔵 ESCENARIO A (BASE)</div>', unsafe_allow_html=True)
    k1_a = st.slider("Capacidad B1 (K1) – Escenario A", 1, 10, 3,
                     help="Piezas máximas en espera antes de E2")
    k2_a = st.slider("Capacidad B2 (K2) – Escenario A", 1, 10, 3,
                     help="Piezas máximas en espera antes de E3")

    st.markdown("---")
    comparar = st.checkbox("⚖️ Comparar con Escenario B", value=True)
    if comparar:
        st.markdown('<div class="section-header">🟠 ESCENARIO B (MEJORA)</div>', unsafe_allow_html=True)
        k1_b = st.slider("Capacidad B1 (K1) – Escenario B", 1, 10, 6)
        k2_b = st.slider("Capacidad B2 (K2) – Escenario B", 1, 10, 6)
    else:
        k1_b, k2_b = k1_a, k2_a

    st.markdown("---")
    # Parámetros avanzados
    with st.expander("🔬 Configuración avanzada"):
        alpha_ic   = st.slider("Nivel de significancia (α)", 0.01, 0.20, 0.05, step=0.01)
        umbral_h0  = st.number_input("Umbral Prueba H₀ (Pz/Hr)", value=12.0, step=0.5,
                                     help="Hipótesis nula: throughput > umbral")
        n_glc_test = st.slider("Números GLC para prueba uniformidad", 100, 2000, 500, step=100)

    st.markdown("---")
    ejecutar = st.button("🚀  INICIAR SIMULACIÓN", type="primary", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# 7. HEADER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='padding: 0.5rem 0 1.5rem 0;'>
    <h1 style='font-family: Rajdhani, sans-serif; font-size: 2.4rem; font-weight: 700;
               color: #24292f; margin: 0; line-height: 1.1;'>
        Simulador Gemelo Digital
        <span style='color: #0969da;'>›</span> Línea de Producción
    </h1>
    <p style='font-family: IBM Plex Mono, monospace; font-size: 0.82rem; color: #57606a;
              margin: 0.3rem 0 0 0;'>
        Motor: GLC propio &nbsp;|&nbsp; Transformada Inversa Exp(λ=0.25) &nbsp;|&nbsp;
        SimPy DES &nbsp;|&nbsp; IC 95% &nbsp;|&nbsp; Mini Reto III · 2026A
    </p>
</div>
""", unsafe_allow_html=True)

# Diagrama esquemático ASCII Tema Claro
st.markdown("""
<div style='background:#ffffff; border:1px solid #d0d7de; border-radius:10px;
            padding:1rem 1.5rem; font-family: IBM Plex Mono, monospace;
            font-size:0.85rem; color:#57606a; margin-bottom:1.5rem;'>
    <span style='color:#0969da; font-weight:600;'>TOPOLOGÍA DEL SISTEMA</span><br><br>
    <span style='color:#1a7f37;'>∞ Materia Prima</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='background:#f6f8fa; color:#24292f; padding:2px 8px; border-radius:4px;
                 border:1px solid #0969da;'>E1</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='background:#f6f8fa; color:#b05c0f; padding:2px 8px; border-radius:4px;
                 border:1px dashed #b05c0f;'>B1(K1)</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='background:#f6f8fa; color:#24292f; padding:2px 8px; border-radius:4px;
                 border:1px solid #0969da;'>E2</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='background:#f6f8fa; color:#b05c0f; padding:2px 8px; border-radius:4px;
                 border:1px dashed #b05c0f;'>B2(K2)</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='background:#f6f8fa; color:#24292f; padding:2px 8px; border-radius:4px;
                 border:1px solid #0969da;'>E3</span>
    <span style='color:#57606a;'> ──▶ </span>
    <span style='color:#1a7f37;'>✓ Salida</span>
    &nbsp;&nbsp;
    <span style='color:#d1242f;'>█ Bloqueo</span>&nbsp;
    <span style='color:#b05c0f;'>░ Hambre</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# 8. LÓGICA PRINCIPAL (al presionar el botón)
# ══════════════════════════════════════════════════════════════════════
if ejecutar:

    barra_progreso = st.progress(0, text="Inicializando motor GLC...")
    tiempo_inicio  = time.time()

    # ── 8.1 Ejecutar réplicas Escenario A ──────────────────────────
    resultados_A = []
    for i in range(num_replicas):
        barra_progreso.progress(
            int((i / (num_replicas * (2 if comparar else 1))) * 100),
            text=f"Escenario A – Réplica {i+1}/{num_replicas}…"
        )
        res = ejecutar_simulacion(semilla + i * 997, k1_a, k2_a,
                                  tiempo_sim, media_proceso)
        resultados_A.append(res)

    df_A = pd.DataFrame([{k: v for k, v in r.items()
                          if not isinstance(v, (list, dict))}
                         for r in resultados_A])

    # ── 8.2 Ejecutar réplicas Escenario B (opcional) ───────────────
    resultados_B = []
    if comparar:
        for i in range(num_replicas):
            barra_progreso.progress(
                int(((num_replicas + i) / (num_replicas * 2)) * 100),
                text=f"Escenario B – Réplica {i+1}/{num_replicas}…"
            )
            res = ejecutar_simulacion(semilla + i * 997, k1_b, k2_b,
                                      tiempo_sim, media_proceso)
            resultados_B.append(res)
        df_B = pd.DataFrame([{k: v for k, v in r.items()
                               if not isinstance(v, (list, dict))}
                              for r in resultados_B])

    barra_progreso.progress(100, text="✅ Simulación completada.")
    tiempo_total = time.time() - tiempo_inicio

    # ── 8.3 IC para métricas clave ─────────────────────────────────
    th_a, th_a_ci   = intervalo_confianza(df_A['throughput_hr'].tolist(), alpha_ic)
    ft_a, ft_a_ci   = intervalo_confianza(df_A['tiempo_flujo'].tolist(),  alpha_ic)
    wip_a           = df_A['wip_prom'].mean()
    if comparar:
        th_b, th_b_ci = intervalo_confianza(df_B['throughput_hr'].tolist(), alpha_ic)
        ft_b, ft_b_ci = intervalo_confianza(df_B['tiempo_flujo'].tolist(),  alpha_ic)
        wip_b         = df_B['wip_prom'].mean()

    # ── 8.4 Prueba de hipótesis t (1 cola) ─────────────────────────
    t_stat_a, p_val_a = st_stats.ttest_1samp(
        df_A['throughput_hr'].tolist(), umbral_h0, alternative='greater')
    if comparar:
        t_stat_b, p_val_b = st_stats.ttest_1samp(
            df_B['throughput_hr'].tolist(), umbral_h0, alternative='greater')

    # ── 8.5 Prueba uniformidad GLC ─────────────────────────────────
    rng_test  = GeneradorCongruencialLineal(semilla)
    nums_u    = rng_test.generar_secuencia_uniforme(n_glc_test)
    chi2_res  = prueba_uniformidad_chi2(nums_u)

    # ══════════════════════════════════════════════════════════════════
    # 9. PESTAÑAS DE RESULTADOS
    # ══════════════════════════════════════════════════════════════════
    tabs = st.tabs([
        "📊 KPIs & Métricas",
        "📈 WIP en el Tiempo",
        "⏱️ Tiempos de Flujo",
        "🚧 Cuellos de Botella",
        "🧪 Estadística & Hipótesis",
        "🎲 Validación GLC",
        "📋 Tabla de Réplicas",
    ])

    # ────────────────────────────────────────────────────────────────
    # TAB 1 – KPIs & MÉTRICAS
    # ────────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown(f"""
        <p style='font-family: IBM Plex Mono, monospace; font-size: 0.78rem; color: #57606a;
                  margin-bottom: 1rem;'>
            ⏱ Tiempo de cómputo: <strong style='color:#0969da;'>{tiempo_total:.2f}s</strong>
            &nbsp;|&nbsp; Réplicas: <strong style='color:#0969da;'>{num_replicas}</strong>
            &nbsp;|&nbsp; Horizonte: <strong style='color:#0969da;'>{tiempo_sim} min</strong>
            &nbsp;|&nbsp; IC: <strong style='color:#0969da;'>{int((1-alpha_ic)*100)}%</strong>
        </p>
        """, unsafe_allow_html=True)

        # ── Throughput ────────────────────────────────────────────
        st.markdown('<div class="section-header">🟢 Throughput (Piezas / Hora)</div>',
                    unsafe_allow_html=True)
        cols_th = st.columns(2 if comparar else 1)
        with cols_th[0]:
            st.markdown(card_metrica(
                f"THROUGHPUT · Escenario A  [K1={k1_a}, K2={k2_a}]",
                f"{th_a:.3f}",
                sub=f"IC {int((1-alpha_ic)*100)}%: [{th_a-th_a_ci:.3f} – {th_a+th_a_ci:.3f}] Pz/Hr",
                acento="blue"
            ), unsafe_allow_html=True)
        if comparar:
            with cols_th[1]:
                delta_th = th_b - th_a
                st.markdown(card_metrica(
                    f"THROUGHPUT · Escenario B  [K1={k1_b}, K2={k2_b}]",
                    f"{th_b:.3f}",
                    sub=f"IC {int((1-alpha_ic)*100)}%: [{th_b-th_b_ci:.3f} – {th_b+th_b_ci:.3f}] Pz/Hr",
                    acento="amber",
                    delta=f"{delta_th:+.3f} Pz/Hr vs A",
                    delta_positivo=delta_th >= 0
                ), unsafe_allow_html=True)

        # ── Tiempo de Flujo ───────────────────────────────────────
        st.markdown('<div class="section-header">🔵 Tiempo Promedio de Flujo (min)</div>',
                    unsafe_allow_html=True)
        cols_ft = st.columns(2 if comparar else 1)
        with cols_ft[0]:
            st.markdown(card_metrica(
                f"TIEMPO FLUJO · Escenario A",
                f"{ft_a:.2f} min",
                sub=f"IC {int((1-alpha_ic)*100)}%: [{ft_a-ft_a_ci:.2f} – {ft_a+ft_a_ci:.2f}]",
                acento="blue"
            ), unsafe_allow_html=True)
        if comparar:
            with cols_ft[1]:
                delta_ft = ft_b - ft_a
                st.markdown(card_metrica(
                    f"TIEMPO FLUJO · Escenario B",
                    f"{ft_b:.2f} min",
                    sub=f"IC {int((1-alpha_ic)*100)}%: [{ft_b-ft_b_ci:.2f} – {ft_b+ft_b_ci:.2f}]",
                    acento="amber",
                    delta=f"{delta_ft:+.2f} min vs A",
                    delta_positivo=delta_ft <= 0
                ), unsafe_allow_html=True)

        # ── WIP & Piezas ──────────────────────────────────────────
        st.markdown('<div class="section-header">📦 WIP & Producción</div>',
                    unsafe_allow_html=True)
        n_cols = 4 if comparar else 2
        cols_wip = st.columns(n_cols)
        with cols_wip[0]:
            st.markdown(card_metrica("WIP PROM – A",
                f"{wip_a:.2f} pz", acento="blue"), unsafe_allow_html=True)
        with cols_wip[1]:
            st.markdown(card_metrica("PIEZAS COMPLETAS – A",
                f"{int(df_A['n_completadas'].mean())}",
                sub=f"por réplica", acento="blue"), unsafe_allow_html=True)
        if comparar:
            with cols_wip[2]:
                delta_wip = wip_b - wip_a
                st.markdown(card_metrica("WIP PROM – B",
                    f"{wip_b:.2f} pz", acento="amber",
                    delta=f"{delta_wip:+.2f} vs A",
                    delta_positivo=delta_wip <= 0), unsafe_allow_html=True)
            with cols_wip[3]:
                st.markdown(card_metrica("PIEZAS COMPLETAS – B",
                    f"{int(df_B['n_completadas'].mean())}",
                    sub=f"por réplica", acento="amber"), unsafe_allow_html=True)

        # ── Gráfico de barras IC para throughput ──────────────────
        st.markdown('<div class="section-header">📊 Comparativa Throughput con IC</div>',
                    unsafe_allow_html=True)
        escenarios  = [f"A [K1={k1_a},K2={k2_a}]"]
        ths_medias  = [th_a]
        ths_errores = [th_a_ci]
        colores_bar = [COLOR_A]
        if comparar:
            escenarios.append(f"B [K1={k1_b},K2={k2_b}]")
            ths_medias.append(th_b)
            ths_errores.append(th_b_ci)
            colores_bar.append(COLOR_B)

        fig_ic = go.Figure()
        fig_ic.add_trace(go.Bar(
            x=escenarios, y=ths_medias,
            error_y=dict(type='data', array=ths_errores, visible=True,
                         color='#24292f', thickness=2, width=10),
            marker_color=colores_bar,
            marker_line=dict(color='#d0d7de', width=1),
            text=[f"{m:.2f}" for m in ths_medias],
            textposition='outside',
            textfont=dict(family='IBM Plex Mono', size=12, color='#24292f'),
        ))
        fig_ic.add_hline(y=umbral_h0, line_dash='dash', line_color=COLOR_RED,
                         annotation_text=f"Umbral H₀: {umbral_h0} Pz/Hr",
                         annotation_font_color=COLOR_RED)
        apply_layout(fig_ic, title=f"Throughput promedio con IC {int((1-alpha_ic)*100)}%",
                     extra=dict(yaxis_title="Piezas / Hora", xaxis_title="Escenario"))
        st.plotly_chart(fig_ic, use_container_width=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 2 – WIP EN EL TIEMPO
    # ────────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="section-header">📈 Evolución del WIP (Inventario en Proceso)</div>',
                    unsafe_allow_html=True)

        replica_sel = st.slider("Réplica a visualizar", 1, num_replicas, 1, key="wip_rep")
        idx = replica_sel - 1

        wip_data_a = pd.DataFrame(
            resultados_A[idx]['wip_historia_raw'],
            columns=['Minuto', 'WIP_Total', 'B1', 'B2']
        )
        wip_data_a['Escenario'] = f'A [K1={k1_a},K2={k2_a}]'

        fig_wip = make_subplots(rows=2, cols=1,
                                shared_xaxes=True,
                                row_heights=[0.65, 0.35],
                                vertical_spacing=0.07)

        # WIP Total
        fig_wip.add_trace(go.Scatter(
            x=wip_data_a['Minuto'], y=wip_data_a['WIP_Total'],
            name=f'WIP Total – A', fill='tozeroy',
            line=dict(color=COLOR_A, width=1.5),
            fillcolor=f'rgba(9,105,218,0.15)'
        ), row=1, col=1)

        # B1 y B2 por separado
        fig_wip.add_trace(go.Scatter(
            x=wip_data_a['Minuto'], y=wip_data_a['B1'],
            name='Buffer B1 – A', line=dict(color=COLOR_GREEN, width=1, dash='dot')
        ), row=2, col=1)
        fig_wip.add_trace(go.Scatter(
            x=wip_data_a['Minuto'], y=wip_data_a['B2'],
            name='Buffer B2 – A', line=dict(color=COLOR_B, width=1, dash='dash')
        ), row=2, col=1)

        if comparar and resultados_B:
            wip_data_b = pd.DataFrame(
                resultados_B[idx]['wip_historia_raw'],
                columns=['Minuto', 'WIP_Total', 'B1', 'B2']
            )
            fig_wip.add_trace(go.Scatter(
                x=wip_data_b['Minuto'], y=wip_data_b['WIP_Total'],
                name=f'WIP Total – B', fill='tozeroy',
                line=dict(color=COLOR_B, width=1.5),
                fillcolor='rgba(176,92,15,0.15)'
            ), row=1, col=1)

        # Líneas de capacidad máxima
        cap_max_a = k1_a + k2_a
        fig_wip.add_hline(y=cap_max_a, line_dash='longdash',
                          line_color='rgba(209,36,47,0.5)',
                          annotation_text=f"Cap. Máx A: {cap_max_a}",
                          annotation_font_color=COLOR_RED, row=1, col=1)
        if comparar:
            cap_max_b = k1_b + k2_b
            if cap_max_b != cap_max_a:
                fig_wip.add_hline(y=cap_max_b, line_dash='longdash',
                                  line_color='rgba(176,92,15,0.5)',
                                  annotation_text=f"Cap. Máx B: {cap_max_b}",
                                  annotation_font_color=COLOR_B, row=1, col=1)

        apply_layout(fig_wip, title=f"WIP en el tiempo – Réplica {replica_sel}", height=500)
        fig_wip.update_yaxes(title_text="WIP (piezas)", row=1, col=1)
        fig_wip.update_yaxes(title_text="Buffer (piezas)", row=2, col=1)
        fig_wip.update_xaxes(title_text="Tiempo (min)", row=2, col=1)
        st.plotly_chart(fig_wip, use_container_width=True)

        # ── Estadísticas de WIP ─────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-box info">
            📦 WIP promedio Escenario A: <strong>{wip_data_a['WIP_Total'].mean():.2f} piezas</strong><br>
            📦 WIP máximo: <strong>{wip_data_a['WIP_Total'].max():.0f}</strong> &nbsp;|&nbsp;
            WIP mínimo: <strong>{wip_data_a['WIP_Total'].min():.0f}</strong><br>
            B1 prom: <strong>{wip_data_a['B1'].mean():.2f}</strong> &nbsp;|&nbsp;
            B2 prom: <strong>{wip_data_a['B2'].mean():.2f}</strong>
            </div>""", unsafe_allow_html=True)
        if comparar and resultados_B:
            with col2:
                st.markdown(f"""
                <div class="stat-box info">
                📦 WIP promedio Escenario B: <strong>{wip_data_b['WIP_Total'].mean():.2f} piezas</strong><br>
                📦 WIP máximo: <strong>{wip_data_b['WIP_Total'].max():.0f}</strong> &nbsp;|&nbsp;
                WIP mínimo: <strong>{wip_data_b['WIP_Total'].min():.0f}</strong><br>
                B1 prom: <strong>{wip_data_b['B1'].mean():.2f}</strong> &nbsp;|&nbsp;
                B2 prom: <strong>{wip_data_b['B2'].mean():.2f}</strong>
                </div>""", unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 3 – HISTOGRAMA DE TIEMPOS DE FLUJO
    # ────────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-header">⏱️ Distribución de Tiempos de Flujo</div>',
                    unsafe_allow_html=True)

        replica_hist = st.slider("Réplica", 1, num_replicas, 1, key="hist_rep")
        n_bins = st.slider("Número de intervalos (bins)", 10, 60, 25, key="hist_bins")

        tf_A = resultados_A[replica_hist - 1]['tiempos_flujo_raw']

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=tf_A, nbinsx=n_bins,
            name=f'A [K1={k1_a},K2={k2_a}]',
            marker_color=COLOR_A,
            marker_line=dict(color='#ffffff', width=0.5),
            opacity=0.75
        ))

        if comparar and resultados_B:
            tf_B = resultados_B[replica_hist - 1]['tiempos_flujo_raw']
            fig_hist.add_trace(go.Histogram(
                x=tf_B, nbinsx=n_bins,
                name=f'B [K1={k1_b},K2={k2_b}]',
                marker_color=COLOR_B,
                marker_line=dict(color='#ffffff', width=0.5),
                opacity=0.65
            ))

        # Líneas de media
        fig_hist.add_vline(x=np.mean(tf_A), line_dash='dash',
                           line_color=COLOR_A,
                           annotation_text=f"μ_A={np.mean(tf_A):.1f}",
                           annotation_font_color=COLOR_A)
        if comparar and resultados_B:
            fig_hist.add_vline(x=np.mean(tf_B), line_dash='dash',
                               line_color=COLOR_B,
                               annotation_text=f"μ_B={np.mean(tf_B):.1f}",
                               annotation_font_color=COLOR_B)

        apply_layout(fig_hist, title=f"Histograma Tiempos de Flujo – Réplica {replica_hist}",
                     extra=dict(barmode='overlay', xaxis_title="Tiempo de Flujo (min)",
                                yaxis_title="Frecuencia"))
        st.plotly_chart(fig_hist, use_container_width=True)

        # Estadísticas descriptivas
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="stat-box info">
            <strong>Escenario A – Estadísticas descriptivas:</strong><br>
            Media: {np.mean(tf_A):.2f} min &nbsp;|&nbsp; Mediana: {np.median(tf_A):.2f} min<br>
            Desv. Est.: {np.std(tf_A):.2f} min &nbsp;|&nbsp; CV: {np.std(tf_A)/np.mean(tf_A):.3f}<br>
            P10: {np.percentile(tf_A,10):.2f} &nbsp;|&nbsp; P90: {np.percentile(tf_A,90):.2f}<br>
            N piezas: {len(tf_A)}
            </div>""", unsafe_allow_html=True)
        if comparar and resultados_B:
            with c2:
                st.markdown(f"""
                <div class="stat-box info">
                <strong>Escenario B – Estadísticas descriptivas:</strong><br>
                Media: {np.mean(tf_B):.2f} min &nbsp;|&nbsp; Mediana: {np.median(tf_B):.2f} min<br>
                Desv. Est.: {np.std(tf_B):.2f} min &nbsp;|&nbsp; CV: {np.std(tf_B)/np.mean(tf_B):.3f}<br>
                P10: {np.percentile(tf_B,10):.2f} &nbsp;|&nbsp; P90: {np.percentile(tf_B,90):.2f}<br>
                N piezas: {len(tf_B)}
                </div>""", unsafe_allow_html=True)

        # Box plot comparativo
        if comparar and resultados_B:
            st.markdown('<div class="section-header">📦 Box Plot Comparativo</div>',
                        unsafe_allow_html=True)
            fig_box = go.Figure()
            for escen, datos, color in [
                (f'A [K1={k1_a},K2={k2_a}]', tf_A, COLOR_A),
                (f'B [K1={k1_b},K2={k2_b}]', tf_B, COLOR_B)
            ]:
                # Función casera para parsear hex a rgba en fillcolor
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                fig_box.add_trace(go.Box(
                    y=datos, name=escen,
                    marker_color=color,
                    line_color=color,
                    boxmean='sd',
                    fillcolor=f'rgba({r},{g},{b},0.2)'
                ))
            apply_layout(fig_box, title="Distribución de Tiempos de Flujo",
                         extra=dict(yaxis_title="Tiempo de Flujo (min)"))
            st.plotly_chart(fig_box, use_container_width=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 4 – CUELLOS DE BOTELLA
    # ────────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown('<div class="section-header">🚧 Análisis de Cuellos de Botella</div>',
                    unsafe_allow_html=True)

        categorias = ['E1 Bloqueada', 'E2 Bloqueada', 'E2 Hambrienta', 'E3 Hambrienta']
        vals_A = [
            df_A['E1_bloq_pct'].mean(),
            df_A['E2_bloq_pct'].mean(),
            df_A['E2_hamb_pct'].mean(),
            df_A['E3_hamb_pct'].mean(),
        ]

        fig_bot = go.Figure()
        fig_bot.add_trace(go.Bar(
            name=f'Escenario A [K1={k1_a},K2={k2_a}]',
            x=categorias, y=vals_A,
            marker_color=COLOR_A,
            marker_line=dict(color='#d0d7de', width=1),
            text=[f"{v:.1f}%" for v in vals_A],
            textposition='outside',
            textfont=dict(color='#24292f', size=11),
        ))

        if comparar:
            vals_B = [
                df_B['E1_bloq_pct'].mean(),
                df_B['E2_bloq_pct'].mean(),
                df_B['E2_hamb_pct'].mean(),
                df_B['E3_hamb_pct'].mean(),
            ]
            fig_bot.add_trace(go.Bar(
                name=f'Escenario B [K1={k1_b},K2={k2_b}]',
                x=categorias, y=vals_B,
                marker_color=COLOR_B,
                marker_line=dict(color='#d0d7de', width=1),
                text=[f"{v:.1f}%" for v in vals_B],
                textposition='outside',
                textfont=dict(color='#24292f', size=11),
            ))

        apply_layout(fig_bot,
                     title="% de Tiempo Ineficiente por Estación (promedio entre réplicas)",
                     extra=dict(barmode='group', yaxis_title="% del Tiempo Total",
                                yaxis_range=[0, 100]))
        fig_bot.add_hline(y=20, line_dash='dot', line_color='rgba(209,36,47,0.4)',
                          annotation_text="Umbral de alerta 20%",
                          annotation_font_color=COLOR_RED)
        st.plotly_chart(fig_bot, use_container_width=True)

        # Gráfico de radar
        st.markdown('<div class="section-header">🕸️ Perfil de Eficiencia (Radar)</div>',
                    unsafe_allow_html=True)
        cats_radar = categorias + [categorias[0]]   # Cerrar el polígono

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[v for v in vals_A] + [vals_A[0]],
            theta=cats_radar,
            fill='toself',
            name=f'A [K1={k1_a},K2={k2_a}]',
            line_color=COLOR_A,
            fillcolor='rgba(9,105,218,0.15)'
        ))
        if comparar:
            fig_radar.add_trace(go.Scatterpolar(
                r=[v for v in vals_B] + [vals_B[0]],
                theta=cats_radar,
                fill='toself',
                name=f'B [K1={k1_b},K2={k2_b}]',
                line_color=COLOR_B,
                fillcolor='rgba(176,92,15,0.15)'
            ))
        apply_layout(fig_radar, title="Perfil de Ineficiencia (%)",
                     extra=dict(polar=dict(
                         radialaxis=dict(visible=True, range=[0, 100],
                                         gridcolor='#e1e4e8', color='#57606a'),
                         angularaxis=dict(gridcolor='#e1e4e8')
                     )))
        st.plotly_chart(fig_radar, use_container_width=True)

        # Tabla resumen cuellos de botella
        df_bot = pd.DataFrame({
            'Indicador': categorias,
            f'A [K1={k1_a},K2={k2_a}] (%)': [f"{v:.2f}" for v in vals_A],
        })
        if comparar:
            df_bot[f'B [K1={k1_b},K2={k2_b}] (%)'] = [f"{v:.2f}" for v in vals_B]
            df_bot['Δ (B-A)']                        = [f"{b-a:+.2f}" for a, b in zip(vals_A, vals_B)]
        st.dataframe(df_bot, use_container_width=True, hide_index=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 5 – ESTADÍSTICA & HIPÓTESIS
    # ────────────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-header">🧪 Prueba de Hipótesis – Throughput</div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-box info">
        <strong>Planteamiento estadístico:</strong><br>
        H₀: μ_throughput ≤ {umbral_h0:.1f} Pz/Hr &nbsp;&nbsp; (no supera el umbral)<br>
        H₁: μ_throughput &gt; {umbral_h0:.1f} Pz/Hr &nbsp;&nbsp; (supera el umbral)<br>
        Prueba: t de Student – 1 cola derecha &nbsp;|&nbsp; α = {alpha_ic:.2f}
        </div>""", unsafe_allow_html=True)

        col_h1, col_h2 = st.columns(2 if comparar else 1)
        with col_h1:
            rechaza_a = p_val_a < alpha_ic
            clase_a   = "success" if rechaza_a else "error"
            icono_a   = "✅" if rechaza_a else "❌"
            st.markdown(f"""
            <div class="stat-box {clase_a}">
            <strong>Escenario A [K1={k1_a}, K2={k2_a}]</strong><br><br>
            Media muestral: {th_a:.4f} Pz/Hr<br>
            Estadístico t: {t_stat_a:.4f}<br>
            Valor-p (cola derecha): <strong>{p_val_a:.6f}</strong><br><br>
            {icono_a} {'Se RECHAZA H₀: hay evidencia estadística (p < α) de que el throughput SUPERA '+str(umbral_h0)+' Pz/Hr.' 
                if rechaza_a else 
                'No se rechaza H₀: NO hay evidencia suficiente (p > α) de que el throughput supere '+str(umbral_h0)+' Pz/Hr.'}
            </div>""", unsafe_allow_html=True)

        if comparar:
            with col_h2:
                rechaza_b = p_val_b < alpha_ic
                clase_b   = "success" if rechaza_b else "error"
                icono_b   = "✅" if rechaza_b else "❌"
                st.markdown(f"""
                <div class="stat-box {clase_b}">
                <strong>Escenario B [K1={k1_b}, K2={k2_b}]</strong><br><br>
                Media muestral: {th_b:.4f} Pz/Hr<br>
                Estadístico t: {t_stat_b:.4f}<br>
                Valor-p (cola derecha): <strong>{p_val_b:.6f}</strong><br><br>
                {icono_b} {'Se RECHAZA H₀: hay evidencia estadística de que el throughput SUPERA '+str(umbral_h0)+' Pz/Hr.'
                    if rechaza_b else
                    'No se rechaza H₀: NO hay evidencia suficiente de que el throughput supere '+str(umbral_h0)+' Pz/Hr.'}
                </div>""", unsafe_allow_html=True)

        # Prueba t de 2 muestras (A vs B)
        if comparar:
            st.markdown('<div class="section-header">⚖️ Prueba t de 2 Muestras Independientes (A vs B)</div>',
                        unsafe_allow_html=True)
            t2_stat, t2_pval = st_stats.ttest_ind(
                df_A['throughput_hr'].tolist(),
                df_B['throughput_hr'].tolist(),
                alternative='less'   # ¿A < B?
            )
            rechaza_ab = t2_pval < alpha_ic
            st.markdown(f"""
            <div class="stat-box {'success' if rechaza_ab else 'error'}">
            H₀: μ_A ≥ μ_B &nbsp;|&nbsp; H₁: μ_A &lt; μ_B (B produce más)<br>
            Estadístico t: {t2_stat:.4f} &nbsp;|&nbsp; Valor-p: <strong>{t2_pval:.6f}</strong><br>
            {'✅ El Escenario B tiene throughput estadísticamente MAYOR que A (p < α).'
             if rechaza_ab else
             '❌ No hay diferencia estadísticamente significativa entre A y B.'}
            </div>""", unsafe_allow_html=True)

        # Distribución muestral del throughput
        st.markdown('<div class="section-header">📊 Distribución Muestral del Throughput</div>',
                    unsafe_allow_html=True)
        fig_th_dist = go.Figure()
        fig_th_dist.add_trace(go.Violin(
            y=df_A['throughput_hr'].tolist(),
            name=f'A [K1={k1_a},K2={k2_a}]',
            box_visible=True,
            meanline_visible=True,
            fillcolor='rgba(9,105,218,0.2)',
            line_color=COLOR_A
        ))
        if comparar:
            fig_th_dist.add_trace(go.Violin(
                y=df_B['throughput_hr'].tolist(),
                name=f'B [K1={k1_b},K2={k2_b}]',
                box_visible=True,
                meanline_visible=True,
                fillcolor='rgba(176,92,15,0.2)',
                line_color=COLOR_B
            ))
        fig_th_dist.add_hline(y=umbral_h0, line_dash='dash', line_color=COLOR_RED,
                              annotation_text=f"H₀ = {umbral_h0}",
                              annotation_font_color=COLOR_RED)
        apply_layout(fig_th_dist, title="Violin Plot – Throughput por réplica",
                     extra=dict(yaxis_title="Throughput (Pz/Hr)"))
        st.plotly_chart(fig_th_dist, use_container_width=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 6 – VALIDACIÓN GLC
    # ────────────────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="section-header">🎲 Validación del Generador Congruencial Lineal</div>',
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stat-box info">
        <strong>Parámetros del GLC:</strong><br>
        Ecuación: X_{{n+1}} = (a · Xₙ + c) mod m<br>
        m = 2³² = 4,294,967,296 &nbsp;|&nbsp; a = 1,664,525 &nbsp;|&nbsp; c = 1,013,904,223<br>
        Semilla X₀ = {semilla} &nbsp;|&nbsp; N generados = {n_glc_test}<br>
        Período máximo garantizado: m = 2³² (criterio Hull-Dobell satisfecho)
        </div>""", unsafe_allow_html=True)

        # Prueba Chi-cuadrado
        st.markdown('<div class="section-header">χ² Prueba de Uniformidad</div>',
                    unsafe_allow_html=True)

        rechaza_chi2 = chi2_res['rechaza']
        st.markdown(f"""
        <div class="stat-box {'error' if rechaza_chi2 else 'success'}">
        k = 10 clases &nbsp;|&nbsp; gl = {chi2_res['gl']}<br>
        χ² calculado: <strong>{chi2_res['chi2_stat']:.4f}</strong><br>
        χ² crítico (α=0.05): <strong>{chi2_res['chi2_crit']:.4f}</strong><br>
        Valor-p: <strong>{chi2_res['p_valor']:.4f}</strong><br><br>
        {'❌ Se RECHAZA H₀: los números NO son uniformes (χ² > χ²_crit).' 
         if rechaza_chi2 else
         '✅ No se rechaza H₀: los números son estadísticamente uniformes en [0,1).'}
        </div>""", unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            # Histograma de frecuencias
            bordes_mid = [(chi2_res['bordes'][i]+chi2_res['bordes'][i+1])/2
                          for i in range(len(chi2_res['observados']))]
            fig_chi = go.Figure()
            fig_chi.add_trace(go.Bar(
                x=[f"[{chi2_res['bordes'][i]:.1f},{chi2_res['bordes'][i+1]:.1f})"
                   for i in range(len(chi2_res['observados']))],
                y=chi2_res['observados'],
                name='Observado',
                marker_color=COLOR_A,
                marker_line=dict(color='#d0d7de', width=1)
            ))
            fig_chi.add_trace(go.Scatter(
                x=[f"[{chi2_res['bordes'][i]:.1f},{chi2_res['bordes'][i+1]:.1f})"
                   for i in range(len(chi2_res['esperados']))],
                y=chi2_res['esperados'],
                name='Esperado (uniforme)',
                mode='lines+markers',
                line=dict(color=COLOR_RED, dash='dash', width=2),
                marker=dict(size=6)
            ))
            apply_layout(fig_chi,
                         title=f"Frecuencias Observadas vs Esperadas (N={n_glc_test})",
                         extra=dict(xaxis_title="Clase", yaxis_title="Frecuencia",
                                    xaxis_tickangle=-30))
            st.plotly_chart(fig_chi, use_container_width=True)

        with col_g2:
            # Gráfico de dispersión U_n vs U_{n+1}
            nums_plot = nums_u[:min(1000, n_glc_test)]
            fig_scatter = go.Figure(go.Scatter(
                x=nums_plot[:-1], y=nums_plot[1:],
                mode='markers',
                marker=dict(color=COLOR_A, size=3, opacity=0.5),
                name='(Uₙ, Uₙ₊₁)'
            ))
            apply_layout(fig_scatter, title="Gráfico de Secuencia: Uₙ vs Uₙ₊₁",
                         extra=dict(xaxis_title="Uₙ", yaxis_title="Uₙ₊₁"))
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Histograma de tiempos exponenciales generados
        st.markdown('<div class="section-header">📐 Distribución de Tiempos Exponenciales Generados</div>',
                    unsafe_allow_html=True)
        rng_exp = GeneradorCongruencialLineal(semilla)
        tiempos_exp = [rng_exp.exponencial(media_proceso) for _ in range(min(1000, n_glc_test))]
        x_teo  = np.linspace(0, max(tiempos_exp)*1.2, 300)
        y_teo  = (1/media_proceso) * np.exp(-x_teo/media_proceso)

        fig_exp = go.Figure()
        fig_exp.add_trace(go.Histogram(
            x=tiempos_exp, nbinsx=30,
            name=f'GLC Exp(μ={media_proceso})',
            histnorm='probability density',
            marker_color=COLOR_GREEN,
            marker_line=dict(color='#ffffff', width=0.5),
            opacity=0.7
        ))
        fig_exp.add_trace(go.Scatter(
            x=x_teo.tolist(), y=y_teo.tolist(),
            name=f'f(x) teórica = (1/{media_proceso})·e^(-x/{media_proceso})',
            line=dict(color=COLOR_RED, width=2)
        ))
        apply_layout(fig_exp,
                     title=f"Tiempos Exponenciales Generados vs Teórica (N={len(tiempos_exp)})",
                     extra=dict(xaxis_title="Tiempo (min)", yaxis_title="Densidad de probabilidad"))
        st.plotly_chart(fig_exp, use_container_width=True)

    # ────────────────────────────────────────────────────────────────
    # TAB 7 – TABLA DE RÉPLICAS
    # ────────────────────────────────────────────────────────────────
    with tabs[6]:
        st.markdown('<div class="section-header">📋 Tabla de Resultados por Réplica</div>',
                    unsafe_allow_html=True)

        # Tabla Escenario A
        st.markdown(f"**Escenario A** – K1={k1_a}, K2={k2_a}")
        tabla_A = df_A[[
            'throughput_hr', 'tiempo_flujo', 'wip_prom',
            'E1_bloq_pct', 'E2_bloq_pct', 'E2_hamb_pct', 'E3_hamb_pct',
            'n_completadas'
        ]].copy()
        tabla_A.index = [f"Réplica {i+1}" for i in range(len(tabla_A))]
        tabla_A.columns = ['Throughput (Pz/Hr)', 'T.Flujo (min)', 'WIP Prom',
                           'E1 Bloq (%)', 'E2 Bloq (%)', 'E2 Hamb (%)', 'E3 Hamb (%)',
                           'N Completas']
        # Fila de resumen
        resumen_A = tabla_A.mean().to_frame().T
        resumen_A.index = ['── PROMEDIO ──']
        tabla_A_full = pd.concat([tabla_A, resumen_A])
        st.dataframe(tabla_A_full.style.format("{:.3f}"), use_container_width=True)

        if comparar:
            st.markdown(f"**Escenario B** – K1={k1_b}, K2={k2_b}")
            tabla_B = df_B[[
                'throughput_hr', 'tiempo_flujo', 'wip_prom',
                'E1_bloq_pct', 'E2_bloq_pct', 'E2_hamb_pct', 'E3_hamb_pct',
                'n_completadas'
            ]].copy()
            tabla_B.index = [f"Réplica {i+1}" for i in range(len(tabla_B))]
            tabla_B.columns = ['Throughput (Pz/Hr)', 'T.Flujo (min)', 'WIP Prom',
                                'E1 Bloq (%)', 'E2 Bloq (%)', 'E2 Hamb (%)', 'E3 Hamb (%)',
                                'N Completas']
            resumen_B = tabla_B.mean().to_frame().T
            resumen_B.index = ['── PROMEDIO ──']
            tabla_B_full = pd.concat([tabla_B, resumen_B])
            st.dataframe(tabla_B_full.style.format("{:.3f}"), use_container_width=True)

        # Descargar CSV
        st.markdown("---")
        csv_A = tabla_A.to_csv(index=True).encode('utf-8')
        st.download_button(
            "⬇️ Descargar CSV Escenario A",
            csv_A,
            file_name=f"replicas_escenario_A_K1{k1_a}_K2{k2_a}.csv",
            mime='text/csv'
        )
        if comparar:
            csv_B = tabla_B.to_csv(index=True).encode('utf-8')
            st.download_button(
                "⬇️ Descargar CSV Escenario B",
                csv_B,
                file_name=f"replicas_escenario_B_K1{k1_b}_K2{k2_b}.csv",
                mime='text/csv'
            )

        # Recomendación final
        st.markdown('<div class="section-header">💡 Recomendación Final</div>',
                    unsafe_allow_html=True)
        if comparar:
            ganador_th  = "B" if th_b > th_a else "A"
            ganador_ft  = "B" if ft_b < ft_a else "A"
            ganador_wip = "B" if wip_b < wip_a else "A"
            mejor_k = (k1_b, k2_b) if ganador_th == "B" else (k1_a, k2_a)
            st.markdown(f"""
            <div class="stat-box success">
            <strong>📌 Análisis comparativo:</strong><br>
            Mayor throughput: Escenario {ganador_th} &nbsp;|&nbsp;
            Menor tiempo de flujo: Escenario {ganador_ft} &nbsp;|&nbsp;
            Menor WIP: Escenario {ganador_wip}<br><br>
            <strong>Recomendación: K1={mejor_k[0]}, K2={mejor_k[1]}</strong> —
            configuración con mejor desempeño global según los KPIs simulados.
            Nota: buffers más grandes reducen bloqueos/hambres pero incrementan el WIP;
            el diseñador debe balancear según restricciones de espacio y costo de inventario.
            </div>""", unsafe_allow_html=True)

# ── Estado inicial (sin simulación) ────────────────────────────────
else:
    st.markdown("""
    <div style='background:#ffffff; border:1px dashed #d0d7de; border-radius:12px;
                padding: 3rem 2rem; text-align:center; margin-top: 2rem;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>🏭</div>
        <p style='font-family: Rajdhani, sans-serif; font-size:1.5rem; font-weight:600;
                  color:#24292f; margin:0;'>
            Configure los parámetros en el panel lateral y presione
        </p>
        <p style='font-family: IBM Plex Mono, monospace; font-size: 1rem;
                  color: #0969da; margin: 0.5rem 0 0 0;'>
            🚀 INICIAR SIMULACIÓN
        </p>
        <hr style='border-color:#d0d7de; margin: 1.5rem auto; width:60%;'>
        <p style='font-family: IBM Plex Mono, monospace; font-size: 0.78rem;
                  color:#57606a; margin:0; line-height:2;'>
            Motor GLC: X_(n+1) = (1664525·Xₙ + 1013904223) mod 2³²<br>
            Exponencial: T = -μ·ln(1-U) &nbsp;|&nbsp; μ = 4 min &nbsp;|&nbsp; λ = 0.25 pz/min<br>
            Bloqueo modelado con simpy.Store &nbsp;|&nbsp; IC calculado con t-Student
        </p>
    </div>
    """, unsafe_allow_html=True)