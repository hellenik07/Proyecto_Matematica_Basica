import streamlit as st
import juego_trivia
import tutor

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MathSolve — Inecuaciones",
    layout="wide", 
)

# ══════════════════════════════════════════════════════════════
# CSS GLOBAL (Sincronizado y adaptado para Sidebar)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
section.main,
.main .block-container {
    font-family: 'Nunito', 'Segoe UI', sans-serif !important;
    background-color: #FAF6F0 !important;
    color: #1A1A1A !important;
}
.main .block-container {
    max-width: 1100px !important; 
    padding-top: 2.2rem !important;
    padding-bottom: 3rem !important;
}

/* ── Barra Lateral (Sidebar Estática) ── */
[data-testid="stSidebar"] {
    background-color: #FAF6F0 !important; 
    border-right: 1px solid #CBD5E1 !important;
    box-shadow: 4px 0 15px rgba(0,0,0,0.05) !important;
    padding-top: 2rem !important;
}

/* ── Cabecera de la app ── */
.app-header {
    background: #8B0000;
    border-radius: 16px;
    padding: 28px 36px 24px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.app-header::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.app-name {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,210,200,0.8);
    margin-bottom: 6px;
}
.app-title {
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
    line-height: 1.1;
}
.app-tagline {
    font-size: 0.92rem;
    color: rgba(255,210,200,0.75);
    font-weight: 500;
    margin: 0;
}

/* ── Divisor ── */
hr {
    border: none !important;
    border-top: 1px solid #E2DDD8 !important;
    margin: 2rem 0 !important;
}

/* ── Pestañas ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 2px solid #E2DDD8 !important;
    gap: 0 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    color: #9CA3AF !important;
    padding: 10px 22px !important;
    border: none !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    transition: color 0.15s ease, border-color 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #8B0000 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #8B0000 !important;
    border-bottom: 2px solid #8B0000 !important;
    font-weight: 800 !important;
}

/* ── Bloques de contenido ── */
.info-block {
    background: #FFFFFF;
    border: 1px solid #E2DDD8;
    border-left: 4px solid #8B0000;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.info-block-title {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8B0000;
    margin-bottom: 8px;
}
.info-block p {
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
    color: #374151 !important;
    font-weight: 400 !important;
    margin: 0 !important;
}
.info-block ul {
    margin: 8px 0 0 0 !important;
    padding-left: 18px !important;
}
.info-block ul li {
    font-size: 0.95rem !important;
    color: #374151 !important;
    line-height: 1.65 !important;
    font-weight: 400 !important;
    padding: 1px 0 !important;
}

.dato-chip {
    display: inline-block;
    background: #FFF0EE;
    border: 1px solid #F5C6BE;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 0.88rem;
    color: #8B0000;
    font-weight: 700;
    margin-top: 8px;
    font-family: 'Space Mono', monospace;
}

/* ── Tarjetas de Módulos (Estilo Fijo en Sidebar) ── */
.modulo-sidebar-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.02);
    position: relative;
    overflow: hidden;
}
.modulo-sidebar-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: #8B0000;
}
.modulo-label {
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8B0000;
    margin-bottom: 2px;
}
.modulo-name {
    font-size: 0.95rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 4px;
}
.modulo-desc {
    font-size: 0.78rem;
    color: #6B7280;
    line-height: 1.4;
    margin-bottom: 10px;
}

/* ── Botones ── */
div.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    background-color: #FAF6F0 !important;
    color: #8B0000 !important;
    border: 1.5px solid #8B0000 !important;
}

div.stButton > button:hover {
    background-color: #8B0000 !important;
    color: #FFFFFF !important;
    border: 1.5px solid #8B0000 !important;
    transform: translateY(-1px) !important;
}

div.stButton > button:active, div.stButton > button:focus {
    background-color: #8B0000 !important;
    color: #FFFFFF !important;
    border-color: #8B0000 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ESTADO DE NAVEGACIÓN
# ══════════════════════════════════════════════════════════════
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

# ══════════════════════════════════════════════════════════════
# BARRA LATERAL ESTÁTICA (Acceso a Módulos estilo Nubes)
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h2 style='color: #8B0000; margin-top: -10px; font-size: 1.25rem;'>Acceso a Módulos</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0 20px 0 !important;'>", unsafe_allow_html=True)
    
    # Módulo 1: Práctica
    st.markdown("""
    <div class="modulo-sidebar-card">
        <div class="modulo-label">Módulo de práctica</div>
        <div class="modulo-name">Rescatar a Gauss</div>
        <div class="modulo-desc">Resuelve inecuaciones paso a paso en un formato interactivo con vidas y comodines.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir al juego", key="side_juego", use_container_width=True):
        st.session_state.pagina = "juego"
        st.rerun()
        
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    
    # Módulo 2: Tutor
    st.markdown("""
    <div class="modulo-sidebar-card">
        <div class="modulo-label">Tutor Inteligente</div>
        <div class="modulo-name">Tutor MathSolve</div>
        <div class="modulo-desc">Resuelve inecuaciones con asistencia inteligente y retroalimentación inmediata.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir al tutor", key="side_tutor", use_container_width=True):
        st.session_state.pagina = "tutor"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# ENRUTAMIENTO
# ══════════════════════════════════════════════════════════════
if st.session_state.pagina == "juego":
    juego_trivia.mostrar_juego()
    st.stop()

if st.session_state.pagina == "tutor":
    tutor.mostrar_tutor()
    st.stop()

# ══════════════════════════════════════════════════════════════
# PÁGINA PRINCIPAL (HOME)
# ══════════════════════════════════════════════════════════════

# ── Cabecera ──────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-name">MathSolve</div>
  <div class="app-title">Inecuaciones</div>
  <div class="app-tagline">Plataforma educativa interactiva para el aprendizaje de inecuaciones</div>
</div>
""", unsafe_allow_html=True)

# ── Pestañas ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Que son",
    "Para que sirven",
    "Historia",
    "Dato curioso",
])

# ── TAB 1: Que son ────────────────────────────────────────────
with tab1:
    st.markdown("""
<div class="info-block">
  <div class="info-block-title">Definicion</div>
  <p>
    Una inecuacion es una expresion matematica que compara dos cantidades usando los simbolos
    de desigualdad: menor que (&lt;), mayor que (&gt;), menor o igual que (&#x2264;) y
    mayor o igual que (&#x2265;). A diferencia de una ecuacion, que busca un valor exacto,
    una inecuacion describe un rango de valores posibles.
  </p>
</div>

<div class="info-block">
  <div class="info-block-title">Cuando las usamos</div>
  <p>No siempre necesitamos un valor exacto. A veces solo necesitamos saber
  si algo es mayor, menor o esta dentro de un rango. Por ejemplo:</p>
  <ul>
    <li>¿Hay suficiente dinero para comprar algo?</li>
    <li>¿Cuantas personas caben en un lugar?</li>
    <li>¿Cual es la velocidad maxima permitida?</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# ── TAB 2: Para que sirven ────────────────────────────────────
with tab2:
    st.markdown("""
<div class="info-block">
  <div class="info-block-title">Aplicaciones en la vida real</div>
  <p>Las inecuaciones permiten modelar restricciones y tomar decisiones cuando existen limites.
  Se utilizan en muchas areas:</p>
  <ul>
    <li>Economia y finanzas: control de presupuestos y rangos de inversion</li>
    <li>Ingenieria y construccion: margenes de tolerancia y cargas maximas</li>
    <li>Medicina y ciencia: rangos normales en examenes clinicos</li>
    <li>Programacion y tecnologia: optimizacion de recursos en algoritmos</li>
    <li>Transporte y logistica: capacidades maximas y rutas eficientes</li>
  </ul>
</div>

<div class="info-block">
  <div class="info-block-title">En matematica avanzada</div>
  <p>
    Las inecuaciones son la base de la programacion lineal, usada en logistica, economia
    y ciencias de la computacion para encontrar la solucion mas eficiente dentro de un
    conjunto acotado de posibilidades.
  </p>
</div>
""", unsafe_allow_html=True)

# ── TAB 3: Historia ───────────────────────────────────────────
with tab3:
    st.markdown("""
<div class="info-block">
  <div class="info-block-title">Origenes en Grecia antigua</div>
  <p>
    Las inecuaciones surgieron en la antigua Grecia.
    Matematicos como Euclides y Arquimedes las utilizaban para comparar longitudes,
    areas y volumenes cuando necesitaban saber si una cantidad era mayor o menor que otra,
    sin requerir un valor exacto.
  </p>
</div>

<div class="info-block">
  <div class="info-block-title">Consolidacion en el siglo XVII</div>
  <p>
    Su estudio formal florecio en el siglo XVII. Fue en esta epoca cuando los matematicos
    comenzaron a desarrollar notaciones precisas para representar limites y restricciones
    mas alla de la igualdad exacta, sentando las bases del algebra moderna.
  </p>
</div>
""", unsafe_allow_html=True)

# ── TAB 4: Dato curioso ───────────────────────────────────────
with tab4:
    st.markdown("""
<div class="info-block">
  <div class="info-block-title">El origen de los simbolos</div>
  <p>
    Los simbolos &lt; y &gt; fueron introducidos por el matematico ingles
    <strong>Thomas Harriot</strong> en 1631, en su obra <em>Artis Analyticae Praxis</em>.
    Antes de su propuesta, los matematicos usaban palabras o notaciones mucho mas largas
    para expresar comparaciones entre cantidades.
  </p>
  <p style="margin-top:10px !important;">
    Desde entonces, estos dos simbolos transformaron la forma de resolver problemas matematicos
    complejos y se convirtieron en una herramienta fundamental tanto en matematica pura
    como aplicada.
  </p>
</div>
""", unsafe_allow_html=True)
    st.markdown("""
<div class="dato-chip">1631 — Thomas Harriot introduce &lt; y &gt;</div>
""", unsafe_allow_html=True)