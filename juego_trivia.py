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
                    "ok": "Misión cumplida. Pasaste el 2x restando y el 7 al otro lado restando impecablemente.",
                    "err": "Casi te muerde una piraña. Recuerda la regla de oro: al cruzar el puente del igual o desigualdad, los signos cambian (El 7 pasa restando).",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: El Despeje Definitivo",
                    "expresion_dinamica": r"2x \ge -10",
                    "expresion": r"x \ge \frac{-10}{2} \implies x \ge -5",
                    "pregunta": "Al dividir todo entre 2 (que es un número positivo), ¿qué le pasa a la desigualdad?",
                    "opciones": {
                        "A": "x ≥ −5 · Mantiene su rumbo",
                        "B": "x ≤ −5 · El sentido se invierte",
                        "C": "x ≥ 5 · Cambia el signo"
                    },
                    "correcta": "A",
                    "ok": "Justo en el blanco. Como el 2 es tu aliado (positivo), la desigualdad no se acobarda y mantiene su dirección. Avanzamos.",
                    "err": "Caíste en la trampa. La desigualdad SOLO se invierte si divides entre un número NEGATIVO. El 2 es positivo, no tengas miedo de mantener el signo.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: Forjando el Intervalo",
                    "expresion_dinamica": r"x \ge -5",
                    "expresion": r"S: x \in [-5, +\infty[",
                    "pregunta": "Último paso: x ≥ −5. Tienes el símbolo 'mayor o igual', así que debes proteger el −5. ¿Qué intervalo eliges?",
                    "opciones": {"A": "S: x ∈ ]−∞, −5]", "B": "S: x ∈ [−5, +∞[", "C": "S: x ∈ ]−5, +∞["},
                    "correcta": "B",
                    "ok": "Misión cumplida. El corchete abraza al −5 (cerrado) y el infinito vuela libre.",
                    "err": "Te desviaste un poco. El símbolo '≥' incluye al −5, así que necesitas usar un corchete CERRADO [ para protegerlo.",
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
                    "pregunta": "Pasa la x restando a la izquierda y el −1 sumando a la derecha. ¿Cómo nos queda el terreno?",
                    "opciones": {"A": "2x ≥ 4", "B": "4x ≥ 2", "C": "2x ≤ 4"},
                    "correcta": "A",
                    "ok": "Movimiento de Maestro. 3x − x = 2x y 3 + 1 = 4.",
                    "err": "Resbalón. Verifica tus tropas: la x de la derecha pasa a RESTAR, y el −1 de la izquierda pasa a SUMAR.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: El Golpe de Gracia",
                    "expresion_dinamica": r"2x \ge 4",
                    "expresion": r"x \ge \frac{4}{2} \implies x \ge 2",
                    "pregunta": "Divide ambos lados entre 2. ¿Logrará cambiar el rumbo de la desigualdad?",
                    "opciones": {"A": "x ≤ 2", "B": "x > 2", "C": "x ≥ 2"},
                    "correcta": "C",
                    "ok": "Justo en el blanco. 4 ÷ 2 = 2 y el signo se mantiene fuerte porque dividiste por un positivo.",
                    "err": "Te desviaste un poco. Dividir entre un número positivo jamás cambia la orientación. Mantén el símbolo de ≥ apuntando igual.",
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
                    "err": "No te quedes a medias. Vamos hacia los mayores (+∞), y el 2 va súper abrazado (corchete cerrado) porque lleva la igualdad.",
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
                    "pregunta": "Necesitas dos números que multiplicados den +8 y sumados den −6. ¿Cuál es la factorización?",
                    "opciones": {"A": "(x − 8)(x + 1) < 0", "B": "(x − 4)(x − 2) < 0", "C": "(x + 4)(x + 2) < 0"},
                    "correcta": "B",
                    "ok": "Mente brillante. −4 y −2 encajan a la perfección.",
                    "err": "Te desviaste un poco. Para que la suma sea negativa y la multiplicación positiva, OBLIGATORIAMENTE tus dos números deben ser negativos. Piénsalo bien.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Buscando los Ceros",
                    "expresion_dinamica": r"(x - 4)(x - 2) < 0",
                    "expresion": r"\text{Ceros: } x = 2 \text{ y } x = 4 \text{ (abiertos)}",
                    "pregunta": "Despeja tus factores. Pero cuidado, la inecuación es < estricta (sin igualdad). ¿Cómo quedan los ceros?",
                    "opciones": {
                        "A": "x = 2 y x = 4, ABIERTOS",
                        "B": "x = −2 y x = −4, ABIERTOS",
                        "C": "x = 2 y x = 4, CERRADOS"
                    },
                    "correcta": "A",
                    "ok": "Esquivaste la trampa. Despejaste los signos perfecto y los dejaste abiertos.",
                    "err": "Resbalón. Al despejar, el −4 se vuelve +4. Además, como es < estricto (no tiene rayita abajo), los puntos van ABIERTOS.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: La Lectura del Mapa",
                    "expresion_dinamica": r"\text{Ceros abiertos: } x = 2 \text{ y } x = 4",
                    "expresion": r"S: x \in ]2, 4[",
                    "pregunta": "Tu producto es NEGATIVO (< 0) justo en el medio de tus ceros. ¿Cuál es el camino seguro para Gauss?",
                    "opciones": {
                        "A": "S: x ∈ ]−∞, 2[ ∪ ]4, +∞[",
                        "B": "S: x ∈ [2, 4]",
                        "C": "S: x ∈ ]2, 4["
                    },
                    "correcta": "C",
                    "ok": "Qué visión. Identificaste la zona central negativa con corchetes abiertos perfectos. Nivel Intermedio completado con honores.",
                    "err": "Te fuiste directo a la trampa. Te interesa la zona donde el resultado es NEGATIVO (< 0), que en este caso es el puro centro, no los bordes.",
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
                    "pregunta": "Tienes un coeficiente negativo al frente. Factorizando cruzado, ¿qué escudos te protegen mejor?",
                    "opciones": {
                        "A": "(x + 2)(x − 3) < 0",
                        "B": "(−x + 2)(x + 3) < 0",
                        "C": "(−x − 2)(x − 3) < 0"
                    },
                    "correcta": "B",
                    "ok": "Cálculo frío y preciso. Al multiplicar cruzado cuadra exactamente a −x²−x+6.",
                    "err": "Caíste en la trampa. Si multiplicas las otras opciones no llegarás a la ecuación original. Verifica multiplicando término a término.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Cazando los Ceros",
                    "expresion_dinamica": r"(-x + 2)(x + 3) < 0",
                    "expresion": r"\text{Ceros: } x = -3 \text{ y } x = 2 \text{ (abiertos)}",
                    "pregunta": "Hora de despejar. Recuerda que uno de los factores tiene la 'x' negativa. ¿Cuáles son tus ceros?",
                    "opciones": {
                        "A": "x = 2 y x = 3, ABIERTOS",
                        "B": "x = −2 y x = 3, CERRADOS",
                        "C": "x = 2 y x = −3, ABIERTOS"
                    },
                    "correcta": "C",
                    "ok": "Cálculo frío y preciso. Al despejar −x+2=0 pasas la x y te queda x=2 positivo.",
                    "err": "Error de coordenadas. Al despejar −x+2=0, pasas el −x al otro lado y queda x=2 (positivo). Y como es <, jamás pueden ir cerrados.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: El Territorio Exterior",
                    "expresion_dinamica": r"\text{Ceros abiertos: } x = -3 \text{ y } x = 2",
                    "expresion": r"S: x \in ]-\infty, -3[ \cup ]2, +\infty[",
                    "pregunta": "Por tener coeficiente negativo, esta vez el producto es NEGATIVO (< 0) en los bordes exteriores. ¿Qué camino tomas?",
                    "opciones": {
                        "A": "S: x ∈ ]−∞, −3[ ∪ ]2, +∞[",
                        "B": "S: x ∈ ]−3, 2[",
                        "C": "S: x ∈ ]−∞, −2[ ∪ ]3, +∞["
                    },
                    "correcta": "A",
                    "ok": "Épico. Dominaste la parábola invertida como todo un experto. Agarraste las dos zonas exteriores perfectamente.",
                    "err": "Al ser invertida, el centro es positivo. Tú buscas los bordes porque la inecuación dice MENOR (<) que cero.",
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
                    "pregunta": "Pasa todo a la izquierda. Con un MCM de (x−3)(x+2), ¿cómo construyes tu nuevo numerador?",
                    "opciones": {
                        "A": "4(x−3) − 5(x+2)",
                        "B": "4 − 5 (Resta directa)",
                        "C": "4(x+2) − 5(x−3)"
                    },
                    "correcta": "C",
                    "ok": "Mente brillante. Cruzaste los factores con sus numeradores opuestos de forma perfecta.",
                    "err": "Estructura inestable. NO PUEDES restar numeradores si los denominadores son diferentes. Cada número arriba debe multiplicarse por el bloque que le falta de abajo.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Fuego de Cobertura (Distribución)",
                    "expresion_dinamica": r"\frac{4(x+2) - 5(x-3)}{(x-3)(x+2)} \ge 0",
                    "expresion": r"\frac{-x + 23}{(x-3)(x+2)} \ge 0",
                    "pregunta": "Multiplica con cuidado. Al distribuir el −5 por el (x−3)... ojo con los signos. ¿Qué queda?",
                    "opciones": {"A": "−x − 7", "B": "9x − 7", "C": "−x + 23"},
                    "correcta": "C",
                    "ok": "Desactivaste la bomba. −5 por −3 es +15 positivo. Agrupaste genial a −x + 23.",
                    "err": "Te desviaste un poco. Multiplicaste mal el último término: un negativo por un negativo (−5 × −3) te da un número POSITIVO (+15). Recalcula.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: El Juicio Final de las Restricciones",
                    "expresion_dinamica": r"\frac{-x + 23}{(x-3)(x+2)} \ge 0",
                    "expresion": r"S: x \in ]-\infty, -2[ \cup ]3, 23]",
                    "pregunta": "El cero de arriba (23) se cierra por el '≥'. Pero las restricciones de abajo (−2 y 3) NUNCA se cierran. ¿Cuál es tu respuesta (≥0)?",
                    "opciones": {
                        "A": "S: x ∈ ]−2, 3[ ∪ ]23, +∞[",
                        "B": "S: x ∈ ]−∞, −2[ ∪ ]3, 23]",
                        "C": "S: x ∈ ]−∞, −2] ∪ [3, 23]"
                    },
                    "correcta": "B",
                    "ok": "Victoria total. Dominaste la regla de oro: las restricciones de abajo siempre van abiertas.",
                    "err": "Te hundiste en el barro. Regla de vida: los ceros del DENOMINADOR (abajo) NUNCA llevan corchete cerrado, porque dividir por cero explota el universo matemático.",
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
                    "pregunta": "Estás frente a la cueva mayor. Para no arruinar tus casos de signos, ¿cuál debe ser tu primer paso estratégico?",
                    "opciones": {
                        "A": "Borrar el denominador",
                        "B": "Pasar el (x+1) a multiplicar al otro lado",
                        "C": "Pasar TODO el bloque derecho restando y armar el MCM"
                    },
                    "correcta": "C",
                    "ok": "Esquivaste la trampa. Sabes perfectamente que multiplicar cruzado en inecuaciones es trampa mortal. Avanzamos.",
                    "err": "Te fuiste directo a la trampa. Pasar un denominador con variables multiplicando al otro lado te hará perder todos tus casos de signos. Pasa el bloque restando mejor.",
                },
                {
                    "num": 2,
                    "descripcion": "Fase 2: Limpiando la Caverna",
                    "expresion_dinamica": r"\frac{-x-10 - [(-x-2)(x+1)]}{x+1} > 0",
                    "expresion": r"\frac{(x+4)(x-2)}{x+1} > 0",
                    "pregunta": "Resolviste el corchete de arriba y te quedó x²+2x−8. Es hora de factorizar rápido. ¿Qué factores dan +2 de suma?",
                    "opciones": {
                        "A": "(x+4)(x−2)",
                        "B": "(x+8)(x−1)",
                        "C": "(x−4)(x+2)"
                    },
                    "correcta": "A",
                    "ok": "Golpe certero. +4 y −2 multiplicados dan −8, y sumados dan tu ansiado +2.",
                    "err": "Espada desviada. Tienes que buscar factores que SUMADOS te den +2 (positivo). Tu opción da un resultado negativo al medio. Vuelve a intentar.",
                },
                {
                    "num": 3,
                    "descripcion": "Fase 3: El Salto a la Libertad",
                    "expresion_dinamica": r"\frac{(x+4)(x-2)}{x+1} > 0",
                    "expresion": r"S: x \in ]-4, -1[ \cup ]2, +\infty[",
                    "pregunta": "Tienes ceros en −4 y 2, y restricción en −1. Como es MAYOR ESTRICTO (>), todo va abierto. ¿A qué luz sigues?",
                    "opciones": {
                        "A": "S: x ∈ [−4, −1] ∪ [2, +∞[",
                        "B": "S: x ∈ ]−4, −1[ ∪ ]2, +∞[",
                        "C": "S: x ∈ ]−∞, −4[ ∪ ]−1, 2["
                    },
                    "correcta": "B",
                    "ok": "Victoria total. Corchetes abiertos en su lugar, tramos positivos perfectos. Superaste el reto.",
                    "err": "Cuidado con la puerta falsa. Si el símbolo es > (estricto sin rayita de igual), JAMÁS puedes usar un corchete cerrado. Revisa tus opciones.",
                },
            ],
        },
    ],
}

# ══════════════════════════════════════════════════════════════
# TEMAS DE FALLO
# ══════════════════════════════════════════════════════════════
TEMAS_ERROR = {
    (1, 0, 0): "Dominio de signos al cruzar el 'igual' (Transposición de términos)",
    (1, 0, 1): "Las desigualdades solo cambian al dividir por negativos",
    (1, 0, 2): "Diferenciar intervalos cerrados [ de los abiertos ]",
    (1, 1, 0): "Agrupación táctica: Variables a la izquierda, números a la derecha",
    (1, 1, 1): "Despejes con coeficientes positivos (el signo se mantiene)",
    (1, 1, 2): "Hacia donde apunta el infinito (+∞ o -∞)",
    (2, 0, 0): "Factorización de trinomios y dominio de la ley de signos",
    (2, 0, 1): "Saber cuándo un punto es abierto o cerrado",
    (2, 0, 2): "Lectura del Mapa de Signos: Hallar las zonas negativas entre los ceros",
    (2, 1, 0): "Factorizar trinomios que inician con coeficiente negativo",
    (2, 1, 1): "Extraer raíces de binomios con la 'x' negativa",
    (2, 1, 2): "Reconocer que las zonas exteriores son negativas si la x² es negativa",
    (3, 0, 0): "Creación de M.C.M y cruce correcto de términos",
    (3, 0, 1): "Multiplicaciones de dos números negativos (da positivo)",
    (3, 0, 2): "Ley Suprema: Las restricciones del denominador NUNCA van cerradas",
    (3, 1, 0): "Regla de Oro Racional: NUNCA multiplicar cruzado en inecuaciones",
    (3, 1, 1): "Factorizar trinomios luego de desarrollar corchetes",
    (3, 1, 2): "Elegir múltiples tramos positivos en tablas grandes",
}

# ══════════════════════════════════════════════════════════════
# CSS — sin cambios
# ══════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], section.main, .main .block-container {
    background-color: #F5F0EB !important;
    color: #0F172A !important;
    font-family: 'Nunito', 'Segoe UI', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #EDE8E2 !important;
    border-right: 1px solid #CBD5E1 !important;
}
.main .block-container { padding-top: 1.4rem !important; max-width: 800px !important; }

h1 { font-weight: 900 !important; font-size: 2rem !important; color: #8B0000 !important; letter-spacing: -0.02em !important; margin-bottom: 4px !important; text-align: center; }
h2 { font-weight: 800 !important; font-size: 1.45rem !important; color: #0F172A !important; letter-spacing: -0.01em !important; }
h3 { font-weight: 700 !important; font-size: 1.15rem !important; color: #1E293B !important; }
p, li, label { color: #334155 !important; font-size: 1rem !important; line-height: 1.65 !important; font-weight: 400 !important; }
.eyebrow { font-size: 0.68rem !important; font-weight: 800 !important; letter-spacing: 0.16em !important; text-transform: uppercase !important; color: #8B0000 !important; margin-bottom: 3px !important; }

.welcome-banner { background: #8B0000; border-radius: 18px; padding: 26px 30px 22px; margin-bottom: 22px; position: relative; overflow: hidden; }
.gauss-title { font-size: 1.55rem !important; font-weight: 900 !important; color: #FFF5F0 !important; margin-bottom: 8px !important; }
.gauss-story { font-size: 0.97rem !important; color: #FFD5CC !important; line-height: 1.6 !important; font-weight: 600 !important; }
.rules-row { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.rules-chip { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 8px; padding: 5px 12px; font-size: 0.8rem !important; color: #FFE8E0 !important; font-weight: 700 !important; white-space: nowrap; }

.nivel-card { background: #FAF6F0; border: 1px solid #CBD5E1; border-radius: 14px; padding: 18px 16px 14px; height: 100%; transition: all 0.18s ease; position: relative; overflow: hidden; }
.nivel-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: #8B0000; border-radius: 14px 14px 0 0; }
.nivel-card:hover { border-color: #8B0000; box-shadow: 0 6px 20px rgba(139,0,0,0.14); transform: translateY(-2px); }
.nivel-num { font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important; font-weight: 700 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; color: #8B0000 !important; margin-bottom: 5px !important; }
.nivel-name { font-size: 1rem !important; font-weight: 800 !important; color: #0F172A !important; margin-bottom: 5px !important; }
.nivel-stars { font-size: 0.95rem !important; margin-bottom: 6px !important; }
.nivel-desc { font-size: 0.84rem !important; color: #64748B !important; line-height: 1.4 !important; margin-bottom: 10px !important; }
.nivel-tag { display: inline-block; font-family: 'Space Mono', monospace !important; font-size: 0.68rem !important; color: #64748B !important; background: #F1EDE8; border: 1px solid #CBD5E1; border-radius: 4px; padding: 2px 6px; margin: 2px 2px 0 0; }

.rio-container { background: #FAF6F0; border: 1px solid #CBD5E1; border-radius: 10px; padding: 9px 16px 7px; margin-bottom: 8px; }
.rio-label { font-size: 0.65rem !important; font-weight: 800 !important; letter-spacing: 0.13em !important; text-transform: uppercase !important; color: #8B0000 !important; margin-bottom: 4px !important; }
.rio-track { font-size: 1.2rem; letter-spacing: 0.06em; line-height: 1; }

[data-testid="stProgress"] { margin-bottom: 10px !important; }
[data-testid="stProgress"] > div > div { background: #8B0000 !important; border-radius: 3px !important; }
[data-testid="stProgress"] > div { background: #DDD8D2 !important; border-radius: 3px !important; height: 5px !important; }

.hud-row { display: flex; gap: 8px; margin-bottom: 12px; }
.hud-chip { flex: 1; background: #FAF6F0; border: 1px solid #CBD5E1; border-radius: 10px; padding: 7px 11px; display: flex; flex-direction: column; gap: 1px; }
.hud-label { font-size: 0.58rem !important; letter-spacing: 0.13em !important; text-transform: uppercase !important; color: #94A3B8 !important; font-weight: 800 !important; }
.hud-value { font-size: 0.95rem !important; color: #0F172A !important; font-weight: 800 !important; }

.stButton > button { font-family: 'Nunito', sans-serif !important; font-weight: 800 !important; font-size: 0.97rem !important; background: #FAF6F0 !important; color: #0F172A !important; border: 1.5px solid #CBD5E1 !important; border-radius: 10px !important; padding: 10px 16px !important; transition: all 0.14s ease !important; }
.stButton > button:hover { background: #8B0000 !important; border-color: #8B0000 !important; color: #FFFFFF !important; box-shadow: 0 3px 14px rgba(139,0,0,0.22) !important; transform: translateY(-1px) !important; }

.ineq-card { background: #FAF6F0; border: 1px solid #CBD5E1; border-left: 5px solid #8B0000; border-radius: 0 12px 12px 0; padding: 12px 22px 10px; margin-bottom: 14px; }
.ineq-badge { display: inline-block; background: #8B0000; color: #FFF5F0 !important; font-size: 0.66rem !important; font-weight: 800 !important; letter-spacing: 0.13em !important; text-transform: uppercase !important; padding: 3px 9px; border-radius: 4px; margin-bottom: 8px; }

.paso-dot-row { display: flex; gap: 7px; margin-bottom: 12px; align-items: center; }
.paso-dot { width: 9px; height: 9px; border-radius: 50%; background: #CBD5E1; }
.paso-dot-active { background: #8B0000 !important; box-shadow: 0 0 6px rgba(139,0,0,0.45) !important; }
.paso-dot-done { background: #94A3B8 !important; }

.opt-btn { background: #FAF6F0; border: 1.5px solid #CBD5E1; border-radius: 10px; padding: 11px 14px; text-align: center; color: #0F172A !important; font-size: 0.93rem !important; font-weight: 700 !important; min-height: 52px; display: flex; align-items: center; justify-content: center; line-height: 1.4; }
.opt-correct { background: #F0FDF4 !important; border: 2px solid #16A34A !important; color: #15803D !important; font-weight: 800 !important; }
.opt-selected-wrong { background: #FFF1F2 !important; border: 2px solid #DC2626 !important; color: #B91C1C !important; font-weight: 800 !important; }
.opt-eliminated { border: 1.5px dashed #CBD5E1; border-radius: 10px; padding: 11px 14px; text-align: center; color: #CBD5E1 !important; font-size: 0.85rem !important; min-height: 52px; display: flex; align-items: center; justify-content: center; }

[data-testid="stAlert"] { border-radius: 10px !important; padding: 12px 16px !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] div { font-size: 0.97rem !important; font-weight: 700 !important; color: inherit !important; }

.final-win { background: #8B0000; border-radius: 16px; padding: 28px 28px 22px; text-align: center; margin-bottom: 16px; color: #fff; }
.final-win h2 { color: #FFFFFF !important; }
.final-win p  { color: #FFD5CC !important; font-weight: 600 !important; }

.final-card { background: #FAF6F0; border: 1px solid #CBD5E1; border-radius: 16px; padding: 26px 26px 20px; text-align: center; margin-bottom: 14px; }
.fail-panel { background: #FAF6F0; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px 22px; text-align: left; margin-top: 10px; }
.fail-intro { font-size: 1rem !important; color: #0F172A !important; font-weight: 800 !important; margin-bottom: 12px !important; }
.fail-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #EDE8E2; font-size: 0.95rem !important; color: #334155 !important; line-height: 1.5 !important; font-weight: 600 !important; }
.fail-item:last-child { border-bottom: none; }
.fail-num { background: #8B0000; color: #FFFFFF !important; font-weight: 800 !important; font-size: 0.75rem !important; border-radius: 50%; min-width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px; }

hr { border: none; border-top: 1px solid #E2DDD8 !important; margin: 14px 0 !important; }
</style>
"""


# ══════════════════════════════════════════════════════════════
# HELPER — barra de progreso con emojis
# paso_global va de 0 a 5 (6 pasos totales: 2 inecuaciones × 3 pasos)
# Antes del cocodrilo: pasos ya completados  → 🟩
# El cocodrilo en su posición actual          → 🐊
# Pasos que quedan por delante               → 🟦
# ══════════════════════════════════════════════════════════════
def _gauss_bar(paso_global: int, total: int = 6) -> str:
    completados = paso_global          # pasos ya hechos (antes del croco)
    restantes   = total - paso_global - 1  # pasos que faltan (después del croco)
    restantes   = max(restantes, 0)

    barra = (
        "🌿"
        + "🟩" * completados
        + "🐊"
        + "🟦" * restantes
        + "🏁"
    )
    return barra


# ══════════════════════════════════════════════════════════════
# JUEGO PRINCIPAL
# ══════════════════════════════════════════════════════════════
def mostrar_juego():
    st.markdown(CSS, unsafe_allow_html=True)

    defaults = {
        "nivel": None, "ineq_idx": 0, "paso_idx": 0,
        "vidas": 3, "comodines": 2,
        "opcion_seleccionada": None, "resultado": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [],
        "opciones_shuffle": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ══════════════════════════════════════════════════════
    # PANTALLA DE INICIO
    # ══════════════════════════════════════════════════════
    if st.session_state.nivel is None:
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
  <div class="gauss-story">
    Gauss es nuestro valiente cocodrilo matemático, y el malvado Río de las Dudas le arrebató su puente.
    Para ayudarlo a llegar al otro lado a salvo, necesitas construir pilares perfectos resolviendo las inecuaciones.
    Usa tu astucia lógica para despejar los misterios, evita trampas de signos y cuida tus vidas. Ponte la capa y salva a Gauss.
  </div>
  <div class="rules-row">
    <span class="rules-chip">3 Niveles</span>
    <span class="rules-chip">2 Inecuaciones por Reto</span>
    <span class="rules-chip">3 Vidas Extra</span>
    <span class="rules-chip">2 Comodines 50/50</span>
  </div>
</div>""", unsafe_allow_html=True)

        niveles_meta = {
            1: {
                "nombre": "Misión 1: El Despertar",
                "stars": "⭐",
                "desc": "Inecuaciones lineales. Ideal para calentar tu cerebro y afinar la puntería lógica.",
                "tags": ["4x + 7 ≥ 2x − 3", "3x − 1 ≥ 3 + x"],
            },
            2: {
                "nombre": "Misión 2: El Laberinto",
                "stars": "⭐⭐",
                "desc": "Terreno Cuadrático. Descifra los factores ocultos y encuentra el camino en los mapas de signos.",
                "tags": ["x² − 6x + 8 < 0", "−x² − x + 6 < 0"],
            },
            3: {
                "nombre": "Misión 3: El Abismo",
                "stars": "⭐⭐⭐",
                "desc": "Fracciones peligrosas. Controla las restricciones y no te dejes engañar por los denominadores.",
                "tags": ["4/(x−3) ≥ 5/(x+2)", "(−x−10)/(x+1) > −x−2"],
            },
        }

        cols = st.columns(3, gap="small")
        for i, (lvl, meta) in enumerate(niveles_meta.items()):
            with cols[i]:
                tags_html = "".join(
                    f"<span class='nivel-tag'>{t}</span>" for t in meta["tags"]
                )
                st.markdown(f"""
<div class="nivel-card">
  <div class="nivel-num">Nivel {lvl:02d}</div>
  <div class="nivel-name">{meta['nombre']}</div>
  <div class="nivel-stars">{meta['stars']}</div>
  <div class="nivel-desc">{meta['desc']}</div>
  <div style="margin-top:8px;">{tags_html}</div>
</div>
<div style="height:8px"></div>""", unsafe_allow_html=True)
                if st.button(
                    f"Aceptar el Reto {lvl}",
                    key=f"sel_{lvl}",
                    use_container_width=True,
                ):
                    _iniciar_nivel(lvl)
                    st.rerun()
        return




    # ══════════════════════════════════════════════════════
    # PANTALLA FINAL
    # ══════════════════════════════════════════════════════
    if st.session_state.juego_terminado:
        nombres = {1: "El Despertar", 2: "El Laberinto", 3: "El Abismo"}
        errores = st.session_state.historial_errores

        if not errores:
            st.balloons()
            st.markdown(f"""
<div class="final-win">
  <h2>LEYENDA. Misión {st.session_state.nivel} perfecta.</h2>
  <p>Gauss pasó al otro lado corriendo gracias a tu precisión. Ni un solo rasguño, eres imparable.</p>
</div>""", unsafe_allow_html=True)
            # GIF de victoria
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWpodXNsZWl2aDZheHg2YnVzNGhkb3pxeGhveHNiNnZwbzI5NDU2bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HumSLHE7SgXETxBet5/giphy.gif",
                    use_container_width=True,
                )
        else:
            st.markdown(f"""
<div class="final-card">
  <h2>Misión {st.session_state.nivel} — {nombres[st.session_state.nivel]}</h2>
  <p style="color:#64748B !important; font-weight:700 !important;">A duras penas pero lo lograste. Gauss llegó sudando a la orilla. Revisa tu bitácora para que la próxima vez seas invencible.</p>
</div>""", unsafe_allow_html=True)

            temas_vistos: list[str] = []
            for err in errores:
                llave = tuple(err)
                tema = TEMAS_ERROR.get(llave, "Tácticas generales de inecuaciones")
                if tema not in temas_vistos:
                    temas_vistos.append(tema)

            items_html = "".join(
                f"<div class='fail-item'>"
                f"<span class='fail-num'>{j + 1}</span>"
                f"<span>{tema}</span>"
                f"</div>"
                for j, tema in enumerate(temas_vistos)
            )
            st.markdown(f"""
<div class="fail-panel">
  <div class="fail-intro">
    Bitácora de Entrenamiento para el Futuro:
  </div>
  {items_html}
</div>""", unsafe_allow_html=True)

            # GIF de victoria (ganó aunque sea con errores)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWpodXNsZWl2aDZheHg2YnVzNGhkb3pxeGhveHNiNnZwbzI5NDU2bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HumSLHE7SgXETxBet5/giphy.gif",
                    use_container_width=True,
                )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Volver a la Base", use_container_width=True):
                st.session_state.nivel = None
                st.session_state.juego_terminado = False
                st.rerun()
        with col2:
            if st.button("Jugar este reto de nuevo", use_container_width=True):
                _reiniciar_nivel()
                st.rerun()
        return

    # ══════════════════════════════════════════════════════
    # BARRA DEL RÍO + PROGRESO
    # ══════════════════════════════════════════════════════
    paso_global = st.session_state.ineq_idx * 3 + st.session_state.paso_idx
    st.markdown(f"""
<div class="rio-container">
  <div class="rio-label">Gauss cruzando el río</div>
  <div class="rio-track">{_gauss_bar(paso_global)}</div>
</div>""", unsafe_allow_html=True)
    st.progress(paso_global / 6)

    # ── HUD ───────────────────────────────────────────────
    nombres = {1: "Básico", 2: "Intermedio", 3: "Experto"}
    vidas_str = "Vidas: " + str(st.session_state.vidas) if st.session_state.vidas > 0 else "—"
    comod_str = f"×{st.session_state.comodines}" if st.session_state.comodines > 0 else "Agotados"
    err_count  = len(st.session_state.historial_errores)
    err_str    = str(err_count) if err_count else "Invicto"

    st.markdown(f"""
<div class="hud-row">
  <div class="hud-chip">
    <span class="hud-label">Misión Activa</span>
    <span class="hud-value">{st.session_state.nivel} · {nombres[st.session_state.nivel]}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Energía Vital</span>
    <span class="hud-value">{vidas_str}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Poderes Mágicos</span>
    <span class="hud-value">{comod_str}</span>
  </div>
  <div class="hud-chip">
    <span class="hud-label">Daño Recibido</span>
    <span class="hud-value">{err_str}</span>
  </div>
</div>""", unsafe_allow_html=True)

    if st.button("Huir a la base de niveles", key="back_nivel"):
        st.session_state.nivel = None
        st.rerun()

    # ── GAME OVER ──────────────────────────────────────────
    if st.session_state.vidas <= 0:
        st.markdown("<hr>", unsafe_allow_html=True)
        # GIF de derrota al quedarse sin vidas
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXlhcGw1NnM3dG42MWtjYnZlbWE1aThkN20wbHBndTlzeW9rMWljYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PB82BUQk9r9h6vgzPv/giphy.gif",
                use_container_width=True,
            )
        st.error("Gauss cayó al agua y los cocodrilos enemigos se ríen. Te quedaste sin energía.")
        st.markdown(
            "<p>Pero los verdaderos héroes siempre tienen revancha. Revisa bien tus tácticas de signos y vuelve a intentarlo. Gauss confía plenamente en ti.</p>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Revivir y jugar de nuevo", use_container_width=True):
                _reiniciar_nivel(); st.rerun()
        with col2:
            if st.button("Ir al menú principal", key="fail_back", use_container_width=True):
                st.session_state.nivel = None; st.rerun()
        return

    # ══════════════════════════════════════════════════════
    # INECUACIÓN ACTIVA
    # ══════════════════════════════════════════════════════
    nivel    = st.session_state.nivel
    ineq_idx = st.session_state.ineq_idx
    paso_idx = st.session_state.paso_idx
    ineq     = INECUACIONES[nivel][ineq_idx]
    paso     = ineq["pasos"][paso_idx]
    total_p  = len(ineq["pasos"])

    dots = "".join(
        "<div class='paso-dot"
        + (" paso-dot-done'" if d < paso_idx else " paso-dot-active'" if d == paso_idx else "'")
        + "></div>"
        for d in range(total_p)
    )
    st.markdown(
        f"<div class='paso-dot-row'>{dots}"
        f"<span style='font-size:0.72rem;color:#94A3B8;margin-left:6px;font-weight:800;'>"
        f"Enfrentamiento {paso['num']} de {total_p}</span></div>",
        unsafe_allow_html=True,
    )

    ya_respondido = st.session_state.resultado is not None
    correcto      = st.session_state.resultado == "correcto"

    ecuacion_display = paso["expresion"] if (ya_respondido and correcto) else paso["expresion_dinamica"]

    st.markdown(f"""
<div class="ineq-card">
  <span class="ineq-badge">Desafío {ineq_idx + 1} de 2 · {ineq['titulo']}</span>
""", unsafe_allow_html=True)
    st.latex(ecuacion_display)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"<p class='eyebrow'>Instrucción Táctica</p>"
        f"<h3 style='margin-bottom:6px;'>{paso['descripcion']}</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-weight:700;font-size:1.05rem;color:#1E293B !important;margin-bottom:12px;'>"
        f"{paso['pregunta']}</p>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════
    # OPCIONES MEZCLADAS
    # ══════════════════════════════════════════════════════
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
    cols          = st.columns(3, gap="small")

    for i, (letra, texto) in enumerate(opciones_show.items()):
        with cols[i]:
            if oculta and letra == oculta:
                st.markdown(
                    "<div class='opt-eliminated'>Eliminada por comodín</div>",
                    unsafe_allow_html=True,
                )
                continue

            if not ya_respondido:
                if st.button(
                    f"**{letra}.** {texto}",
                    key=f"opt_{letra}",
                    use_container_width=True,
                ):
                    _procesar_respuesta(letra, correcta_now)
                    st.rerun()
            else:
                es_sel = st.session_state.opcion_seleccionada == letra
                es_ok  = correcta_now == letra
                if (es_sel and correcto) or (es_ok and not correcto):
                    cls = "opt-correct"
                elif es_sel:
                    cls = "opt-selected-wrong"
                else:
                    cls = "opt-btn"
                st.markdown(
                    f"<div class='{cls}'><strong>{letra}.</strong> {texto}</div>",
                    unsafe_allow_html=True,
                )

    # ── Comodín ────────────────────────────────────────────
    if not ya_respondido and st.session_state.comodines > 0 and oculta is None:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button(
            f"Eliminar una opción  ({st.session_state.comodines} carga{'s' if st.session_state.comodines > 1 else ''} restante{'s' if st.session_state.comodines > 1 else ''})",
            key="comodin",
        ):
            _usar_comodin(opciones_show, correcta_now)
            st.rerun()

    # ── Feedback ───────────────────────────────────────────
    if ya_respondido:
        st.markdown("<hr>", unsafe_allow_html=True)
        if correcto:
            st.success(paso["ok"])
            if st.button("Siguiente movimiento", use_container_width=True):
                _avanzar_paso(); st.rerun()
        else:
            st.error(paso["err"])
            if st.button("Reagruparse e intentarlo de nuevo", use_container_width=True):
                st.session_state.update({
                    "resultado": None,
                    "opcion_seleccionada": None,
                    "opcion_oculta": None,
                    "opciones_shuffle": None,
                })
                st.rerun()


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def _iniciar_nivel(lvl: int) -> None:
    st.session_state.update({
        "nivel": lvl, "ineq_idx": 0, "paso_idx": 0,
        "vidas": 3, "comodines": 2,
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [], "opciones_shuffle": None,
    })


def _reiniciar_nivel() -> None:
    st.session_state.update({
        "ineq_idx": 0, "paso_idx": 0,
        "vidas": 3, "comodines": 2,
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "juego_terminado": False,
        "historial_errores": [], "opciones_shuffle": None,
    })


def _procesar_respuesta(letra_elegida: str, correcta: str) -> None:
    st.session_state.opcion_seleccionada = letra_elegida
    nivel    = st.session_state.nivel
    ineq_idx = st.session_state.ineq_idx
    paso_idx = st.session_state.paso_idx

    if letra_elegida == correcta:
        st.session_state.resultado = "correcto"
    else:
        st.session_state.resultado = "incorrecto"
        st.session_state.vidas    -= 1
        err_key = [nivel, ineq_idx, paso_idx]
        if err_key not in st.session_state.historial_errores:
            st.session_state.historial_errores.append(err_key)


def _usar_comodin(opciones_show: dict, correcta: str) -> None:
    candidatas = [
        k for k in opciones_show
        if k != correcta and k != st.session_state.opcion_oculta
    ]
    if candidatas:
        st.session_state.opcion_oculta  = random.choice(candidatas)
        st.session_state.comodines     -= 1


def _avanzar_paso() -> None:
    st.session_state.update({
        "resultado": None, "opcion_seleccionada": None,
        "opcion_oculta": None, "opciones_shuffle": None,
    })
    nivel    = st.session_state.nivel
    ineq_idx = st.session_state.ineq_idx
    paso_idx = st.session_state.paso_idx

    if paso_idx + 1 < len(INECUACIONES[nivel][ineq_idx]["pasos"]):
        st.session_state.paso_idx += 1
    elif ineq_idx + 1 < len(INECUACIONES[nivel]):
        st.session_state.ineq_idx += 1
        st.session_state.paso_idx  = 0
    else:
        st.session_state.juego_terminado = True


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    st.set_page_config(
        page_title="Misión: Rescatar a Gauss",
        layout="centered",
    )
    mostrar_juego()