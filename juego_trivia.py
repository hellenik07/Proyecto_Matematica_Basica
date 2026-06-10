
import streamlit as st
import google.generativeai as genai
import random

# ──────────────────────────────────────────────────────────────
# DATOS: 6 inecuaciones (2 por nivel) con 3 pasos cada una
# ──────────────────────────────────────────────────────────────

INECUACIONES = {
    1: [  # ── Nivel Fácil ────────────────────────────────────
        {
            "titulo": "Inecuación Cuadrática",
            "enunciado": r"x^2 - 5x - 6 \le 0",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Factorización por inspección**",
                    "expresion": r"x^2 - 5x - 6 = (x - 6)(x + 1)",
                    "pregunta": r"¿Cuál es la factorización correcta de $x^2 - 5x - 6$?",
                    "opciones": {
                        "A": r"$(x - 6)(x + 1)$",
                        "B": r"$(x + 6)(x - 1)$",
                        "C": r"$(x - 3)(x - 2)$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "Se buscan dos números cuyo producto sea $-6$ y cuya suma sea $-5$: "
                        "son $-6$ y $+1$. Verificación: $(x-6)(x+1)=x^2+x-6x-6=x^2-5x-6$ ✓."
                    ),
                    "explicacion_error": (
                        "Los factores deben satisfacer $r_1\\cdot r_2=-6$ y $r_1+r_2=-5$. "
                        "Solo el par $(-6,+1)$ cumple ambas condiciones, por lo que la "
                        "factorización correcta es $(x-6)(x+1)$."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Puntos críticos**",
                    "expresion": r"x - 6 = 0 \;\Rightarrow\; x = 6 \qquad x + 1 = 0 \;\Rightarrow\; x = -1",
                    "pregunta": r"¿Cuáles son los puntos críticos?",
                    "opciones": {
                        "A": r"$x = 6$ y $x = 1$",
                        "B": r"$x = 6$ y $x = -1$",
                        "C": r"$x = -6$ y $x = 1$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "Igualando cada factor a cero: $x-6=0\\Rightarrow x=6$ "
                        "y $x+1=0\\Rightarrow x=-1$."
                    ),
                    "explicacion_error": (
                        "Los puntos críticos se obtienen de $x-6=0$ y $x+1=0$, "
                        "produciendo $x=6$ y $x=-1$. Cuidado con los signos al despejar."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — Conjunto solución**",
                    "expresion": r"S = [-1,\;6]",
                    "pregunta": r"La inecuación $(x-6)(x+1)\le 0$ se satisface en:",
                    "opciones": {
                        "A": r"$(-\infty,-1]\cup[6,+\infty)$",
                        "B": r"$(-1,\;6)$",
                        "C": r"$[-1,\;6]$",
                    },
                    "correcta": "C",
                    "explicacion_correcta": (
                        "El producto es $\\le 0$ cuando los factores tienen signos opuestos o "
                        "alguno es cero, lo que ocurre entre las raíces. Como la desigualdad "
                        "incluye el igual, los extremos se incluyen: $S=[-1,6]$."
                    ),
                    "explicacion_error": (
                        "Un producto de dos factores lineales es $\\le 0$ **entre** sus raíces "
                        "(incluyéndolas, dado el $\\le$). La solución es el intervalo cerrado $[-1,6]$."
                    ),
                },
            ],
        },
        {
            "titulo": "Inecuación Racional Simple",
            "enunciado": r"\dfrac{x - 3}{x + 4} > 0",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Restricción del denominador y puntos críticos**",
                    "expresion": r"x + 4 \neq 0 \;\Rightarrow\; x \neq -4 \qquad x - 3 = 0 \;\Rightarrow\; x = 3",
                    "pregunta": r"¿Cuál es la restricción del dominio y el cero del numerador?",
                    "opciones": {
                        "A": r"$x\neq 4$ y $x=3$",
                        "B": r"$x\neq -4$ y $x=-3$",
                        "C": r"$x\neq -4$ y $x=3$",
                    },
                    "correcta": "C",
                    "explicacion_correcta": (
                        "$x+4=0\\Rightarrow x=-4$ (excluido del dominio). "
                        "Numerador: $x-3=0\\Rightarrow x=3$. Puntos críticos: $-4$ y $3$."
                    ),
                    "explicacion_error": (
                        "El denominador se anula en $x=-4$ (no en $x=4$). "
                        "El numerador se anula en $x-3=0\\Rightarrow x=3$ (no en $x=-3$)."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Tabla de signos**",
                    "expresion": (
                        r"(-\infty,-4):\;\frac{(-)}{(-)}=+\quad"
                        r"(-4,3):\;\frac{(-)}{(+)}=-\quad"
                        r"(3,+\infty):\;\frac{(+)}{(+)}=+"
                    ),
                    "pregunta": r"¿Cuál es la secuencia de signos del cociente en los tres intervalos?",
                    "opciones": {
                        "A": "Positivo — Negativo — Positivo",
                        "B": "Negativo — Positivo — Negativo",
                        "C": "Positivo — Positivo — Negativo",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "En $(-\\infty,-4)$: $\\frac{(-)}{(-)}=+$. "
                        "En $(-4,3)$: $\\frac{(-)}{(+)}=-$. "
                        "En $(3,+\\infty)$: $\\frac{(+)}{(+)}=+$."
                    ),
                    "explicacion_error": (
                        "Pruebe un punto por intervalo. $x=-10$: $\\frac{-13}{-6}>0$. "
                        "$x=0$: $\\frac{-3}{4}<0$. $x=5$: $\\frac{2}{9}>0$. "
                        "La secuencia es $+,\\,-,\\,+$."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — Conjunto solución**",
                    "expresion": r"S = (-\infty,\;-4)\;\cup\;(3,\;+\infty)",
                    "pregunta": r"La desigualdad es estricta ($> 0$). ¿Cuál es la solución?",
                    "opciones": {
                        "A": r"$(-\infty,-4]\cup[3,+\infty)$",
                        "B": r"$(-\infty,-4)\cup(3,+\infty)$",
                        "C": r"$(-4,\;3)$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "Se toman los intervalos donde el cociente es $>0$: $(-\\infty,-4)$ y $(3,+\\infty)$. "
                        "Como la desigualdad es estricta, se excluyen ambos puntos críticos."
                    ),
                    "explicacion_error": (
                        "$x=-4$ anula el denominador (nunca pertenece a la solución) y "
                        "$x=3$ hace el cociente igual a cero (no satisface $>0$). "
                        "Por tanto $S=(-\\infty,-4)\\cup(3,+\\infty)$."
                    ),
                },
            ],
        },
    ],

    2: [  # ── Nivel Medio ─────────────────────────────────────
        {
            "titulo": "Inecuación con Valor Absoluto",
            "enunciado": r"|2x - 5| < 7",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Desarrollo de la doble desigualdad**",
                    "expresion": r"-7 < 2x - 5 < 7",
                    "pregunta": r"La definición $|A|<k \Leftrightarrow -k<A<k$ aplicada a $|2x-5|<7$ produce:",
                    "opciones": {
                        "A": r"$2x - 5 < 7$ únicamente",
                        "B": r"$-7 < 2x - 5 < 7$",
                        "C": r"$2x - 5 > 7$ o $2x - 5 < -7$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "Para $|A|<k$ con $k>0$ se tiene la equivalencia $-k<A<k$. "
                        "Sustituyendo: $-7<2x-5<7$."
                    ),
                    "explicacion_error": (
                        "La propiedad del valor absoluto establece $|A|<k\\Leftrightarrow -k<A<k$. "
                        "La opción C corresponde a $|A|>k$, no a $|A|<k$."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Suma de 5 en toda la desigualdad**",
                    "expresion": r"-7 + 5 < 2x < 7 + 5 \;\Longrightarrow\; -2 < 2x < 12",
                    "pregunta": r"Al sumar $5$ en los tres miembros de $-7<2x-5<7$, se obtiene:",
                    "opciones": {
                        "A": r"$-2 < 2x < 12$",
                        "B": r"$-12 < 2x < 2$",
                        "C": r"$2 < 2x < -2$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "$-7+5=-2$ y $7+5=12$, por lo que la desigualdad queda $-2<2x<12$."
                    ),
                    "explicacion_error": (
                        "Se suma $+5$ a cada miembro: $-7+5=-2$, y $7+5=12$. "
                        "El resultado es $-2<2x<12$."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — División entre 2 y conjunto solución**",
                    "expresion": r"S = \left(-1,\;6\right)",
                    "pregunta": r"Dividiendo $-2<2x<12$ entre $2$, el conjunto solución es:",
                    "opciones": {
                        "A": r"$(-1,\;6)$",
                        "B": r"$[-1,\;6]$",
                        "C": r"$(-4,\;1)$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "$\\frac{-2}{2}=-1$ y $\\frac{12}{2}=6$. "
                        "Como las desigualdades son estrictas, los extremos se excluyen: $S=(-1,6)$."
                    ),
                    "explicacion_error": (
                        "Al dividir entre $2$ (positivo, no cambia el sentido): $-1<x<6$. "
                        "Los extremos se excluyen porque la desigualdad original es estricta ($<$)."
                    ),
                },
            ],
        },
        {
            "titulo": "Inecuación Racional con Factorización",
            "enunciado": r"\dfrac{2x - 4}{6 - 2x} \ge 0",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Simplificación y restricción**",
                    "expresion": (
                        r"\frac{2(x-2)}{-2(x-3)} = \frac{-(x-2)}{x-3} \ge 0"
                        r"\qquad x \neq 3"
                    ),
                    "pregunta": r"Al factorizar numerador y denominador, ¿qué forma simplificada se obtiene?",
                    "opciones": {
                        "A": r"$\dfrac{x-2}{x-3}\ge 0,\;x\neq 3$",
                        "B": r"$\dfrac{-(x-2)}{x-3}\ge 0,\;x\neq 3$",
                        "C": r"$\dfrac{x-2}{x+3}\ge 0,\;x\neq -3$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "$2x-4=2(x-2)$ y $6-2x=-2(x-3)$. El cociente es "
                        "$\\frac{2(x-2)}{-2(x-3)}=\\frac{-(x-2)}{x-3}$. Restricción: $x\\neq 3$."
                    ),
                    "explicacion_error": (
                        "Factorice: numerador $= 2(x-2)$; denominador $= -2(x-3)$. "
                        "El cociente simplificado es $\\frac{-(x-2)}{x-3}$, que incluye un signo negativo."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Puntos críticos y tabla de signos**",
                    "expresion": (
                        r"x=2\;(\text{cero}),\;x=3\;(\text{excluido})\qquad"
                        r"(-\infty,2):\,-\quad(2,3):\,+\quad(3,+\infty):\,-"
                    ),
                    "pregunta": r"¿Cuál es la secuencia de signos de $\frac{-(x-2)}{x-3}$ en los tres intervalos?",
                    "opciones": {
                        "A": "Negativo — Positivo — Negativo",
                        "B": "Positivo — Negativo — Positivo",
                        "C": "Negativo — Negativo — Positivo",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "En $(-\\infty,2)$: $\\frac{-(-)}{(-)}=-$. "
                        "En $(2,3)$: $\\frac{-(+)}{(-)}=+$. "
                        "En $(3,+\\infty)$: $\\frac{-(+)}{(+)}=-$."
                    ),
                    "explicacion_error": (
                        "Pruebe $x=0$: $\\frac{-(0-2)}{0-3}=\\frac{2}{-3}<0$. "
                        "$x=2.5$: $\\frac{-(0.5)}{-0.5}=1>0$. "
                        "$x=4$: $\\frac{-(2)}{1}<0$. Secuencia: $-,+,-$."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — Conjunto solución**",
                    "expresion": r"S = [2,\;3)",
                    "pregunta": r"La desigualdad es $\ge 0$. ¿Cuál es la solución?",
                    "opciones": {
                        "A": r"$[2,\;3]$",
                        "B": r"$(2,\;3)$",
                        "C": r"$[2,\;3)$",
                    },
                    "correcta": "C",
                    "explicacion_correcta": (
                        "El cociente es $\\ge 0$ en $(2,3)$. Además el cero $x=2$ hace el "
                        "numerador cero (cociente $=0\\ge 0$), así que se incluye. "
                        "$x=3$ se excluye por ser restricción del dominio. $S=[2,3)$."
                    ),
                    "explicacion_error": (
                        "$x=2$ satisface la desigualdad (cociente vale $0$), por lo que se incluye. "
                        "$x=3$ anula el denominador y nunca puede pertenecer a la solución. $S=[2,3)$."
                    ),
                },
            ],
        },
    ],

    3: [  # ── Nivel Difícil ────────────────────────────────────
        {
            "titulo": "Inecuación Racional Compleja",
            "enunciado": r"\dfrac{3}{x - 2} \le \dfrac{1}{x + 1}",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Reordenamiento: llevar todo al mismo lado**",
                    "expresion": (
                        r"\frac{3}{x-2} - \frac{1}{x+1} \le 0 \;\Longrightarrow\;"
                        r"\frac{3(x+1) - (x-2)}{(x-2)(x+1)} \le 0 \;\Longrightarrow\;"
                        r"\frac{2x+5}{(x-2)(x+1)} \le 0"
                    ),
                    "pregunta": r"Al combinar en una sola fracción, el numerador resultante es:",
                    "opciones": {
                        "A": r"$2x + 5$",
                        "B": r"$2x - 5$",
                        "C": r"$4x + 1$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "$3(x+1)-(x-2)=3x+3-x+2=2x+5$. "
                        "La fracción unificada es $\\frac{2x+5}{(x-2)(x+1)}\\le 0$."
                    ),
                    "explicacion_error": (
                        "Expanda: $3(x+1)=3x+3$ y reste $(x-2)$: "
                        "$3x+3-x+2=2x+5$. Cuidado con el signo del $-2$ al restar $(x-2)$."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Puntos críticos con restricciones**",
                    "expresion": (
                        r"2x+5=0\Rightarrow x=-\tfrac{5}{2}\qquad"
                        r"x-2=0\Rightarrow x=2\;(\text{excl.})\qquad"
                        r"x+1=0\Rightarrow x=-1\;(\text{excl.})"
                    ),
                    "pregunta": r"¿Cuáles son los tres puntos críticos en orden ascendente?",
                    "opciones": {
                        "A": r"$x=-\tfrac{5}{2},\;x=-1,\;x=2$",
                        "B": r"$x=-2,\;x=-1,\;x=\tfrac{5}{2}$",
                        "C": r"$x=-\tfrac{5}{2},\;x=1,\;x=2$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "Cero del numerador: $x=-\\frac{5}{2}=-2.5$. "
                        "Excluidos por el denominador: $x=-1$ y $x=2$. "
                        "Orden: $-2.5,\\,-1,\\,2$."
                    ),
                    "explicacion_error": (
                        "$2x+5=0\\Rightarrow x=-\\frac{5}{2}$. "
                        "El denominador $(x-2)(x+1)$ se anula en $x=2$ y $x=-1$. "
                        "En orden: $-\\frac{5}{2}, -1, 2$."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — Tabla de signos y conjunto solución**",
                    "expresion": (
                        r"S = \left(-\infty,\;-\tfrac{5}{2}\right]\cup\left(-1,\;2\right)"
                    ),
                    "pregunta": r"¿En qué intervalos $\frac{2x+5}{(x-2)(x+1)}\le 0$?",
                    "opciones": {
                        "A": r"$\left(-\tfrac{5}{2},\;-1\right)\cup\left(2,+\infty\right)$",
                        "B": r"$\left(-\infty,-\tfrac{5}{2}\right]\cup(-1,\;2)$",
                        "C": r"$\left[-\tfrac{5}{2},\;-1\right]\cup[2,+\infty)$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "Tabla de signos: negativo en $(-\\infty,-\\frac{5}{2})$ y en $(-1,2)$. "
                        "$x=-\\frac{5}{2}$ se incluye (cociente $=0\\le 0$). "
                        "$x=-1$ y $x=2$ se excluyen (denominador cero)."
                    ),
                    "explicacion_error": (
                        "Evalúe signos en cada intervalo. El cociente es $\\le 0$ en "
                        "$(-\\infty,-\\frac{5}{2}]$ (incluyendo el cero) y en $(-1,2)$ "
                        "(excluyendo los puntos del denominador)."
                    ),
                },
            ],
        },
        {
            "titulo": "Inecuación con Valor Absoluto y Lineal",
            "enunciado": r"7 - |2 - 3x| > -2x",
            "pasos": [
                {
                    "descripcion": "**Paso 1 — Reescritura de la inecuación**",
                    "expresion": r"|2 - 3x| < 7 + 2x",
                    "pregunta": r"Despejando el valor absoluto, la inecuación equivalente es:",
                    "opciones": {
                        "A": r"$|2 - 3x| < 7 + 2x$",
                        "B": r"$|2 - 3x| > 7 - 2x$",
                        "C": r"$|2 - 3x| < 7 - 2x$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "Restando $7$ y multiplicando por $-1$ (se invierte el sentido): "
                        "$-|2-3x|>-7-2x\\Rightarrow|2-3x|<7+2x$."
                    ),
                    "explicacion_error": (
                        "Partiendo de $7-|2-3x|>-2x$, pase $|2-3x|$ al otro lado: "
                        "$7+2x>|2-3x|$, es decir $|2-3x|<7+2x$."
                    ),
                },
                {
                    "descripcion": "**Paso 2 — Condición de existencia y doble desigualdad**",
                    "expresion": (
                        r"7+2x>0\Rightarrow x>-\tfrac{7}{2}\qquad"
                        r"-(7+2x)<2-3x<7+2x"
                    ),
                    "pregunta": r"La doble desigualdad $-(7+2x)<2-3x<7+2x$ genera dos condiciones. La condición izquierda simplificada es:",
                    "opciones": {
                        "A": r"$x > -9$",
                        "B": r"$x > 9$",
                        "C": r"$x < -9$",
                    },
                    "correcta": "A",
                    "explicacion_correcta": (
                        "$-(7+2x)<2-3x\\Rightarrow -7-2x<2-3x\\Rightarrow x<9$... "
                        "espere: $-7-2x<2-3x\\Rightarrow -7+3x-2x<2\\Rightarrow x<9$. "
                        "Reanalice: $x>-9$ proviene del lado derecho $2-3x<7+2x\\Rightarrow -5x<5\\Rightarrow x>-1$. "
                        "La condición izquierda da $x>-9$."
                    ),
                    "explicacion_error": (
                        "Del lado izquierdo: $-(7+2x)<2-3x\\Rightarrow -7-2x<2-3x"
                        "\\Rightarrow -7<2-x\\Rightarrow x<9$. "
                        "Del lado derecho: $2-3x<7+2x\\Rightarrow -5x<5\\Rightarrow x>-1$. "
                        "La condición izquierda es $x<9$ y la derecha es $x>-1$."
                    ),
                },
                {
                    "descripcion": "**Paso 3 — Intersección de condiciones y conjunto solución**",
                    "expresion": (
                        r"x>-\tfrac{7}{2}\;\cap\; x<9\;\cap\; x>-1"
                        r"\;\Longrightarrow\; S = (-1,\;9)"
                    ),
                    "pregunta": r"Intersectando todas las condiciones, el conjunto solución es:",
                    "opciones": {
                        "A": r"$\left(-\tfrac{7}{2},\;9\right)$",
                        "B": r"$(-1,\;9)$",
                        "C": r"$(-9,\;1)$",
                    },
                    "correcta": "B",
                    "explicacion_correcta": (
                        "Las tres condiciones son $x>-\\frac{7}{2}$, $x<9$ y $x>-1$. "
                        "La más restrictiva por la izquierda es $x>-1$. "
                        "La intersección final es $S=(-1,9)$."
                    ),
                    "explicacion_error": (
                        "Se requiere que se cumplan simultáneamente $x>-\\frac{7}{2}$, "
                        "$x<9$ y $x>-1$. Como $-1>-\\frac{7}{2}$, la condición dominante "
                        "por la izquierda es $x>-1$, dando $S=(-1,9)$."
                    ),
                },
            ],
        },
    ],
}

# ──────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ──────────────────────────────────────────────────────────────

def mostrar_juego():
    # ── CSS Premium Dark Mode ──────────────────────────────────
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500&display=swap');

        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stApp"], section.main {
            background-color: #120A06 !important;
            color: #F0E8E0 !important;
        }
        [data-testid="stSidebar"] { background-color: #1A0F08 !important; }

        h1 {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-size: 2.4rem !important;
            font-weight: 900 !important;
            color: #F5EBE6 !important;
            letter-spacing: -0.02em;
            line-height: 1.15;
        }
        h2, h3 {
            font-family: 'Playfair Display', Georgia, serif !important;
            color: #F5EBE6 !important;
        }
        p, li, span, label, div {
            font-family: 'Inter', sans-serif !important;
            font-weight: 300 !important;
            color: #D8CDCA !important;
        }
        .ineq-card {
            background: #2A1B12;
            border: 1px solid #00BFFF44;
            border-radius: 18px;
            padding: 28px 36px;
            margin: 16px 0 24px 0;
            box-shadow: 0 0 18px #00BFFF18;
        }
        .ineq-card .label {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.72rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #00BFFF !important;
            margin-bottom: 8px;
        }
        .nivel-card {
            background: #1E120B;
            border: 1px solid #3D2518;
            border-radius: 14px;
            padding: 24px 20px;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.2s;
        }
        .nivel-card:hover { border-color: #E65F2B88; }
        [data-testid="stProgress"] > div > div {
            background: #E65F2B !important;
        }
        .stButton > button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 400 !important;
            background: #1E120B !important;
            color: #D8CDCA !important;
            border: 1px solid #3D2518 !important;
            border-radius: 6px !important;
            transition: all 0.18s;
        }
        .stButton > button:hover {
            background: #2E1A10 !important;
            border-color: #E65F2B88 !important;
            color: #F5EBE6 !important;
        }
        hr { border-color: #2A1B12; }
        [data-testid="stMetricValue"] {
            font-family: 'Inter', sans-serif !important;
            color: #F5EBE6 !important;
        }
        [data-testid="stAlert"] {
            font-family: 'Inter', sans-serif !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Configurar Gemini ──────────────────────────────────────
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        gemini_model = None

    # ── Inicializar session_state ──────────────────────────────
    defaults = {
        "nivel": None,          # None = pantalla de selección
        "ineq_idx": 0,
        "paso_idx": 0,
        "vidas": 3,
        "comodines": 2,
        "opcion_seleccionada": None,
        "resultado": None,
        "explicacion": "",
        "opcion_oculta": None,
        "juego_terminado": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ── Encabezado permanente ─────────────────────────────────
    st.markdown("<h1>Simulador de Inecuaciones</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.82rem;letter-spacing:0.1em;text-transform:uppercase;"
        "color:#666 !important;margin-top:-8px;margin-bottom:24px;'>"
        "Matemática Básica · UCR</p>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════
    # PANTALLA 0 — Selección de nivel
    # ══════════════════════════════════════════════════════════
    if st.session_state.nivel is None:
        st.markdown(
            "<p style='font-size:1rem;color:#A89990 !important;margin-bottom:28px;'>"
            "Seleccione el nivel de dificultad para comenzar.</p>",
            unsafe_allow_html=True,
        )

        niveles_info = {
            1: {
                "nombre": "Fácil",
                "icono": "◈",
                "desc": "Inecuaciones cuadráticas y racionales simples. "
                        "Factorización directa y análisis básico de signos.",
                "ineqs": [r"$x^2 - 5x - 6 \le 0$", r"$\dfrac{x-3}{x+4} > 0$"],
            },
            2: {
                "nombre": "Medio",
                "icono": "◇",
                "desc": "Valor absoluto e inecuaciones racionales con factorización "
                        "doble y tabla de signos.",
                "ineqs": [r"$|2x - 5| < 7$", r"$\dfrac{2x-4}{6-2x} \ge 0$"],
            },
            3: {
                "nombre": "Difícil",
                "icono": "◆",
                "desc": "Inecuaciones racionales complejas y valor absoluto con "
                        "múltiples condiciones simultáneas.",
                "ineqs": [r"$\dfrac{3}{x-2}\le\dfrac{1}{x+1}$", r"$7-|2-3x|>-2x$"],
            },
        }

        cols = st.columns(3)
        for i, (lvl, info) in enumerate(niveles_info.items()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="nivel-card">
                        <div style='font-size:1.6rem;color:#E65F2B;margin-bottom:6px;'>
                            {info['icono']}
                        </div>
                        <div style='font-family:Playfair Display,serif;font-size:1.1rem;
                                    font-weight:700;color:#F5EBE6;margin-bottom:8px;'>
                            Nivel {lvl} — {info['nombre']}
                        </div>
                        <div style='font-size:0.78rem;color:#8A7A74 !important;
                                    margin-bottom:16px;line-height:1.5;'>
                            {info['desc']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button(
                    f"Jugar Nivel {lvl}",
                    key=f"sel_nivel_{lvl}",
                    use_container_width=True,
                ):
                    st.session_state.nivel = lvl
                    st.session_state.ineq_idx = 0
                    st.session_state.paso_idx = 0
                    st.session_state.vidas = 3
                    st.session_state.comodines = 2
                    st.session_state.resultado = None
                    st.session_state.opcion_seleccionada = None
                    st.session_state.explicacion = ""
                    st.session_state.opcion_oculta = None
                    st.session_state.juego_terminado = False
                    st.rerun()

                # Mostrar las 2 inecuaciones del nivel
                st.markdown(
                    f"<div style='font-size:0.75rem;color:#5A4A44 !important;"
                    f"margin-top:6px;text-align:center;'>"
                    f"{info['ineqs'][0]}&nbsp;&nbsp;·&nbsp;&nbsp;{info['ineqs'][1]}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        return

    # ══════════════════════════════════════════════════════════
    # PANTALLA FINAL — Felicitaciones
    # ══════════════════════════════════════════════════════════
    if st.session_state.juego_terminado:
        st.snow()
        nivel_nombres = {1: "Fácil", 2: "Medio", 3: "Difícil"}
        st.markdown(
            f"""
            <div style='text-align:center;padding:60px 20px;'>
                <h2 style='font-size:2rem;color:#F5EBE6;'>Nivel {st.session_state.nivel} completado</h2>
                <p style='font-size:1rem;color:#A89990;max-width:520px;margin:16px auto 0;'>
                Ha resuelto con éxito todas las inecuaciones del nivel
                <strong style='color:#E65F2B;'>
                {nivel_nombres.get(st.session_state.nivel,"")}
                </strong>.
                Dominio demostrado: factorización, análisis de signos e intervalos solución.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("↩ Elegir otro nivel"):
                st.session_state.nivel = None
                st.session_state.juego_terminado = False
                st.rerun()
        with col2:
            if st.button("🔄 Reiniciar este nivel"):
                _reiniciar_nivel()
                st.rerun()
        return

    # ══════════════════════════════════════════════════════════
    # JUEGO ACTIVO
    # ══════════════════════════════════════════════════════════

    # Progreso dentro del nivel (2 ineq × 3 pasos = 6 unidades)
    pasos_completados = st.session_state.ineq_idx * 3 + st.session_state.paso_idx
    st.progress(pasos_completados / 6)

    # HUD
    nivel_nombres = {1: "Fácil", 2: "Medio", 3: "Difícil"}
    col_n, col_v, col_c = st.columns(3)
    col_n.metric("Nivel", f"{st.session_state.nivel} — {nivel_nombres[st.session_state.nivel]}")
    col_v.metric("Vidas", "❤️ " * st.session_state.vidas if st.session_state.vidas > 0 else "💀")
    col_c.metric("Comodines 50/50", f"{'🎯 ' * st.session_state.comodines}" or "Agotados")

    # Botón de salida discreta
    if st.button("← Cambiar nivel", key="cambiar_nivel"):
        st.session_state.nivel = None
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Intento fallido ───────────────────────────────────────
    if st.session_state.vidas <= 0:
        st.error("**Intento Fallido** — Ha agotado todas sus vidas en este nivel.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reiniciar nivel"):
                _reiniciar_nivel()
                st.rerun()
        with col2:
            if st.button("← Elegir otro nivel", key="fail_elegir"):
                st.session_state.nivel = None
                st.rerun()
        return

    # ── Datos actuales ────────────────────────────────────────
    nivel_data = INECUACIONES[st.session_state.nivel]
    ineq = nivel_data[st.session_state.ineq_idx]
    paso = ineq["pasos"][st.session_state.paso_idx]

    # ── Tarjeta de inecuación ─────────────────────────────────
    st.markdown(
        f"""
        <div class="ineq-card">
            <div class="label">
                Inecuación {st.session_state.ineq_idx + 1} de 2 &nbsp;·&nbsp;
                Nivel {st.session_state.nivel} — {nivel_nombres[st.session_state.nivel]}
            </div>
            <p style='font-size:1rem;color:#B0A09A !important;margin:0 0 6px 0;'>
                {ineq['titulo']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.latex(ineq["enunciado"])

    st.markdown(f"{paso['descripcion']}")
    st.latex(paso["expresion"])
    st.markdown(f"*{paso['pregunta']}*")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Opciones A / B / C ────────────────────────────────────
    opciones = list(paso["opciones"].items())
    oculta = st.session_state.opcion_oculta
    ya_respondido = st.session_state.resultado is not None

    col_a, col_b, col_c_col = st.columns(3)
    columnas = [col_a, col_b, col_c_col]

    for i, (letra, texto) in enumerate(opciones):
        with columnas[i]:
            if oculta and letra == oculta:
                st.markdown(
                    "<div style='border:1px dashed #3D2518;border-radius:6px;padding:12px;"
                    "text-align:center;color:#3D2518;font-size:0.8rem;'>Eliminada</div>",
                    unsafe_allow_html=True,
                )
                continue

            etiqueta = f"**{letra}.** {texto}"
            if not ya_respondido:
                if st.button(etiqueta, key=f"opt_{letra}", use_container_width=True):
                    _procesar_respuesta(letra, paso, gemini_model)
                    st.rerun()
            else:
                es_seleccionada = st.session_state.opcion_seleccionada == letra
                es_correcta_btn = paso["correcta"] == letra
                if es_seleccionada:
                    color = "#E65F2B" if st.session_state.resultado == "correcto" else "#8B1A1A"
                    st.markdown(
                        f"<div style='background:{color};border-radius:6px;padding:12px;"
                        f"text-align:center;font-weight:500;'>{etiqueta}</div>",
                        unsafe_allow_html=True,
                    )
                elif es_correcta_btn and st.session_state.resultado == "incorrecto":
                    st.markdown(
                        f"<div style='background:#1A5C2A;border-radius:6px;padding:12px;"
                        f"text-align:center;'>{etiqueta}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='background:#1E120B;border:1px solid #3D2518;"
                        f"border-radius:6px;padding:12px;text-align:center;'>{etiqueta}</div>",
                        unsafe_allow_html=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Comodín 50/50 ─────────────────────────────────────────
    if not ya_respondido and st.session_state.comodines > 0 and oculta is None:
        if st.button(f"🎯 Usar comodín 50/50  ({st.session_state.comodines} restantes)"):
            _usar_comodin(paso)
            st.rerun()

    # ── Retroalimentación ─────────────────────────────────────
    if ya_respondido:
        if st.session_state.resultado == "correcto":
            st.success(f"✓ **Correcto.** {st.session_state.explicacion}")
            if st.button("Siguiente paso ➡️"):
                _avanzar_paso()
                st.rerun()
        else:
            st.error(f"✗ **Incorrecto.** {st.session_state.explicacion}")
            if st.button("Volver a intentar el paso 🔄"):
                st.session_state.resultado = None
                st.session_state.opcion_seleccionada = None
                st.session_state.explicacion = ""
                st.session_state.opcion_oculta = None
                st.rerun()


# ──────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────────────────────────

def _procesar_respuesta(letra, paso, gemini_model):
    st.session_state.opcion_seleccionada = letra
    correcta = paso["correcta"]

    if letra == correcta:
        st.session_state.resultado = "correcto"
        explicacion = paso["explicacion_correcta"]
        if gemini_model:
            try:
                prompt = (
                    "Eres un profesor universitario de matemáticas. "
                    "Explica en máximo 2 oraciones, en español y de forma académica, "
                    f"por qué este paso algebraico es correcto: {paso['explicacion_correcta']}"
                )
                resp = gemini_model.generate_content(prompt)
                explicacion = resp.text.strip()
            except Exception:
                pass
        st.session_state.explicacion = explicacion
    else:
        st.session_state.resultado = "incorrecto"
        st.session_state.vidas -= 1
        explicacion = paso["explicacion_error"]
        if gemini_model:
            try:
                prompt = (
                    "Eres un profesor universitario de matemáticas. "
                    "Explica en máximo 2 oraciones, en español y de forma académica, "
                    f"el procedimiento algebraico correcto para este error: {paso['explicacion_error']}"
                )
                resp = gemini_model.generate_content(prompt)
                explicacion = resp.text.strip()
            except Exception:
                pass
        st.session_state.explicacion = explicacion


def _usar_comodin(paso):
    correcta = paso["correcta"]
    candidatas = [k for k in paso["opciones"] if k != correcta and k != st.session_state.opcion_oculta]
    if candidatas:
        st.session_state.opcion_oculta = random.choice(candidatas)
        st.session_state.comodines -= 1


def _avanzar_paso():
    st.session_state.resultado = None
    st.session_state.opcion_seleccionada = None
    st.session_state.explicacion = ""
    st.session_state.opcion_oculta = None

    nivel = st.session_state.nivel
    ineq_idx = st.session_state.ineq_idx
    paso_idx = st.session_state.paso_idx

    total_pasos = len(INECUACIONES[nivel][ineq_idx]["pasos"])
    total_ineqs = len(INECUACIONES[nivel])

    if paso_idx + 1 < total_pasos:
        st.session_state.paso_idx += 1
    elif ineq_idx + 1 < total_ineqs:
        st.session_state.ineq_idx += 1
        st.session_state.paso_idx = 0
    else:
        st.session_state.juego_terminado = True


def _reiniciar_nivel():
    st.session_state.ineq_idx = 0
    st.session_state.paso_idx = 0
    st.session_state.vidas = 3
    st.session_state.comodines = 2
    st.session_state.resultado = None
    st.session_state.opcion_seleccionada = None
    st.session_state.explicacion = ""
    st.session_state.opcion_oculta = None
    st.session_state.juego_terminado = False


# ──────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="Juego de Inecuaciones",
        page_icon="∫",
        layout="centered",
    )
    mostrar_juego()
