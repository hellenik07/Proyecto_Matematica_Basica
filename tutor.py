import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import base64
import html


# ── INICIAR EL MENÚ CERRADO POR DEFECTO ──
st.set_page_config(initial_sidebar_state="collapsed")


def mostrar_tutor():
    # ── CSS DEFINITIVO: CENTRADO, BARRA LATERAL FUNCIONAL Y CÁMARA HERMOSA ──
    st.markdown("""
    <style>
        /* Ocultar menú principal nativo */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* ── ESTILO DE LA BARRA LATERAL (NO OCULTARLA) ── */
        [data-testid="stHeader"] {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* ── EL BOTÓN DE LAS 3 RAYITAS (HAMBURGUESA) CON COLOR QUE SE VEA ── */
        [data-testid="collapsedControl"] {
            display: flex !important;
            background-color: #FF6B6B !important;
            border: 2px solid #FF6B6B !important;
            border-radius: 8px !important;
            margin-top: 15px !important;
            margin-left: 15px !important;
            box-shadow: 0 4px 12px rgba(255,107,107,0.4) !important;
            z-index: 999999 !important;
            width: 45px !important;
            height: 45px !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
        }
        
        [data-testid="collapsedControl"]:hover {
            background-color: #FF5252 !important;
            border-color: #FF5252 !important;
            box-shadow: 0 6px 16px rgba(255,82,82,0.5) !important;
        }
        
        /* Ocultar la flecha nativa de Streamlit */
        [data-testid="collapsedControl"] svg {
            display: none !important; 
        }
        
        /* Inyectar las 3 rayitas */
        [data-testid="collapsedControl"]::after {
            content: "☰" !important;
            color: white !important;
            font-size: 26px !important;
            font-weight: 900 !important;
            font-family: sans-serif !important;
        }

        /* Fondo general crema inquebrantable para toda la app y texto forzado */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
            background-color: #FAF6F0 !important;
            background: #FAF6F0 !important;
            color: #0F172A !important; 
        }
        
        .stMarkdown, .stMarkdown p {
            color: #0F172A !important;
        }

        /* Centrado de pantalla */
        .main .block-container {
            padding-top: 60px !important; /* Espacio para que no choque con las 3 rayitas fijo */
            padding-bottom: 90px !important; 
            max-width: 950px !important;
            margin: 0 auto !important; 
        }

        /* Barra lateral - SOLO ESTILO, NO OCULTAR */
        [data-testid="stSidebar"], 
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebarNav"] {
            background-color: #FAF6F0 !important;
            background: #FAF6F0 !important;
            border-right: 1px solid #cbd5e1 !important;
        }
        
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] h2 {
            color: #0F172A !important;
        }

        /* Eliminar contenedor negro inferior */
        div[data-testid="stBottom"], 
        div[data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] {
            background-color: #FAF6F0 !important;
            background: #FAF6F0 !important;
            border-top: none !important;
        }

        /* Botones generales */
        div.stButton > button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1.5px solid #8B0000 !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            transition: 0.2s all ease-in-out !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background-color: #8B0000 !important;
            color: white !important;
        }

        /* Botón primario */
        div.stButton > button[kind="primary"] {
            background-color: #8B0000 !important;
            color: white !important;
            border-radius: 12px !important;
            height: 50px !important;
            font-size: 16px !important;
        }

        /* Entrada de cámara */
        [data-testid="stCameraInput"] {
            background-color: #FFFFFF !important;
            border: 2px solid #cbd5e1 !important;
            border-radius: 16px !important;
            padding: 15px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            margin-top: 15px !important;
        }
        [data-testid="stCameraInput"] button {
            background-color: #8B0000 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
            border: none !important;
            padding-bottom: 10px !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: #FFFFFF !important;
            border: 2px solid #CBD5E1 !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stChatInput"]:focus-within > div {
            border-color: #8B0000 !important;
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

        /* File Uploader */
        [data-testid="stFileUploader"] { padding: 0 !important; margin: 0 !important; }
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
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0px 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)


    # ── ESTADO DE SESIÓN ──
    for key, val in [
        ("page", "practica"), 
        ("sidebar_view", "menu"), 
        ("history", [{ 
            "role": "assistant",
            "content": "¡Hola! Soy tu Tutor de Inecuaciones. Escribe una expresión para empezar (ej. -3x + 5 ≤ 20).",
            "is_image": False
        }]),
        ("clouds", []),
        ("uploader_key", 0),
        ("cam_active", False),
        ("first_cloud_shown", False)
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
        <div style="display:flex;justify-content:{align};margin-bottom:12px;width:100%;">
          <div style="background:{bg};color:white;padding:12px 16px;border-radius:{radius};
                      max-width:80%;word-wrap:break-word;box-shadow:0 3px 8px rgba(0,0,0,0.1);
                      font-family:sans-serif;font-size:15px;line-height:1.5;">
            {img_tag}{safe}
          </div>
        </div>""", unsafe_allow_html=True)


    # ── SIDEBAR MÁGICO (FUNCIONAL) ──
    with st.sidebar:
        st.markdown("<h1 style='color:#8B0000;margin:0 0 20px 0;font-size:28px;font-weight:900;'>MathSolve.</h1>", unsafe_allow_html=True)
        
        if st.session_state.sidebar_view == "menu":
            if st.button("📖 Teoría"):
                st.session_state.sidebar_view = "teoria"; st.rerun()
            if st.button("📐 Fórmulas"):
                st.session_state.sidebar_view = "formulas"; st.rerun()
            if st.button("☁️ Mis Nubes"):
                st.session_state.sidebar_view = "nubes"; st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Botón de reiniciar CON CONFIRMACIÓN
            if st.button("🔄 Reiniciar Chat"):
                st.session_state.sidebar_view = "confirm_reiniciar"; st.rerun()


        elif st.session_state.sidebar_view == "confirm_reiniciar":
            st.markdown("<h2 style='color:#8B0000; font-weight:800; margin-top:10px;'>⚠️ Reiniciar Chat</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#0F172A;'>¿Estás seguro de que quieres reiniciar todo? Se perderá el chat y las nubes guardadas.</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sí, reiniciar", kind="primary"):
                    st.session_state.history = [{
                        "role": "assistant",
                        "content": "¡Hola! Soy tu Tutor de Inecuaciones. Escribe una expresión para empezar (ej. -3x + 5 ≤ 20).",
                        "is_image": False
                    }]
                    st.session_state.clouds = []
                    st.session_state.first_cloud_shown = False
                    st.session_state.sidebar_view = "menu"
                    st.toast("Chat reiniciado!")
                    st.rerun()
            with col2:
                if st.button("❌ No, volver"):
                    st.session_state.sidebar_view = "menu"; st.rerun()


        elif st.session_state.sidebar_view == "formulas":
            if st.button("⬅ Volver al Menú"):
                st.session_state.sidebar_view = "menu"; st.rerun()
            st.markdown("<h2 style='color:#8B0000; font-weight:800; margin-top:10px;'>Apoyo Rápido</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color:#FFFFFF; border-radius:12px; border:1px solid #cbd5e1; padding:15px; color:#0F172A; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
              <strong style='color:#8B0000; font-size:16px;'>Regla del Negativo</strong><br><br>
              Al multiplicar o dividir por (−):<br><br>
              ≤  se convierte en  ≥<br>
              &lt;  se convierte en  &gt;
            </div>""", unsafe_allow_html=True)


        elif st.session_state.sidebar_view == "teoria":
            if st.button("⬅ Volver al Menú"):
                st.session_state.sidebar_view = "menu"; st.rerun()
            st.markdown("<h2 style='color:#8B0000; font-weight:800; margin-top:10px;'>Teoría</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background-color:#FFFFFF; border-radius:12px; border:1px solid #cbd5e1; padding:15px; color:#0F172A; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
                <h3 style='color:#0f172a;font-size:18px;margin:0 0 10px 0;'>Desigualdades y Conjuntos</h3>
                <p style='color:#475569;font-size:14px;line-height:1.5;margin:0;'>
                    <b>Concepto Básico:</b> Una inecuación es una desigualdad algebraica. Buscamos el conjunto de valores que cumple con la condición de ser mayor o menor.<br><br>
                    <b>Regla de Oro:</b> Se resuelven casi igual que las ecuaciones lineales, pero si multiplicas o divides por un número <b>negativo</b>, el símbolo de desigualdad se <b>invierte</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)


        elif st.session_state.sidebar_view == "nubes":
            if st.button("⬅ Volver al Menú"):
                st.session_state.sidebar_view = "menu"; st.rerun()
            st.markdown("<h2 style='color:#8B0000; font-weight:800; margin-top:10px;'>☁️ Mis Nubes</h2>", unsafe_allow_html=True)
            if not st.session_state.clouds:
                st.markdown("<span style='color:#0F172A;'>Aún no hay nubes guardadas.</span>", unsafe_allow_html=True)
            else:
                for idx, cloud in enumerate(reversed(st.session_state.clouds)):
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #cbd5e1;border-radius:12px;
                                padding:12px;margin-bottom:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                      <div style="color:#8B0000;font-weight:bold;font-size:14px;">☁️ Aprendizaje</div>
                      <div style="color:#0F172A;font-size:14px;margin-top:6px;line-height:1.5;">{html.escape(cloud)}</div>
                    </div>""", unsafe_allow_html=True)


    # ── VISTA PRINCIPAL (SOLO CHAT) ──
    chat_scroll = st.container(height=420, border=False)
    with chat_scroll:
        for msg in st.session_state.history:
            render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))
        
        if st.session_state.history and st.session_state.history[-1]["role"] == "assistant":
            col_sv, _ = st.columns([1.5, 4])
            with col_sv:
                if st.button("☁️ Guardar Nube", key="btn_save"):
                    nueva_nube = st.session_state.history[-1]["content"]
                    
                    # Verificar si ya existe una nube con el mismo mensaje
                    if nueva_nube in st.session_state.clouds:
                        st.toast("⚠️ Esta nube ya está guardada!", icon="⚠️")
                    else:
                        st.session_state.clouds.append(nueva_nube)
                        
                        # Si es la primera nube, mostrar mensaje de ayuda
                        if not st.session_state.first_cloud_shown:
                            st.toast("🎉 ¡Primera nube guardada!", icon="🎉")
                            st.modal("☁️ **Qué son las Nubes**\n\nLas nubes guardan los aprendizajes importantes de tu chat. Puedes verlas siempre en **☁️ Mis Nubes** en el menú de la izquierda.\n\n**Para verlas:** Abre el menú (☰) → Haz clic en **☁️ Mis Nubes**")
                            st.session_state.first_cloud_shown = True
                        else:
                            st.toast("¡Guardado en Mis Nubes!")
                        st.rerun()
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


        # Auto-scroll corregido y seguro
        components.html(
            f"""
            <script>
                // Actualización de scroll: {len(st.session_state.history)}
                var iframe = window.frameElement;
                if(iframe) {{
                    var el = iframe;
                    while(el && el.parentElement) {{
                        el = el.parentElement;
                        var style = window.getComputedStyle(el);
                        if(style.overflowY === 'auto' || style.overflowY === 'scroll') {{
                            el.scrollTop = el.scrollHeight;
                            break;
                        }}
                    }}
                }}
            </script>
            """, 
            height=0, 
            width=0
        )


    st.markdown("<hr style='border:none;border-top:1px solid #cbd5e1;margin:10px 0;'>", unsafe_allow_html=True)


    # Herramientas debajo del chat
    col_sym, col_up, col_cam = st.columns([2.2, 1.3, 1.5])
    
    with col_sym:
        st.markdown("""
        <div style='padding-top:10px;'>
            <span style='color:#8B0000;font-size:12px;font-weight:700;'>Copia rápido:</span>
            <span style='color:#0F172A;font-size:16px;font-family:monospace;letter-spacing:4px;margin-left:8px;'>≤ ≥ ≠ ∞ ∪ ∩</span>
        </div>""", unsafe_allow_html=True)


    with col_up:
        uploaded_image = st.file_uploader(
            "Adjuntar",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed",
            key=f"up_{st.session_state.uploader_key}"
        )
        
    with col_cam:
        texto_btn = "❌ Cerrar Cámara" if st.session_state.cam_active else "📷 Abrir Cámara"
        if st.button(texto_btn, key="btn_toggle_cam"):
            st.session_state.cam_active = not st.session_state.cam_active
            st.rerun()


    camera_image = None
    if st.session_state.cam_active:
        camera_image = st.camera_input("Capturar", label_visibility="collapsed", key=f"cam_{st.session_state.uploader_key}")


    user_input = st.chat_input("Escribe tu duda y presiona Enter...")


    if user_input:
        img_activa = uploaded_image if uploaded_image else camera_image
        img_b64 = encode_image(img_activa) if img_activa else None
        
        st.session_state.history.append({
            "role": "user", "content": user_input,
            "image_b64": img_b64, "is_image": bool(img_b64)
        })
        
        with st.spinner("Analizando..."):
            reply = get_ai_response(user_input, img_activa)
            
        st.session_state.history.append({
            "role": "assistant", "content": reply, "is_image": False
        })
        
        if img_activa:
            st.session_state.uploader_key += 1
            st.session_state.cam_active = False
        st.rerun()


# ── EJECUTAR EL TUTOR ──
mostrar_tutor()