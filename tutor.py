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
        /* ── Ocultar elementos nativos de Streamlit ── */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* ── Fondo general y MainCard ── */
        .stApp {
            background: linear-gradient(180deg, #FAF6F0 0%, #e2e8f0 100%) !important;
            background-attachment: fixed !important;
        }

        .block-container {
            background-color: #FAF6F0 !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 24px !important;
            padding: 30px 45px !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
            margin-top: 20px !important;
            max-width: 1000px !important;
        }

        /* ── Modificando la barra lateral ── */
        [data-testid="stSidebar"] {
            background-color: #FAF6F0 !important;
            border-left: 1px solid #cbd5e1 !important;
            box-shadow: -8px 0 25px rgba(0,0,0,0.05) !important;
        }
       
        /* ── TipCard (Apoyo rápido) ── */
        .tip-card {
            background-color: #FAF6F0;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            color: #475569;
            font-family: 'Consolas', monospace;
        }

        /* ── Estilo de botones superiores ── */
        div.stButton > button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1px solid #8B0000 !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            font-family: sans-serif !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05) !important;
            transition: 0.2s all ease-in-out !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background-color: #8B0000 !important;
            color: white !important;
        }

        /* ── Botón CTA (Comenzar Práctica) ── */
        div.stButton > button[kind="primary"] {
            background-color: #8B0000 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 5px 15px rgba(139,0,0,0.3) !important;
            height: 55px !important;
            font-size: 18px !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #b91c1c !important;
        }

        /* ── UPLOADER MINIMALISTA ── */
        [data-testid="stFileUploader"] {
            padding: 0 !important;
        }
        [data-testid="stFileUploader"] section {
            padding: 5px 15px !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            background-color: #FAF6F0 !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] svg {
            display: none !important;
        }

        /* ── CHAT INPUT BLINDADO ── */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: #FFFFFF !important;
            border: 2px solid #cbd5e1 !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stChatInput"]:focus-within > div {
            border-color: #8B0000 !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #0F172A !important;
            font-size: 16px !important;
        }
        [data-testid="stChatInputSubmitButton"] {
            color: #8B0000 !important;
            background-color: transparent !important;
        }
        [data-testid="stChatInputSubmitButton"] svg {
            fill: #8B0000 !important;
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
        "NUNCA hables de algo que no sea matemáticas o inecuaciones. "
        "es EXTREMADAMENTE PROHIBIDO dar la respuesta de un ejercicio directamente, guía paso a paso. "
        "IMPORTANTE FORMATO: NUNCA uses formato LaTeX ni encierres las inecuaciones entre símbolos de dólar. "
        "Escribe las matemáticas en texto plano y limpio (ejemplo: 5x ≤ 25)."
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

    def render_chat_bubble(role, text, image_b64=None):
        is_user = (role == "user")
        bg_color = "#262626" if is_user else "#8B0000"
        radius = "18px 18px 4px 18px" if is_user else "18px 18px 18px 4px"
        align = "flex-end" if is_user else "flex-start"
       
        safe_text = html.escape(text).replace('\n', '<br>')
        img_tag = f'<img src="data:image/jpeg;base64,{image_b64}" style="max-width: 250px; border-radius: 8px; margin-bottom: 8px;"><br>' if image_b64 else ""
       
        html_content = f"""<div style="display: flex; justify-content: {align}; margin-bottom: 15px; width: 100%;">
        <div style="background-color: {bg_color}; color: white; padding: 12px 18px; border-radius: {radius}; max-width: 75%; width: fit-content; word-wrap: break-word; box-shadow: 0 4px 10px rgba(0,0,0,0.15); font-family: sans-serif; font-size: 15px; line-height: 1.5;">
        {img_tag}{safe_text}
        </div>
        </div>"""
        st.markdown(html_content, unsafe_allow_html=True)


    # ==========================================
    # UI: HEADER (ESTÁTICO)
    # ==========================================
    col_back, col_logo, col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1.5, 1, 1, 1, 1])

    with col_back:
        if st.button("⬅ Inicio"):
            st.session_state.pagina = "home"
            st.rerun()

    with col_logo:
        st.markdown("<h1 style='color: #8B0000; margin-top: -15px; font-weight: bold; white-space: nowrap;'>MathSolve.</h1>", unsafe_allow_html=True)

    with col_btn1:
        if st.button("📖 Teórico"):
            st.session_state.page = "teoria"
            st.rerun()
    with col_btn2:
        if st.button("📐 Fórmulas"):
            st.session_state.sidebar_view = "formulas"
            st.rerun()
    with col_btn3:
        if st.button("☁️ Nubes"):
            st.session_state.sidebar_view = "nubes"
            st.rerun()
    with col_btn4:
        if st.button("🔄 Reiniciar"):
            st.session_state.history = []
            st.rerun()

    st.markdown("<hr style='margin-top: 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)


    # ==========================================
    # UI: SIDEBAR
    # ==========================================
    with st.sidebar:
        if st.session_state.sidebar_view == "formulas":
            st.markdown("<h2 style='color: #8B0000;'>Apoyo Rápido</h2>", unsafe_allow_html=True)
            tip_html = """<div class="tip-card">
            <strong style="color: #8B0000; font-family: sans-serif; font-size: 16px;">Regla Negativa</strong><br><br>
            Si divides o multiplicas por (-):<br><br>
            ≤  se convierte en  ≥<br>
            ≥  se convierte en  ≤
            </div>"""
            st.markdown(tip_html, unsafe_allow_html=True)

        elif st.session_state.sidebar_view == "nubes":
            st.markdown("<h2 style='color: #8B0000;'>☁️ Mis Nubes</h2>", unsafe_allow_html=True)
            if not st.session_state.clouds:
                st.markdown("<span style='color:#475569;'>Aún no hay nubes guardadas.</span>", unsafe_allow_html=True)
            else:
                for idx, cloud in enumerate(reversed(st.session_state.clouds)):
                    cloud_html = f"""<div style="background: #FAF6F0; border: 2px solid #8B0000; border-radius: 16px; padding: 12px; margin-bottom: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
                    <strong style="color: #8B0000;">☁️ Aprendizaje</strong>
                    <div style="color: #475569; margin-top: 8px; font-size: 14px;">{html.escape(cloud)}</div>
                    </div>"""
                    st.markdown(cloud_html, unsafe_allow_html=True)


    # ==========================================
    # VISTA 1: TEORÍA
    # ==========================================
    if st.session_state.page == "teoria":
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='display: inline-block; border: 2px solid #8B0000; border-radius: 15px; padding: 5px 15px; margin-bottom: 20px;'>
                <span style='color: #8B0000; font-weight: bold; font-size: 12px;'>MÓDULO: INECUACIONES</span>
            </div>
            <h1 style='color: #0f172a; font-size: 42px; margin-bottom: 20px;'>Desigualdades y Conjuntos</h1>
            <p style='color: #475569; font-size: 18px; line-height: 1.6; max-width: 700px; margin: 0 auto;'>
                <b>Concepto Básico:</b><br>
                Una inecuación es una desigualdad algebraica. Aquí buscamos un conjunto de valores (un intervalo) que cumpla con la condición de ser mayor o menor.<br><br>
                <b>Reglas de Oro del Despeje:</b><br>
                Se resuelven casi idénticamente a las ecuaciones lineales, pero con una regla irrompible: ¡Si multiplicas o divides por un número negativo, el sentido de la desigualdad se invierte!
            </p>
        </div>
        <br>
        """, unsafe_allow_html=True)
       
        col_space1, col_btn, col_space2 = st.columns([1, 1.5, 1])
        with col_btn:
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
    # VISTA 2: PRÁCTICA (CHAT Y HERRAMIENTAS)
    # ==========================================
    elif st.session_state.page == "practica":
       
        # 1. Contenedor del chat con altura fija (Scroll interno)
        chat_container = st.container(height=400, border=False)
        with chat_container:
            for msg in st.session_state.history:
                render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))

            # Botón de guardar nube (Aparece solo si el último en hablar fue el bot)
            if len(st.session_state.history) > 0 and st.session_state.history[-1]["role"] == "assistant":
                col_save, _ = st.columns([1, 3])
                with col_save:
                    if st.button("☁️ Guardar Nube", use_container_width=True):
                        st.session_state.clouds.append(st.session_state.history[-1]["content"])
                        st.toast("¡Guardado en Mis Nubes!")
                        st.rerun()
            
            # ESPACIO EN BLANCO INVISIBLE: Esto evita que el último mensaje se corte
            st.markdown("<div style='height: 50px; width: 100%;'></div>", unsafe_allow_html=True)
            
            # AUTO-SCROLL hacia abajo
            st.markdown(
                '''
                <script>
                    var chatContainer = window.parent.document.querySelector('.stVerticalBlock[data-testid="stVerticalBlock"] > div');
                    if (chatContainer) {
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                </script>
                ''', 
                unsafe_allow_html=True
            )

        st.markdown("<hr style='margin: 15px 0 10px 0;'>", unsafe_allow_html=True)

        # 2. Barra de herramientas VISTA: Copia rápida, Subir Foto, Tomar Foto
        col_sym, col_upload, col_cam = st.columns([2, 1.5, 1.5])
        
        with col_sym:
            st.markdown("""
            <div style="padding-top: 15px;">
                <span style='color: #8B0000; font-size: 13px; font-weight: bold;'>Copia rápido:</span>
                <span style='color: #0F172A; font-size: 18px; font-family: monospace; letter-spacing: 2px; margin-left: 5px;'>≤ ≥ ≠ ∞ ∪ ∩</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col_upload:
            uploaded_image = st.file_uploader(
                "📂 Adjuntar",
                type=['png', 'jpg', 'jpeg'],
                label_visibility="collapsed",
                key=f"uploader_{st.session_state.uploader_key}"
            )
            
        with col_cam:
            camera_image = st.camera_input(
                "📷 Foto",
                label_visibility="collapsed",
                key=f"cam_{st.session_state.uploader_key}"
            )

        # 3. Chat Input nativo
        user_input = st.chat_input("Escribe tu duda y presiona Enter...")

        if user_input:
            # Determinamos si se usó la cámara o se subió un archivo
            img_activa = uploaded_image if uploaded_image else camera_image
            img_b64 = encode_image(img_activa) if img_activa else None
           
            st.session_state.history.append({
                "role": "user",
                "content": user_input,
                "image_b64": img_b64,
                "is_image": True if img_b64 else False
            })
           
            # Mostramos inmediatamente el mensaje del usuario
            with chat_container:
                render_chat_bubble("user", user_input, img_b64)

            with st.spinner("MathSolve está analizando..."):
                ai_reply = get_ai_response(user_input, img_activa)
               
            st.session_state.history.append({
                "role": "assistant",
                "content": ai_reply,
                "is_image": False
            })
           
            # Limpiar la cámara/subida para el siguiente mensaje
            if img_activa:
                st.session_state.uploader_key += 1
           
            st.rerun()