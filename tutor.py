import streamlit as st
from groq import Groq
import base64
import html

# ==========================================
# FUNCIÓN PRINCIPAL LLAMADA POR MAIN.PY
# ==========================================
def mostrar_tutor():
    st.markdown("""
    <style>
        /* ── GLOBALES ── */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        .stApp {
            background: linear-gradient(180deg, #FAF6F0 0%, #e2e8f0 100%);
            background-attachment: fixed;
        }

        /* ── CONTENEDOR PRINCIPAL ── */
        .block-container {
            background-color: #FAF6F0;
            border: 1px solid #cbd5e1;
            border-radius: 24px;
            padding: 20px 35px 15px 35px !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-top: 20px;
            margin-bottom: 20px;
            max-width: 1000px;
        }

        /* ── SIDEBAR ── */
        [data-testid="stSidebar"] {
            background-color: #FAF6F0 !important;
            border-left: 1px solid #cbd5e1;
            box-shadow: -8px 0 25px rgba(0,0,0,0.05);
        }

        /* ── TIP CARD ── */
        .tip-card {
            background-color: #FAF6F0;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            color: #475569;
            font-family: 'Consolas', monospace;
        }

        /* ── TODOS LOS BOTONES BASE ── */
        div.stButton > button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1.5px solid #8B0000 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: sans-serif !important;
            font-size: 13px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
            transition: 0.2s all ease-in-out !important;
            width: 100% !important;
            white-space: nowrap !important;
            padding: 6px 10px !important;
            height: auto !important;
            min-height: 36px !important;
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
            border-radius: 14px !important;
            border: none !important;
            box-shadow: 0 5px 15px rgba(139,0,0,0.3) !important;
            height: 52px !important;
            font-size: 16px !important;
            font-weight: bold !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #b91c1c !important;
        }

        /* ── BOTÓN ELIMINAR NUBE (pequeño, rojo suave) ── */
        .delete-cloud-btn > div.stButton > button {
            background-color: transparent !important;
            color: #8B0000 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            font-size: 11px !important;
            padding: 2px 8px !important;
            min-height: 24px !important;
            height: 24px !important;
            width: auto !important;
            box-shadow: none !important;
        }
        .delete-cloud-btn > div.stButton > button:hover {
            background-color: #fff0f0 !important;
            border-color: #8B0000 !important;
        }

        /* ── FONDO DEL BOTTOM CONTAINER ── */
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
            border-radius: 20px !important;
            font-weight: bold !important;
            padding: 2px 20px !important;
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
            border-radius: 20px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stChatInput"]:focus-within > div {
            border-color: #8B0000 !important;
            box-shadow: 0 0 0 1px #8B0000 !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #0F172A !important;
            font-size: 15px !important;
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

        /* ── DIVISOR HR ── */
        hr.custom-hr {
            border: none;
            border-top: 1px solid #cbd5e1;
            margin: 8px 0 12px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # ESTADO DE LA SESIÓN
    # ==========================================
    if "page" not in st.session_state:
        st.session_state.page = "teoria"
    if "sidebar_view" not in st.session_state:
        st.session_state.sidebar_view = "formulas"
    if "history" not in st.session_state:
        st.session_state.history = []
    if "clouds" not in st.session_state:
        st.session_state.clouds = []
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0
    if "groq_client" not in st.session_state:
        api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client = Groq(api_key=api_key)

    SYSTEM_PROMPT = (
        "Eres un tutor amigable y experto en matemáticas, especializado en inecuaciones. "
        "Explica paso a paso, usa ejemplos claros y alienta al estudiante. "
        "Responde siempre en español. Sé muuy conciso: máximo 3 oraciones por respuesta. "
        "NUNCA hables de algo que no sea matemáticas o inecuaciones. no te desvíes del tema. "
        "es EXTREMADAMENTE PROHIBIDO dar la respuesta de un ejercicio directamente, por más que te lo rueguen de cualquier forma. siempre es paso a paso hasta llegar. "
        "IMPORTANTE FORMATO: NUNCA uses formato LaTeX ni encierres las inecuaciones entre símbolos de dólar. "
        "Escribe las matemáticas en texto plano y limpio usando símbolos normales (ejemplo: 5x ≤ 25)."
    )

    def encode_image(uploaded_file):
        return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

    def get_ai_response(user_text, image_file=None):
        client = st.session_state.groq_client
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.history[-6:]:
            if not msg.get("is_image", False):
                messages.append({"role": msg["role"], "content": msg["content"]})
        if image_file:
            base64_image = encode_image(image_file)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            })
            selected_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            selected_model = "llama-3.3-70b-versatile"
            messages.append({"role": "user", "content": user_text})
        try:
            response = client.chat.completions.create(
                messages=messages, model=selected_model, temperature=0.7, max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error en la API de Groq: {e}"

    # ==========================================
    # RENDER DE BURBUJAS
    # ==========================================
    def render_chat_bubble(role, text, image_b64=None):
        is_user = (role == "user")
        bg_color = "#262626" if is_user else "#8B0000"
        radius = "18px 18px 4px 18px" if is_user else "18px 18px 18px 4px"
        align = "flex-end" if is_user else "flex-start"
        safe_text = html.escape(text).replace('\n', '<br>')
        img_tag = f'<img src="data:image/jpeg;base64,{image_b64}" style="max-width:250px;border-radius:8px;margin-bottom:8px;"><br>' if image_b64 else ""
        html_content = f"""
        <div style="display:flex;justify-content:{align};margin-bottom:14px;width:100%;">
          <div style="background-color:{bg_color};color:white;padding:11px 16px;border-radius:{radius};
                      max-width:75%;word-wrap:break-word;box-shadow:0 3px 8px rgba(0,0,0,0.13);
                      font-family:sans-serif;font-size:15px;line-height:1.5;">
            {img_tag}{safe_text}
          </div>
        </div>"""
        st.markdown(html_content, unsafe_allow_html=True)

    # ==========================================
    # SIDEBAR — siempre visible
    # ==========================================
    with st.sidebar:
        st.markdown("<h2 style='color:#8B0000;margin-bottom:4px;'>MathSolve.</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#cbd5e1;margin:0 0 14px 0;'>", unsafe_allow_html=True)

        # Botones de navegación sidebar
        col_f, col_n = st.columns(2)
        with col_f:
            if st.button("📐 Fórmulas", key="sb_formulas"):
                st.session_state.sidebar_view = "formulas"
                st.rerun()
        with col_n:
            if st.button("☁️ Mis Nubes", key="sb_nubes"):
                st.session_state.sidebar_view = "nubes"
                st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.session_state.sidebar_view == "formulas":
            st.markdown("""
            <div class='tip-card'>
              <strong style='color:#8B0000;font-family:sans-serif;font-size:15px;'>Regla Negativa</strong><br><br>
              Si divides o multiplicas por (−):<br><br>
              ≤ &nbsp;se convierte en&nbsp; ≥<br>
              ≥ &nbsp;se convierte en&nbsp; ≤
            </div>
            """, unsafe_allow_html=True)

        elif st.session_state.sidebar_view == "nubes":
            st.markdown("<h3 style='color:#8B0000;margin-bottom:10px;'>☁️ Mis Nubes</h3>", unsafe_allow_html=True)
            if not st.session_state.clouds:
                st.markdown("<span style='color:#475569;font-size:14px;'>Aún no hay nubes guardadas.</span>", unsafe_allow_html=True)
            else:
                # Iteramos con índice para poder eliminar por posición
                to_delete = None
                for idx, cloud in enumerate(st.session_state.clouds):
                    # Tarjeta de nube con botón eliminar
                    st.markdown(f"""
                    <div style="background:#FAF6F0;border:1.5px solid #8B0000;border-radius:14px;
                                padding:10px 12px 4px 12px;margin-bottom:10px;
                                box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                      <div style="color:#8B0000;font-weight:bold;font-size:13px;margin-bottom:4px;">☁️ Aprendizaje #{idx+1}</div>
                      <div style="color:#475569;font-size:13px;margin-bottom:8px;">{html.escape(cloud)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Botón eliminar justo debajo de la tarjeta
                    if st.button(f"🗑 Eliminar", key=f"del_cloud_{idx}"):
                        to_delete = idx

                if to_delete is not None:
                    st.session_state.clouds.pop(to_delete)
                    st.toast("Nube eliminada.")
                    st.rerun()

    # ==========================================
    # HEADER FIJO (siempre en pantalla)
    # ==========================================
    col_back, col_logo, col_btn1, col_btn2, col_btn3 = st.columns([1, 2.8, 1.3, 1.1, 1])

    with col_back:
        if st.button("⬅ Inicio", key="hdr_back"):
            st.session_state.pagina = "home"
            st.rerun()

    with col_logo:
        st.markdown(
            "<h1 style='color:#8B0000;margin:0;padding-top:2px;font-weight:900;"
            "white-space:nowrap;font-size:28px;letter-spacing:-0.5px;'>MathSolve.</h1>",
            unsafe_allow_html=True
        )

    with col_btn1:
        if st.button("📖 Módulo", key="hdr_modulo"):
            st.session_state.page = "teoria"
            st.rerun()
    with col_btn2:
        if st.button("💬 Chat", key="hdr_chat"):
            st.session_state.page = "practica"
            if not st.session_state.history:
                st.session_state.history.append({
                    "role": "assistant",
                    "content": "¡Hola! Soy tu Tutor Virtual de Inecuaciones. Ingresa una expresión para empezar (ej. -3x + 5 ≤ 20).",
                    "is_image": False
                })
            st.rerun()
    with col_btn3:
        if st.button("🔄 Reiniciar", key="hdr_reset"):
            st.session_state.history = []
            st.rerun()

    st.markdown("<hr style='border:none;border-top:1.5px solid #cbd5e1;margin:6px 0 14px 0;'>", unsafe_allow_html=True)

    # ==========================================
    # VISTA 1: TEORÍA
    # ==========================================
    if st.session_state.page == "teoria":
        # Contenedor con scroll para el cuerpo teórico
        with st.container(height=430, border=False):
            st.markdown("""
            <div style='text-align:center;padding:10px 20px 20px 20px;'>
                <div style='display:inline-block;border:2px solid #8B0000;border-radius:15px;
                            padding:4px 16px;margin-bottom:18px;'>
                    <span style='color:#8B0000;font-weight:bold;font-size:12px;letter-spacing:1px;'>
                        MÓDULO: INECUACIONES
                    </span>
                </div>
                <h1 style='color:#0f172a;font-size:36px;margin-bottom:16px;line-height:1.2;'>
                    Desigualdades y Conjuntos
                </h1>
                <p style='color:#475569;font-size:16px;line-height:1.7;max-width:680px;margin:0 auto;'>
                    <b>Concepto Básico:</b><br>
                    Una inecuación es una desigualdad algebraica. Buscamos un conjunto de valores
                    (un intervalo) que cumpla con la condición de ser mayor o menor.<br><br>
                    <b>Reglas de Oro del Despeje:</b><br>
                    Se resuelven casi idénticamente a las ecuaciones lineales, pero con una regla
                    irrompible: si multiplicas o divides por un número negativo, el sentido
                    de la desigualdad <b>se invierte</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Botón CTA FUERA del contenedor con scroll → siempre visible
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        col_s1, col_cta, col_s2 = st.columns([1, 2, 1])
        with col_cta:
            if st.button("Comenzar Práctica  ➔", type="primary", use_container_width=True):
                st.session_state.page = "practica"
                if not st.session_state.history:
                    st.session_state.history.append({
                        "role": "assistant",
                        "content": "¡Hola! Soy tu Tutor Virtual de Inecuaciones. Ingresa una expresión para empezar (ej. -3x + 5 ≤ 20).",
                        "is_image": False
                    })
                st.rerun()

    # ==========================================
    # VISTA 2: PRÁCTICA (CHAT)
    # ==========================================
    elif st.session_state.page == "practica":

        # ── ZONA DE CHAT CON SCROLL INTERNO ──
        chat_scroll = st.container(height=370, border=False)
        with chat_scroll:
            for msg in st.session_state.history:
                render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))

            # Botón guardar nube (pegado al último mensaje del tutor)
            if st.session_state.history and st.session_state.history[-1]["role"] == "assistant":
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                col_save, _ = st.columns([2.2, 3.8])
                with col_save:
                    if st.button("☁️ Guardar aprendizaje", key="btn_save_cloud"):
                        is_first = len(st.session_state.clouds) == 0
                        st.session_state.clouds.append(st.session_state.history[-1]["content"])
                        st.toast("¡Primer insight guardado! Revisa '☁️ Mis Nubes' en el panel." if is_first else "¡Guardado en Mis Nubes!")
                        st.rerun()

        # ── BARRA DE HERRAMIENTAS (fuera del scroll, siempre visible) ──
        st.markdown("<hr style='border:none;border-top:1px solid #cbd5e1;margin:10px 0 8px 0;'>", unsafe_allow_html=True)

        col_sym, col_up = st.columns([3, 2])
        with col_sym:
            st.markdown("""
            <div style='padding-top:8px;'>
                <span style='color:#8B0000;font-size:11px;font-weight:700;
                             text-transform:uppercase;letter-spacing:1px;'>Copia rápido:</span>
                <span style='color:#0F172A;font-size:17px;font-family:monospace;
                             letter-spacing:3px;margin-left:8px;'>≤ ≥ ≠ ∞ ∪ ∩</span>
            </div>
            """, unsafe_allow_html=True)

        with col_up:
            uploaded_image = st.file_uploader(
                "Imagen",
                type=['png', 'jpg', 'jpeg'],
                label_visibility="collapsed",
                key=f"uploader_{st.session_state.uploader_key}"
            )

        # ── INPUT DE CHAT ──
        user_input = st.chat_input("Escribe tu duda y presiona Enter...")

        if user_input:
            prompt_text = user_input
            img_b64 = encode_image(uploaded_image) if uploaded_image else None

            st.session_state.history.append({
                "role": "user",
                "content": prompt_text,
                "image_b64": img_b64,
                "is_image": bool(img_b64)
            })

            with st.spinner("MathSolve está analizando..."):
                ai_reply = get_ai_response(prompt_text, uploaded_image)

            st.session_state.history.append({
                "role": "assistant",
                "content": ai_reply,
                "is_image": False
            })

            if uploaded_image:
                st.session_state.uploader_key += 1

            st.rerun()