import streamlit as st
import random


# ══════════════════════════════════════════════════════════════
# DATOS
# ══════════════════════════════════════════════════════════════

INECUACIONES = {
    1: [
        {
            "titulo": "El Despertar Lineal",
            "enunciado": r"4x + 7 \ge 2x - 3",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: Transposición",
                    "expresion_dinamica": r"4x + 7 \ge 2x - 3",
                    "expresion": r"4x - 2x \ge -3 - 7 \implies 2x \ge -10",
                    "pregunta": "Pasa las variables a la izquierda y los números a la derecha. ¿Cuál es tu jugada?",
                    "opciones": {"A": "6x ≥ 4", "B": "2x ≤ −10", "C": "2x ≥ −10"},
                    "correcta": "C",
                    "ok": "Misión cumplida. Pasaste el 2x restando y el 7 al otro lado perfectamente.",
                    "err": "Recuerda: al cruzar la desigualdad, los signos cambian (el 7 pasa restando).",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: El Despeje Definitivo",
                    "expresion_dinamica": r"2x \ge -10",
                    "expresion": r"x \ge \frac{-10}{2} \implies x \ge -5",
                    "pregunta": "Al dividir entre 2 (positivo), ¿qué le pasa a la desigualdad?",
                    "opciones": {
                        "A": "x ≥ −5 · Mantiene su rumbo",
                        "B": "x ≤ −5 · El sentido se invierte",
                        "C": "x ≥ 5 · Cambia el signo"
                    },
                    "correcta": "A",
                    "ok": "Justo en el blanco. El 2 es positivo, la desigualdad mantiene su dirección.",
                    "err": "La desigualdad SOLO se invierte si divides entre un número NEGATIVO.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: Forjando el Intervalo",
                    "expresion_dinamica": r"x \ge -5",
                    "expresion": r"S: x \in [-5, +\infty[",
                    "pregunta": "x ≥ −5. Tienes 'mayor o igual', el −5 debe estar incluido. ¿Qué intervalo eliges?",
                    "opciones": {"A": "S: x ∈ ]−∞, −5]", "B": "S: x ∈ [−5, +∞[", "C": "S: x ∈ ]−5, +∞["},
                    "correcta": "B",
                    "ok": "Misión cumplida. El corchete abraza al −5 (cerrado) y el infinito vuela libre.",
                    "err": "El símbolo '≥' incluye al −5, necesitas corchete CERRADO [ para protegerlo.",
                },
            ],
        },
        {
            "titulo": "Duelo de Agrupaciones",
            "enunciado": r"3x - 1 \ge 3 + x",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: El Choque de Términos",
                    "expresion_dinamica": r"3x - 1 \ge 3 + x",
                    "expresion": r"3x - x \ge 3 + 1 \implies 2x \ge 4",
                    "pregunta": "Pasa la x restando a la izquierda y el −1 sumando a la derecha.",
                    "opciones": {"A": "2x ≥ 4", "B": "4x ≥ 2", "C": "2x ≤ 4"},
                    "correcta": "A",
                    "ok": "Movimiento de Maestro. 3x − x = 2x y 3 + 1 = 4.",
                    "err": "La x de la derecha pasa a RESTAR, y el −1 de la izquierda pasa a SUMAR.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: El Golpe de Gracia",
                    "expresion_dinamica": r"2x \ge 4",
                    "expresion": r"x \ge \frac{4}{2} \implies x \ge 2",
                    "pregunta": "Divide ambos lados entre 2. ¿Cambia el rumbo de la desigualdad?",
                    "opciones": {"A": "x ≤ 2", "B": "x > 2", "C": "x ≥ 2"},
                    "correcta": "C",
                    "ok": "Justo en el blanco. 4 ÷ 2 = 2 y el signo se mantiene (dividiste por positivo).",
                    "err": "Dividir entre un número positivo jamás cambia la orientación. Mantén el ≥.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: Sellando el Destino",
                    "expresion_dinamica": r"x \ge 2",
                    "expresion": r"S: x \in [2, +\infty[",
                    "pregunta": "x ≥ 2 significa valores mayores o iguales a 2. ¿Cuál es el conjunto correcto?",
                    "opciones": {"A": "S: x ∈ ]2, +∞[", "B": "S: x ∈ ]−∞, 2]", "C": "S: x ∈ [2, +∞["},
                    "correcta": "C",
                    "ok": "Épico. Cerraste el corchete en el 2 como todo un profesional.",
                    "err": "Vamos hacia los mayores (+∞), y el 2 va con corchete cerrado porque lleva la igualdad.",
                },
            ],
        },
    ],

    2: [
        {
            "titulo": "El Bosque Polinomial",
            "enunciado": r"x^{2} - 6x + 8 < 0",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: Descifrando el Enigma",
                    "expresion_dinamica": r"x^{2} - 6x + 8 < 0",
                    "expresion": r"(x - 4)(x - 2) < 0",
                    "pregunta": "Dos números: multiplicados dan +8, sumados dan −6. ¿Cuál es la factorización?",
                    "opciones": {"A": "(x − 8)(x + 1) < 0", "B": "(x − 4)(x − 2) < 0", "C": "(x + 4)(x + 2) < 0"},
                    "correcta": "B",
                    "ok": "Mente brillante. −4 y −2 encajan a la perfección.",
                    "err": "Para suma negativa y producto positivo, ambos números DEBEN ser negativos.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Buscando los Ceros",
                    "expresion_dinamica": r"(x - 4)(x - 2) < 0",
                    "expresion": r"\text{Ceros: } x = 2 \text{ y } x = 4 \text{ (abiertos)}",
                    "pregunta": "Es < estricta (sin igualdad). ¿Cómo quedan los ceros al despejar?",
                    "opciones": {
                        "A": "x = 2 y x = 4, ABIERTOS",
                        "B": "x = −2 y x = −4, ABIERTOS",
                        "C": "x = 2 y x = 4, CERRADOS"
                    },
                    "correcta": "A",
                    "ok": "Esquivaste la trampa. Los puntos van abiertos porque es < estricto.",
                    "err": "Como es < (sin rayita abajo), los puntos van ABIERTOS. Al despejar −4 → +4.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: La Lectura del Mapa",
                    "expresion_dinamica": r"\text{Ceros abiertos: } x = 2 \text{ y } x = 4",
                    "expresion": r"S: x \in ]2, 4[",
                    "pregunta": "El producto es NEGATIVO (< 0) justo en el medio. ¿Cuál es el camino?",
                    "opciones": {
                        "A": "S: x ∈ ]−∞, 2[ ∪ ]4, +∞[",
                        "B": "S: x ∈ [2, 4]",
                        "C": "S: x ∈ ]2, 4["
                    },
                    "correcta": "C",
                    "ok": "Zona central negativa con corchetes abiertos perfectos. ¡Nivel completado!",
                    "err": "Te interesa la zona NEGATIVA (< 0), que es el centro, no los bordes.",
                },
            ],
        },
        {
            "titulo": "La Parábola Invertida",
            "enunciado": r"-x^{2} - x + 6 < 0",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: El Espejismo Negativo",
                    "expresion_dinamica": r"-x^{2} - x + 6 < 0",
                    "expresion": r"(-x + 2)(x + 3) < 0",
                    "pregunta": "Tienes coeficiente negativo al frente. ¿Qué factorización cuadra exactamente?",
                    "opciones": {
                        "A": "(x + 2)(x − 3) < 0",
                        "B": "(−x + 2)(x + 3) < 0",
                        "C": "(−x − 2)(x − 3) < 0"
                    },
                    "correcta": "B",
                    "ok": "Cálculo frío y preciso. Al multiplicar cruzado cuadra exactamente.",
                    "err": "Verifica multiplicando término a término; las otras opciones no llegan a la original.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Cazando los Ceros",
                    "expresion_dinamica": r"(-x + 2)(x + 3) < 0",
                    "expresion": r"\text{Ceros: } x = -3 \text{ y } x = 2 \text{ (abiertos)}",
                    "pregunta": "Uno de los factores tiene la 'x' negativa. ¿Cuáles son los ceros?",
                    "opciones": {
                        "A": "x = 2 y x = 3, ABIERTOS",
                        "B": "x = −2 y x = 3, CERRADOS",
                        "C": "x = 2 y x = −3, ABIERTOS"
                    },
                    "correcta": "C",
                    "ok": "Al despejar −x+2=0 pasa la x y queda x=2 positivo.",
                    "err": "Al despejar −x+2=0 queda x=2 (positivo). Y como es <, los puntos son abiertos.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: El Territorio Exterior",
                    "expresion_dinamica": r"\text{Ceros abiertos: } x = -3 \text{ y } x = 2",
                    "expresion": r"S: x \in ]-\infty, -3[ \cup ]2, +\infty[",
                    "pregunta": "Con coeficiente negativo, el producto < 0 está en los bordes exteriores.",
                    "opciones": {
                        "A": "S: x ∈ ]−∞, −3[ ∪ ]2, +∞[",
                        "B": "S: x ∈ ]−3, 2[",
                        "C": "S: x ∈ ]−∞, −2[ ∪ ]3, +∞["
                    },
                    "correcta": "A",
                    "ok": "Épico. Dominaste la parábola invertida. Las dos zonas exteriores perfectas.",
                    "err": "Al ser invertida el centro es positivo. Buscas los bordes porque es < cero.",
                },
            ],
        },
    ],

    3: [
        {
            "titulo": "El Pantano del M.C.M",
            "enunciado": r"\frac{4}{x-3} \ge \frac{5}{x+2}",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: El Gran Puente Común",
                    "expresion_dinamica": r"\frac{4}{x-3} \ge \frac{5}{x+2}",
                    "expresion": r"\frac{4(x+2) - 5(x-3)}{(x-3)(x+2)} \ge 0",
                    "pregunta": "Pasa todo a la izquierda. Con MCM (x−3)(x+2), ¿cómo construyes el numerador?",
                    "opciones": {
                        "A": "4(x−3) − 5(x+2)",
                        "B": "4 − 5 (Resta directa)",
                        "C": "4(x+2) − 5(x−3)"
                    },
                    "correcta": "C",
                    "ok": "Cruzaste los factores con sus numeradores opuestos perfectamente.",
                    "err": "Cada número arriba debe multiplicarse por el bloque que le falta de abajo.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Distribución",
                    "expresion_dinamica": r"\frac{4(x+2) - 5(x-3)}{(x-3)(x+2)} \ge 0",
                    "expresion": r"\frac{-x + 23}{(x-3)(x+2)} \ge 0",
                    "pregunta": "Al distribuir el −5 por el (x−3)… ojo con los signos. ¿Qué queda?",
                    "opciones": {"A": "−x − 7", "B": "9x − 7", "C": "−x + 23"},
                    "correcta": "C",
                    "ok": "−5 por −3 es +15 positivo. Agrupaste genial a −x + 23.",
                    "err": "Un negativo por un negativo (−5 × −3) da POSITIVO (+15). Recalcula.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: Restricciones",
                    "expresion_dinamica": r"\frac{-x + 23}{(x-3)(x+2)} \ge 0",
                    "expresion": r"S: x \in ]-\infty, -2[ \cup ]3, 23]",
                    "pregunta": "El cero 23 se cierra (≥). Las restricciones −2 y 3 NUNCA se cierran. ¿Tu respuesta?",
                    "opciones": {
                        "A": "S: x ∈ ]−2, 3[ ∪ ]23, +∞[",
                        "B": "S: x ∈ ]−∞, −2[ ∪ ]3, 23]",
                        "C": "S: x ∈ ]−∞, −2] ∪ [3, 23]"
                    },
                    "correcta": "B",
                    "ok": "Victoria total. Las restricciones de abajo siempre van abiertas.",
                    "err": "Los ceros del DENOMINADOR NUNCA llevan corchete cerrado (dividir por 0 es imposible).",
                },
            ],
        },
        {
            "titulo": "La Caverna de los Bloques",
            "enunciado": r"\frac{-x-10}{x+1} > -x-2",
            "pasos": [
                {
                    "num": 1,
                    "descripcion": "Fase 1: El Movimiento Táctico",
                    "expresion_dinamica": r"\frac{-x-10}{x+1} > -x-2",
                    "expresion": r"\frac{-x-10 - [(-x-2)(x+1)]}{x+1} > 0",
                    "pregunta": "Para no arruinar los casos de signos, ¿cuál es tu primer paso estratégico?",
                    "opciones": {
                        "A": "Borrar el denominador",
                        "B": "Pasar el (x+1) a multiplicar al otro lado",
                        "C": "Pasar TODO el bloque derecho restando y armar el MCM"
                    },
                    "correcta": "C",
                    "ok": "Esquivaste la trampa. Pasar el bloque restando es el movimiento correcto.",
                    "err": "Multiplicar cruzado en inecuaciones es trampa mortal. Pasa el bloque restando.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Limpiando la Caverna",
                    "expresion_dinamica": r"\frac{-x-10 - [(-x-2)(x+1)]}{x+1} > 0",
                    "expresion": r"\frac{(x+4)(x-2)}{x+1} > 0",
                    "pregunta": "Arriba quedó x²+2x−8. Factoriza: ¿qué factores suman +2 y multiplican −8?",
                    "opciones": {
                        "A": "(x+4)(x−2)",
                        "B": "(x+8)(x−1)",
                        "C": "(x−4)(x+2)"
                    },
                    "correcta": "A",
                    "ok": "Golpe certero. +4 y −2: producto −8, suma +2.",
                    "err": "Busca factores que SUMADOS den +2 (positivo). Tu opción da negativo al medio.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: El Salto a la Libertad",
                    "expresion_dinamica": r"\frac{(x+4)(x-2)}{x+1} > 0",
                    "expresion": r"S: x \in ]-4, -1[ \cup ]2, +\infty[",
                    "pregunta": "Ceros en −4 y 2, restricción en −1. Es MAYOR ESTRICTO (>): todo va abierto.",
                    "opciones": {
                        "A": "S: x ∈ [−4, −1] ∪ [2, +∞[",
                        "B": "S: x ∈ ]−4, −1[ ∪ ]2, +∞[",
                        "C": "S: x ∈ ]−∞, −4[ ∪ ]−1, 2["
                    },
                    "correcta": "B",
                    "ok": "Victoria total. Corchetes abiertos en su lugar, tramos positivos perfectos.",
                    "err": "Si el símbolo es > (estricto), JAMÁS puedes usar corchete cerrado.",
                },
            ],
        },
    ],
}

TEMAS_ERROR = {
    (1, 0, 0): "Dominio de signos al cruzar el 'igual' (Transposición)",
    (1, 0, 1): "Las desigualdades solo cambian al dividir por negativos",
    (1, 0, 2): "Diferenciar intervalos cerrados [ de los abiertos ]",
    (1, 1, 0): "Agrupación táctica: Variables izquierda, números derecha",
    (1, 1, 1): "Despejes con coeficientes positivos (el signo se mantiene)",
    (1, 1, 2): "Hacia donde apunta el infinito (+∞ o -∞)",
    (2, 0, 0): "Factorización de trinomios y ley de signos",
    (2, 0, 1): "Saber cuándo un punto es abierto o cerrado",
    (2, 0, 2): "Mapa de Signos: Hallar zonas negativas entre los ceros",
    (2, 1, 0): "Factorizar trinomios con coeficiente negativo",
    (2, 1, 1): "Extraer raíces de binomios con la 'x' negativa",
    (2, 1, 2): "Zonas exteriores negativas si la x² es negativa",
    (3, 0, 0): "Creación de M.C.M y cruce correcto de términos",
    (3, 0, 1): "Multiplicaciones de dos números negativos (da positivo)",
    (3, 0, 2): "Restricciones del denominador NUNCA van cerradas",
    (3, 1, 0): "NUNCA multiplicar cruzado en inecuaciones racionales",
    (3, 1, 1): "Factorizar trinomios luego de desarrollar corchetes",
    (3, 1, 2): "Elegir múltiples tramos positivos en tablas grandes",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

.stDecoration, [data-testid="stHeader"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
section.main, .main .block-container {
    background-color: #F5F0EB !important;
    color: #0F172A !important;
    font-family: 'Nunito', 'Segoe UI', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #EDE8E2 !important;
    border-right: 1px solid #CBD5E1 !important;
}
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 820px !important;
}

/* Tipografía compacta */
h1 { font-weight:900!important; font-size:1.7rem!important; color:#8B0000!important;
     letter-spacing:-0.02em!important; margin:0 0 2px 0!important; text-align:center; }
h2 { font-weight:800!important; font-size:1.25rem!important; color:#0F172A!important; margin:0 0 4px 0!important; }
h3 { font-weight:700!important; font-size:1rem!important; color:#1E293B!important; margin:0 0 4px 0!important; }
p, li, label { color:#334155!important; font-size:0.92rem!important; line-height:1.55!important; }
.eyebrow { font-size:0.62rem!important; font-weight:800!important; letter-spacing:0.16em!important;
           text-transform:uppercase!important; color:#8B0000!important; margin-bottom:1px!important; display:block; }

/* ── WELCOME BANNER ── */
.welcome-banner { background:#8B0000; border-radius:14px; padding:16px 20px 14px; margin-bottom:14px; }
.gauss-title { font-size:1.25rem!important; font-weight:900!important; color:#FFF5F0!important; margin-bottom:5px!important; }
.gauss-story { font-size:0.87rem!important; color:#FFD5CC!important; line-height:1.5!important; font-weight:600!important; }
.rules-row { display:flex; gap:6px; margin-top:10px; flex-wrap:wrap; }
.rules-chip { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25); border-radius:6px;
              padding:3px 10px; font-size:0.74rem!important; color:#FFE8E0!important; font-weight:700!important; }

/* ── NIVEL CARDS ── */
.nivel-card { background:#FAF6F0; border:1px solid #CBD5E1; border-radius:12px; padding:14px 13px 10px;
              position:relative; overflow:hidden; transition:all 0.15s ease; }
.nivel-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px;
                      background:#8B0000; border-radius:12px 12px 0 0; }
.nivel-card:hover { border-color:#8B0000; box-shadow:0 4px 14px rgba(139,0,0,0.13); transform:translateY(-1px); }
.nivel-num { font-family:'Space Mono',monospace!important; font-size:0.6rem!important; font-weight:700!important;
             letter-spacing:0.14em!important; text-transform:uppercase!important; color:#8B0000!important; margin-bottom:3px!important; }
.nivel-name { font-size:0.88rem!important; font-weight:800!important; color:#0F172A!important; margin-bottom:3px!important; }
.nivel-stars { font-size:0.85rem!important; margin-bottom:4px!important; }
.nivel-desc { font-size:0.78rem!important; color:#64748B!important; line-height:1.35!important; margin-bottom:8px!important; }
.nivel-tag { display:inline-block; font-family:'Space Mono',monospace!important; font-size:0.62rem!important;
             color:#64748B!important; background:#F1EDE8; border:1px solid #CBD5E1; border-radius:3px;
             padding:1px 5px; margin:1px 1px 0 0; }

/* ── HUD COMPACTO (barra horizontal) ── */
.hud-bar { display:flex; gap:6px; margin-bottom:8px; align-items:stretch; }
.hud-chip { flex:1; background:#FAF6F0; border:1px solid #CBD5E1; border-radius:8px;
            padding:5px 10px; display:flex; flex-direction:column; gap:1px; }
.hud-label { font-size:0.55rem!important; letter-spacing:0.12em!important; text-transform:uppercase!important;
             color:#94A3B8!important; font-weight:800!important; }
.hud-value { font-size:0.88rem!important; color:#0F172A!important; font-weight:800!important; white-space:nowrap; }

/* ── BARRA DEL RÍO ── */
.rio-bar { background:#FAF6F0; border:1px solid #CBD5E1; border-radius:8px;
           padding:5px 12px; margin-bottom:6px; display:flex; align-items:center; gap:10px; }
.rio-label { font-size:0.58rem!important; font-weight:800!important; letter-spacing:0.12em!important;
             text-transform:uppercase!important; color:#8B0000!important; white-space:nowrap; }
.rio-track { font-size:1.05rem; letter-spacing:0.04em; line-height:1; }

/* ── PROGRESS BAR ── */
[data-testid="stProgress"] { margin-bottom:8px!important; }
[data-testid="stProgress"] > div > div { background:#8B0000!important; border-radius:2px!important; }
[data-testid="stProgress"] > div { background:#DDD8D2!important; border-radius:2px!important; height:4px!important; }

/* ── TARJETA INECUACIÓN ── */
.ineq-card { background:#FAF6F0; border:1px solid #CBD5E1; border-left:4px solid #8B0000;
             border-radius:0 10px 10px 0; padding:8px 16px 6px; margin-bottom:10px; }
.ineq-badge { display:inline-block; background:#8B0000; color:#FFF5F0!important;
              font-size:0.6rem!important; font-weight:800!important; letter-spacing:0.11em!important;
              text-transform:uppercase!important; padding:2px 8px; border-radius:3px; margin-bottom:5px; }

/* ── DOTS DE PASO ── */
.paso-dot-row { display:flex; gap:5px; margin-bottom:8px; align-items:center; }
.paso-dot { width:7px; height:7px; border-radius:50%; background:#CBD5E1; }
.paso-dot-active { background:#8B0000!important; box-shadow:0 0 5px rgba(139,0,0,0.45)!important; }
.paso-dot-done { background:#94A3B8!important; }

/* ── BOTONES GLOBALES ── */
.stButton > button { font-family:'Nunito',sans-serif!important; font-weight:800!important;
    font-size:0.88rem!important; background:#FAF6F0!important; color:#0F172A!important;
    border:1.5px solid #CBD5E1!important; border-radius:9px!important; padding:8px 12px!important;
    transition:all 0.13s ease!important; }
.stButton > button:hover { background:#8B0000!important; border-color:#8B0000!important;
    color:#FFFFFF!important; box-shadow:0 2px 10px rgba(139,0,0,0.2)!important; transform:translateY(-1px)!important; }

/* ── OPCIONES ── */
.opt-btn { background:#FAF6F0; border:1.5px solid #CBD5E1; border-radius:9px; padding:9px 12px;
           text-align:center; color:#0F172A!important; font-size:0.87rem!important; font-weight:700!important;
           min-height:46px; display:flex; align-items:center; justify-content:center; line-height:1.35; }
.opt-correct { background:#F0FDF4!important; border:2px solid #16A34A!important; color:#15803D!important; font-weight:800!important; }
.opt-selected-wrong { background:#FFF1F2!important; border:2px solid #DC2626!important; color:#B91C1C!important; font-weight:800!important; }
.opt-eliminated { border:1.5px dashed #CBD5E1; border-radius:9px; padding:9px 12px; text-align:center;
                  color:#CBD5E1!important; font-size:0.82rem!important; min-height:46px;
                  display:flex; align-items:center; justify-content:center; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius:8px!important; padding:9px 13px!important; margin-top:6px!important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] div { font-size:0.88rem!important; font-weight:700!important; }

/* ── PANTALLA FINAL ── */
.final-win { background:#8B0000; border-radius:14px; padding:20px 24px 16px; text-align:center; margin-bottom:12px; }
.final-win h2 { color:#FFFFFF!important; font-size:1.3rem!important; }
.final-win p  { color:#FFD5CC!important; font-weight:600!important; font-size:0.9rem!important; }
.final-card { background:#FAF6F0; border:1px solid #CBD5E1; border-radius:14px; padding:20px 22px 16px;
              text-align:center; margin-bottom:12px; }
.fail-panel { background:#FAF6F0; border:1px solid #CBD5E1; border-radius:10px; padding:14px 18px; margin-top:8px; }
.fail-intro { font-size:0.9rem!important; color:#0F172A!important; font-weight:800!important; margin-bottom:8px!important; }
.fail-item { display:flex; align-items:flex-start; gap:8px; padding:6px 0;
             border-bottom:1px solid #EDE8E2; font-size:0.88rem!important;
             color:#334155!important; line-height:1.4!important; font-weight:600!important; }
.fail-item:last-child { border-bottom:none; }
.fail-num { background:#8B0000; color:#FFFFFF!important; font-weight:800!important; font-size:0.7rem!important;
            border-radius:50%; min-width:20px; height:20px; display:flex; align-items:center;
            justify-content:center; flex-shrink:0; margin-top:1px; }

hr { border:none; border-top:1px solid #E2DDD8!important; margin:8px 0!important; }

/* Reducir gap entre elementos Streamlit */
.element-container { margin-bottom:0!important; }
[data-testid="stHorizontalBlock"] { gap:6px!important; }
/* Reducir espacio encima/debajo de latex */
.stMarkdown { margin-bottom:0!important; }
</style>
"""


def _gauss_bar(paso_global: int, total: int = 6) -> str:
    completados = paso_global
    restantes   = max(total - paso_global - 1, 0)
    return "🌿" + "🟩" * completados + "🐊" + "🟦" * restantes + "🏁"


def mostrar_juego():
    st.markdown(CSS, unsafe_allow_html=True)

    defaults = {
        "nivel": None, "ineq_idx": 0, "paso_idx": 0,
        "vidas": 3, "comodines": 2,
        "opcion_seleccionada": None, "resultado": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [], "opciones_shuffle": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ══════════════════════════════════════════════════
    # PANTALLA DE INICIO
    # ══════════════════════════════════════════════════
    if st.session_state.nivel is None:
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅ Inicio", use_container_width=True):
                st.session_state.pagina = "home"
                st.rerun()

        st.markdown("<p class='eyebrow'>Aventura Matemática</p>", unsafe_allow_html=True)
        st.markdown("<h1>Misión: Rescatar a Gauss</h1>", unsafe_allow_html=True)

        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(
                "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmp4bXFyMngwZTlib2I4aDg5b2V0NXBlbGV4YTkzbDJocHB5NDc1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/e5GHuG6BRgk9FEzU74/giphy.gif",
                use_container_width=True,
            )

        st.markdown("""
<div class="welcome-banner">
  <div class="gauss-title">El Río te espera, Estratega</div>
  <div class="gauss-story">Gauss es nuestro valiente cocodrilo y el malvado Río de las Dudas le arrebató su puente.
  Resuelve las inecuaciones para construir pilares perfectos. Cuida tus vidas y salva a Gauss.</div>
  <div class="rules-row">
    <span class="rules-chip">3 Niveles</span>
    <span class="rules-chip">2 Inecuaciones por Reto</span>
    <span class="rules-chip">❤️ 3 Vidas</span>
    <span class="rules-chip">🃏 2 Comodines 50/50</span>
  </div>
</div>""", unsafe_allow_html=True)

        niveles_meta = {
            1: {"nombre": "Misión 1: El Despertar", "stars": "⭐",
                "desc": "Inecuaciones lineales. Ideal para afinar la puntería lógica.",
                "tags": ["4x + 7 ≥ 2x − 3", "3x − 1 ≥ 3 + x"]},
            2: {"nombre": "Misión 2: El Laberinto", "stars": "⭐⭐",
                "desc": "Terreno Cuadrático. Descifra factores y mapas de signos.",
                "tags": ["x² − 6x + 8 < 0", "−x² − x + 6 < 0"]},
            3: {"nombre": "Misión 3: El Abismo", "stars": "⭐⭐⭐",
                "desc": "Fracciones peligrosas. Controla las restricciones.",
                "tags": ["4/(x−3) ≥ 5/(x+2)", "(−x−10)/(x+1) > −x−2"]},
        }

        cols = st.columns(3, gap="small")
        for i, (lvl, meta) in enumerate(niveles_meta.items()):
            with cols[i]:
                tags_html = "".join(f"<span class='nivel-tag'>{t}</span>" for t in meta["tags"])
                st.markdown(f"""
<div class="nivel-card">
  <div class="nivel-num">Nivel {lvl:02d}</div>
  <div class="nivel-name">{meta['nombre']}</div>
  <div class="nivel-stars">{meta['stars']}</div>
  <div class="nivel-desc">{meta['desc']}</div>
  <div style="margin-top:6px;">{tags_html}</div>
</div><div style="height:6px"></div>""", unsafe_allow_html=True)
                if st.button(f"Aceptar Reto {lvl}", key=f"sel_{lvl}", use_container_width=True):
                    _iniciar_nivel(lvl)
                    st.rerun()
        return

    # ══════════════════════════════════════════════════
    # PANTALLA FINAL
    # ══════════════════════════════════════════════════
    if st.session_state.juego_terminado:
        errores = st.session_state.historial_errores
        if not errores:
            st.balloons()
            st.markdown(f"""
<div class="final-win">
  <h2>LEYENDA. Misión {st.session_state.nivel} perfecta.</h2>
  <p>Gauss pasó al otro lado corriendo. Ni un solo rasguño, eres imparable.</p>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="final-card">
  <h2>Misión {st.session_state.nivel} completada</h2>
  <p style="color:#64748B!important;font-weight:700!important;">Gauss llegó sudando a la orilla. Revisa tu bitácora.</p>
</div>""", unsafe_allow_html=True)
            temas_vistos: list[str] = []
            for err in errores:
                tema = TEMAS_ERROR.get(tuple(err), "Tácticas generales de inecuaciones")
                if tema not in temas_vistos:
                    temas_vistos.append(tema)
            items_html = "".join(
                f"<div class='fail-item'><span class='fail-num'>{j+1}</span><span>{t}</span></div>"
                for j, t in enumerate(temas_vistos)
            )
            st.markdown(f"<div class='fail-panel'><div class='fail-intro'>Bitácora de entrenamiento:</div>{items_html}</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWpodXNsZWl2aDZheHg2YnVzNGhkb3pxeGhveHNiNnZwbzI5NDU2bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HumSLHE7SgXETxBet5/giphy.gif", use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Volver a niveles", use_container_width=True):
                st.session_state.nivel = None; st.session_state.juego_terminado = False; st.rerun()
        with c2:
            if st.button("Repetir reto", use_container_width=True):
                _reiniciar_nivel(); st.rerun()
        return

    # ══════════════════════════════════════════════════
    # JUEGO ACTIVO
    # ══════════════════════════════════════════════════
    nivel    = st.session_state.nivel
    ineq_idx = st.session_state.ineq_idx
    paso_idx = st.session_state.paso_idx
    ineq     = INECUACIONES[nivel][ineq_idx]
    paso     = ineq["pasos"][paso_idx]
    total_p  = len(ineq["pasos"])
    paso_global = ineq_idx * 3 + paso_idx

    # ── GAME OVER ──
    if st.session_state.vidas <= 0:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXlhcGw1NnM3dG42MWtjYnZlbWE1aThkN20wbHBndTlzeW9rMWljYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PB82BUQk9r9h6vgzPv/giphy.gif", use_container_width=True)
        st.error("Gauss cayó al agua. Sin energía.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Revivir", use_container_width=True): _reiniciar_nivel(); st.rerun()
        with c2:
            if st.button("Menú principal", use_container_width=True): st.session_state.nivel = None; st.rerun()
        return

    # ── HUD COMPACTO: todo en una sola fila ──
    nombres = {1: "Básico", 2: "Intermedio", 3: "Experto"}
    vidas_ico = ("❤️" * st.session_state.vidas) + ("🖤" * (3 - st.session_state.vidas))
    comod_str = f"🃏 ×{st.session_state.comodines}" if st.session_state.comodines > 0 else "🃏 Agotados"
    err_count = len(st.session_state.historial_errores)

    st.markdown(f"""
<div class="hud-bar">
  <div class="hud-chip">
    <span class="hud-label">Misión</span>
    <span class="hud-value">{nivel} · {nombres[nivel]}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Vidas</span>
    <span class="hud-value">{vidas_ico}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Comodín</span>
    <span class="hud-value">{comod_str}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Errores</span>
    <span class="hud-value">{"⚡ " + str(err_count) if err_count else "✨ Invicto"}</span>
  </div>
</div>""", unsafe_allow_html=True)

    # ── BARRA RÍO + PROGRESO en la misma fila ──
    st.markdown(f"""
<div class="rio-bar">
  <span class="rio-label">Gauss →</span>
  <span class="rio-track">{_gauss_bar(paso_global)}</span>
</div>""", unsafe_allow_html=True)
    st.progress(paso_global / 6)

    # ── BOTÓN HUIR (pequeño, discreto) ──
    col_huir, col_esp = st.columns([1.4, 4])
    with col_huir:
        if st.button("⬅ Cambiar nivel", key="back_nivel"):
            st.session_state.nivel = None; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── INECUACIÓN + DOTS en la misma línea ──
    dots = "".join(
        "<div class='paso-dot"
        + (" paso-dot-done'" if d < paso_idx else " paso-dot-active'" if d == paso_idx else "'")
        + "></div>"
        for d in range(total_p)
    )
    st.markdown(
        f"<div class='paso-dot-row'>{dots}"
        f"<span style='font-size:0.68rem;color:#94A3B8;margin-left:5px;font-weight:800;'>"
        f"Paso {paso['num']} de {total_p} · {ineq['titulo']}</span></div>",
        unsafe_allow_html=True,
    )

    ya_respondido = st.session_state.resultado is not None
    correcto      = st.session_state.resultado == "correcto"
    ecuacion_display = paso["expresion"] if (ya_respondido and correcto) else paso["expresion_dinamica"]

    # ── ECUACIÓN + PREGUNTA LADO A LADO ──
    col_eq, col_q = st.columns([1, 1.6])
    with col_eq:
        st.markdown(f"""
<div class="ineq-card">
  <span class="ineq-badge">{ineq_idx + 1}/2 · {paso['descripcion']}</span>
""", unsafe_allow_html=True)
        st.latex(ecuacion_display)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_q:
        st.markdown(
            f"<p style='font-weight:700;font-size:0.95rem;color:#1E293B!important;"
            f"margin-top:8px;line-height:1.5;'>{paso['pregunta']}</p>",
            unsafe_allow_html=True,
        )

        # Comodín dentro de la columna de pregunta
        if not ya_respondido and st.session_state.comodines > 0 and st.session_state.opcion_oculta is None:
            if st.button(f"🃏 Usar comodín ({st.session_state.comodines} restante{'s' if st.session_state.comodines > 1 else ''})", key="comodin"):
                paso_key = (nivel, ineq_idx, paso_idx)
                if st.session_state.opciones_shuffle and st.session_state.opciones_shuffle.get("key") == paso_key:
                    _usar_comodin(st.session_state.opciones_shuffle["opciones"], st.session_state.opciones_shuffle["correcta"])
                st.rerun()

    # ── OPCIONES ──
    paso_key = (nivel, ineq_idx, paso_idx)
    if st.session_state.opciones_shuffle is None or \
       st.session_state.opciones_shuffle.get("key") != paso_key:
        textos_orig    = list(paso["opciones"].values())
        correcta_texto = paso["opciones"][paso["correcta"]]
        textos_mezclados = textos_orig[:]
        random.shuffle(textos_mezclados)
        letras_nuevas  = ["A", "B", "C"]
        nueva_correcta = letras_nuevas[textos_mezclados.index(correcta_texto)]
        st.session_state.opciones_shuffle = {
            "key": paso_key,
            "opciones": dict(zip(letras_nuevas, textos_mezclados)),
            "correcta": nueva_correcta,
        }

    shuffle_data  = st.session_state.opciones_shuffle
    opciones_show = shuffle_data["opciones"]
    correcta_now  = shuffle_data["correcta"]
    oculta        = st.session_state.opcion_oculta
    cols_opt      = st.columns(3, gap="small")

    for i, (letra, texto) in enumerate(opciones_show.items()):
        with cols_opt[i]:
            if oculta and letra == oculta:
                st.markdown("<div class='opt-eliminated'>🃏 Eliminada</div>", unsafe_allow_html=True)
                continue
            if not ya_respondido:
                if st.button(f"**{letra}.** {texto}", key=f"opt_{letra}", use_container_width=True):
                    _procesar_respuesta(letra, correcta_now); st.rerun()
            else:
                es_sel = st.session_state.opcion_seleccionada == letra
                es_ok  = correcta_now == letra
                if (es_sel and correcto) or (es_ok and not correcto): cls = "opt-correct"
                elif es_sel: cls = "opt-selected-wrong"
                else: cls = "opt-btn"
                st.markdown(f"<div class='{cls}'><strong>{letra}.</strong> {texto}</div>", unsafe_allow_html=True)

    # ── FEEDBACK ──
    if ya_respondido:
        if correcto:
            st.success(f"✅ {paso['ok']}")
            if st.button("Siguiente movimiento →", use_container_width=True):
                _avanzar_paso(); st.rerun()
        else:
            st.error(f"❌ {paso['err']}")
            if st.button("Reagruparse e intentar de nuevo", use_container_width=True):
                st.session_state.update({
                    "resultado": None, "opcion_seleccionada": None,
                    "opcion_oculta": None, "opciones_shuffle": None,
                })
                st.rerun()


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def _iniciar_nivel(lvl):
    st.session_state.update({
        "nivel": lvl, "ineq_idx": 0, "paso_idx": 0,
        "vidas": 3, "comodines": 2,
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [], "opciones_shuffle": None,
    })

def _reiniciar_nivel():
    st.session_state.update({
        "ineq_idx": 0, "paso_idx": 0, "vidas": 3, "comodines": 2,
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [], "opciones_shuffle": None,
    })

def _procesar_respuesta(letra_elegida, correcta):
    st.session_state.opcion_seleccionada = letra_elegida
    nivel, ineq_idx, paso_idx = st.session_state.nivel, st.session_state.ineq_idx, st.session_state.paso_idx
    if letra_elegida == correcta:
        st.session_state.resultado = "correcto"
    else:
        st.session_state.resultado = "incorrecto"
        st.session_state.vidas -= 1
        err_key = [nivel, ineq_idx, paso_idx]
        if err_key not in st.session_state.historial_errores:
            st.session_state.historial_errores.append(err_key)

def _usar_comodin(opciones_show, correcta):
    candidatas = [k for k in opciones_show if k != correcta and k != st.session_state.opcion_oculta]
    if candidatas:
        st.session_state.opcion_oculta = random.choice(candidatas)
        st.session_state.comodines -= 1

def _avanzar_paso():
    st.session_state.update({
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "opciones_shuffle": None,
    })
    nivel, ineq_idx, paso_idx = st.session_state.nivel, st.session_state.ineq_idx, st.session_state.paso_idx
    if paso_idx + 1 < len(INECUACIONES[nivel][ineq_idx]["pasos"]):
        st.session_state.paso_idx += 1
    elif ineq_idx + 1 < len(INECUACIONES[nivel]):
        st.session_state.ineq_idx += 1
        st.session_state.paso_idx = 0
    else:
        st.session_state.juego_terminado = True

if __name__ == "__main__":
    st.set_page_config(page_title="Misión: Rescatar a Gauss", layout="centered")
    mostrar_juego()