import streamlit as st
from groq import Groq
import base64
import html

def mostrar_tutor():
    st.markdown("""
    <style>
        /* ── RESET GLOBAL: eliminar scroll de la página completa ── */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        html, body {
            overflow: hidden !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Fondo general */
        .stApp {
            background: linear-gradient(180deg, #FAF6F0 0%, #e2e8f0 100%) !important;
            background-attachment: fixed !important;
            height: 100vh !important;
            overflow: hidden !important;
        }

        /* El wrapper principal que Streamlit agrega */
        [data-testid="stAppViewContainer"] {
            height: 100vh !important;
            overflow: hidden !important;
        }

        /* El contenedor de contenido */
        [data-testid="stAppViewBlockContainer"],
        [data-testid="block-container"] {
            overflow: hidden !important;
        }

        /* ── BLOQUE CENTRAL: sin margen enorme, sin scroll ── */
        .block-container {
            background-color: #FAF6F0 !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 20px !important;
            /* Padding muy reducido para ganar espacio vertical */
            padding: 14px 30px 8px 30px !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.09) !important;
            /* Margen mínimo para que no se pegue al borde */
            margin-top: 12px !important;
            margin-bottom: 8px !important;
            max-width: 980px !important;
            /* Sin scroll propio del bloque */
            overflow: hidden !important;
        }

        /* ── SIDEBAR ── */
        [data-testid="stSidebar"] {
            background-color: #FAF6F0 !important;
            border-right: 1px solid #cbd5e1 !important;
            box-shadow: 2px 0 16px rgba(0,0,0,0.04) !important;
            overflow-y: auto !important;
        }

        /* ── TIP CARD ── */
        .tip-card {
            background-color: #FAF6F0;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            padding: 12px 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            color: #475569;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.7;
        }

        /* ── BOTONES BASE ── */
        div.stButton > button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1.5px solid #8B0000 !important;
            border-radius: 9px !important;
            font-weight: 600 !important;
            font-family: sans-serif !important;
            font-size: 12px !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
            transition: 0.18s all ease-in-out !important;
            width: 100% !important;
            white-space: nowrap !important;
            padding: 5px 8px !important;
            height: auto !important;
            min-height: 32px !important;
            line-height: 1.2 !important;
        }
        div.stButton > button:hover {
            background-color: #8B0000 !important;
            color: white !important;
        }

        /* ── BOTÓN CTA PRIMARIO ── */
        div.stButton > button[kind="primary"] {
            background-color: #8B0000 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(139,0,0,0.28) !important;
            height: 46px !important;
            font-size: 15px !important;
            font-weight: bold !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #b91c1c !important;
        }

        /* ── FONDO BOTTOM CONTAINER ── */
        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] > div {
            background-color: transparent !important;
        }

        /* ── FILE UPLOADER MINIMALISTA ── */
        [data-testid="stFileUploader"] { padding: 0 !important; }
        [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] svg { display: none !important; }
        [data-testid="stFileUploader"] > section {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        [data-testid="stFileUploader"] button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1.5px solid #8B0000 !important;
            border-radius: 18px !important;
            font-weight: bold !important;
            padding: 1px 16px !important;
            font-size: 12px !important;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #8B0000 !important;
            color: #FFFFFF !important;
        }

        /* ── CHAT INPUT ── */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
            border: none !important;
        }
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInputContainer"] {
            background-color: #FFFFFF !important;
            border: 2px solid #CBD5E1 !important;
            border-radius: 18px !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stChatInput"]:focus-within > div {
            border-color: #8B0000 !important;
            box-shadow: 0 0 0 1px #8B0000 !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #0F172A !important;
            font-size: 14px !important;
            background-color: #FFFFFF !important;
            -webkit-text-fill-color: #0F172A !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }
        [data-testid="stChatInputSubmitButton"] {
            background-color: #FAF6F0 !important;
            border-radius: 50% !important;
        }
        [data-testid="stChatInputSubmitButton"] svg {
            fill: #8B0000 !important;
        }

        /* ── REDUCIR GAPS entre columnas y elementos ── */
        [data-testid="stHorizontalBlock"] {
            gap: 6px !important;
        }
        /* Quitar espacio entre elementos stMarkdown consecutivos */
        .element-container {
            margin-bottom: 0 !important;
        }
        /* Spinner compacto */
        [data-testid="stSpinner"] {
            margin: 2px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── ESTADO DE SESIÓN ──
    for key, val in [
        ("page", "teoria"),
        ("sidebar_view", "formulas"),
        ("history", []),
        ("clouds", []),
        ("uploader_key", 0),
    ]:
        if key not in st.session_state:
            st.session_state[key] = val

    if "groq_client" not in st.session_state:
        st.session_state.groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    SYSTEM_PROMPT = (
        "Eres un tutor amigable y experto en matemáticas, especializado en inecuaciones. "
        "Explica paso a paso, usa ejemplos claros y alienta al estudiante. "
        "Responde siempre en español. Sé muy conciso: máximo 3 oraciones por respuesta. "
        "NUNCA hables de algo que no sea matemáticas o inecuaciones. "
        "PROHIBIDO dar la respuesta directamente; guía paso a paso. "
        "NUNCA uses LaTeX ni símbolos de dólar. Usa texto plano (ej: 5x ≤ 25)."
    )

    def encode_image(f):
        return base64.b64encode(f.getvalue()).decode('utf-8')

    def get_ai_response(user_text, image_file=None):
        client = st.session_state.groq_client
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.history[-6:]:
            if not msg.get("is_image", False):
                messages.append({"role": msg["role"], "content": msg["content"]})
        if image_file:
            b64 = encode_image(image_file)
            messages.append({"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]})
            model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            messages.append({"role": "user", "content": user_text})
            model = "llama-3.3-70b-versatile"
        try:
            resp = client.chat.completions.create(
                messages=messages, model=model, temperature=0.7, max_tokens=1024
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {e}"

    def render_chat_bubble(role, text, image_b64=None):
        is_user = role == "user"
        bg = "#262626" if is_user else "#8B0000"
        radius = "16px 16px 4px 16px" if is_user else "16px 16px 16px 4px"
        align = "flex-end" if is_user else "flex-start"
        safe = html.escape(text).replace('\n', '<br>')
        img_tag = f'<img src="data:image/jpeg;base64,{image_b64}" style="max-width:220px;border-radius:8px;margin-bottom:6px;"><br>' if image_b64 else ""
        st.markdown(f"""
        <div style="display:flex;justify-content:{align};margin-bottom:10px;width:100%;">
          <div style="background:{bg};color:white;padding:10px 14px;border-radius:{radius};
                      max-width:75%;word-wrap:break-word;box-shadow:0 2px 7px rgba(0,0,0,0.13);
                      font-family:sans-serif;font-size:14px;line-height:1.5;">
            {img_tag}{safe}
          </div>
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════
    # SIDEBAR — siempre fija
    # ══════════════════════════════
    with st.sidebar:
        st.markdown("<h2 style='color:#8B0000;margin:0 0 4px 0;font-size:22px;'>MathSolve.</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#cbd5e1;margin:0 0 10px 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("📐 Fórmulas", key="sb_f"):
                st.session_state.sidebar_view = "formulas"; st.rerun()
        with c2:
            if st.button("☁️ Nubes", key="sb_n"):
                st.session_state.sidebar_view = "nubes"; st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.session_state.sidebar_view == "formulas":
            st.markdown("""
            <div class='tip-card'>
              <strong style='color:#8B0000;'>Regla del Negativo</strong><br><br>
              Al multiplicar o dividir por (−):<br><br>
              ≤ &nbsp;↔&nbsp; ≥<br>
              &lt; &nbsp;↔&nbsp; &gt;
            </div>""", unsafe_allow_html=True)

        else:  # nubes
            st.markdown("<strong style='color:#8B0000;font-size:14px;'>☁️ Mis Nubes</strong>", unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if not st.session_state.clouds:
                st.markdown("<span style='color:#94a3b8;font-size:13px;'>Aún no hay nubes.</span>", unsafe_allow_html=True)
            else:
                to_delete = None
                for idx, cloud in enumerate(st.session_state.clouds):
                    st.markdown(f"""
                    <div style="background:#FAF6F0;border:1.5px solid #8B0000;border-radius:12px;
                                padding:8px 10px 4px 10px;margin-bottom:8px;">
                      <div style="color:#8B0000;font-weight:bold;font-size:12px;">☁️ #{idx+1}</div>
                      <div style="color:#475569;font-size:12px;margin:4px 0 6px;">{html.escape(cloud)}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"🗑 Eliminar #{idx+1}", key=f"del_{idx}"):
                        to_delete = idx
                if to_delete is not None:
                    st.session_state.clouds.pop(to_delete)
                    st.toast("Nube eliminada.")
                    st.rerun()

    # ══════════════════════════════
    # HEADER — compacto
    # ══════════════════════════════
    c_back, c_logo, c_m, c_chat, c_reset = st.columns([0.9, 2.6, 1.1, 0.9, 1.0])
    with c_back:
        if st.button("⬅ Inicio", key="h_back"):
            st.session_state.pagina = "home"; st.rerun()
    with c_logo:
        st.markdown("<h1 style='color:#8B0000;margin:0;font-size:26px;font-weight:900;"
                    "white-space:nowrap;padding-top:1px;'>MathSolve.</h1>", unsafe_allow_html=True)
    with c_m:
        if st.button("📖 Módulo", key="h_mod"):
            st.session_state.page = "teoria"; st.rerun()
    with c_chat:
        if st.button("💬 Chat", key="h_chat"):
            st.session_state.page = "practica"
            if not st.session_state.history:
                st.session_state.history.append({
                    "role": "assistant",
                    "content": "¡Hola! Soy tu Tutor de Inecuaciones. Escribe una expresión para empezar (ej. -3x + 5 ≤ 20).",
                    "is_image": False
                })
            st.rerun()
    with c_reset:
        if st.button("🔄 Reiniciar", key="h_reset"):
            st.session_state.history = []; st.rerun()

    st.markdown("<hr style='border:none;border-top:1.5px solid #cbd5e1;margin:4px 0 10px 0;'>",
                unsafe_allow_html=True)

    # ══════════════════════════════
    # VISTA TEORÍA
    # ══════════════════════════════
    if st.session_state.page == "teoria":
        # Contenido teórico en un bloque compacto, sin scroll de página
        st.markdown("""
        <div style='text-align:center;padding:6px 20px 12px 20px;'>
            <div style='display:inline-block;border:2px solid #8B0000;border-radius:12px;
                        padding:3px 14px;margin-bottom:12px;'>
                <span style='color:#8B0000;font-weight:bold;font-size:11px;letter-spacing:1px;'>
                    MÓDULO: INECUACIONES
                </span>
            </div>
            <h1 style='color:#0f172a;font-size:30px;margin:0 0 12px 0;line-height:1.2;'>
                Desigualdades y Conjuntos
            </h1>
            <p style='color:#475569;font-size:15px;line-height:1.65;max-width:640px;
                      margin:0 auto 18px auto;text-align:left;'>
                <b>Concepto Básico:</b> Una inecuación es una desigualdad algebraica. Buscamos
                el conjunto de valores (intervalo) que cumple con la condición de ser mayor o menor.<br><br>
                <b>Regla de Oro:</b> Se resuelven casi igual que las ecuaciones lineales, con una
                excepción irrompible: si multiplicas o divides por un número <b>negativo</b>,
                el símbolo de desigualdad se <b>invierte</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_cta, col_s2 = st.columns([1.2, 1.6, 1.2])
        with col_cta:
            if st.button("Comenzar Práctica  ➔", type="primary", use_container_width=True):
                st.session_state.page = "practica"
                if not st.session_state.history:
                    st.session_state.history.append({
                        "role": "assistant",
                        "content": "¡Hola! Soy tu Tutor de Inecuaciones. Escribe una expresión para empezar (ej. -3x + 5 ≤ 20).",
                        "is_image": False
                    })
                st.rerun()

    # ══════════════════════════════
    # VISTA PRÁCTICA (CHAT)
    # ══════════════════════════════
    elif st.session_state.page == "practica":

        # Chat con scroll interno
        chat_scroll = st.container(height=350, border=False)
        with chat_scroll:
            for msg in st.session_state.history:
                render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))
            if st.session_state.history and st.session_state.history[-1]["role"] == "assistant":
                col_sv, _ = st.columns([2, 4])
                with col_sv:
                    if st.button("☁️ Guardar aprendizaje", key="btn_save"):
                        first = len(st.session_state.clouds) == 0
                        st.session_state.clouds.append(st.session_state.history[-1]["content"])
                        st.toast("¡Guardado! Ve a '☁️ Nubes' en el panel." if first else "¡Guardado en Mis Nubes!")
                        st.rerun()

            # ── ANCLA DE AUTO-SCROLL: siempre al final del contenedor ──
            st.markdown(
                '<div id="chat-bottom"></div>'
                '<script>'
                '(function(){'
                '  var el = document.getElementById("chat-bottom");'
                '  if(el){'
                '    var scrollable = el.closest("[data-testid=\\"stVerticalBlockBorderWrapper\\"]")'
                '                  || el.closest(".stVerticalBlock");'
                '    // Sube por el DOM hasta encontrar el div con overflow:auto (el contenedor con height)'
                '    var node = el.parentElement;'
                '    while(node){'
                '      var st = window.getComputedStyle(node);'
                '      if(st.overflowY === "auto" || st.overflowY === "scroll"){'
                '        node.scrollTop = node.scrollHeight;'
                '        break;'
                '      }'
                '      node = node.parentElement;'
                '    }'
                '  }'
                '})();'
                '</script>',
                unsafe_allow_html=True
            )

        # Barra de herramientas (fija debajo del chat)
        st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:6px 0 4px 0;'>",
                    unsafe_allow_html=True)

        col_sym, col_up = st.columns([3, 2])
        with col_sym:
            st.markdown("""
            <div style='padding-top:6px;'>
                <span style='color:#8B0000;font-size:10px;font-weight:700;
                             text-transform:uppercase;letter-spacing:1px;'>Copia:</span>
                <span style='color:#0F172A;font-size:16px;font-family:monospace;
                             letter-spacing:2px;margin-left:6px;'>≤ ≥ ≠ ∞ ∪ ∩</span>
            </div>""", unsafe_allow_html=True)

        with col_up:
            # Label visible para que el usuario sepa que puede subir imagen
            st.markdown(
                "<span style='color:#8B0000;font-size:10px;font-weight:700;"
                "text-transform:uppercase;letter-spacing:1px;'>📎 Adjuntar imagen:</span>",
                unsafe_allow_html=True
            )
            uploaded_image = st.file_uploader(
                "Adjuntar imagen",
                type=['png', 'jpg', 'jpeg'],
                label_visibility="collapsed",
                key=f"up_{st.session_state.uploader_key}"
            )

        user_input = st.chat_input("Escribe tu duda...")

        if user_input:
            img_b64 = encode_image(uploaded_image) if uploaded_image else None
            st.session_state.history.append({
                "role": "user", "content": user_input,
                "image_b64": img_b64, "is_image": bool(img_b64)
            })
            with st.spinner("Analizando..."):
                reply = get_ai_response(user_input, uploaded_image)
            st.session_state.history.append({
                "role": "assistant", "content": reply, "is_image": False
            })
            if uploaded_image:
                st.session_state.uploader_key += 1
            st.rerun()