import streamlit as st
from groq import Groq
import base64
import html

def mostrar_tutor():
    # ── CSS ULTRA-COMPACTO PARA ENCAJAR EN UNA PANTALLA ──
    st.markdown("""
    <style>
        /* Ocultar elementos nativos estorbosos */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stHeader"] { background-color: transparent !important; box-shadow: none !important; }
        [data-testid="stToolbar"] { display: none !important; }

        /* Fondo general crema inquebrantable */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
            background-color: #FAF6F0 !important;
            background: #FAF6F0 !important;
            overflow: hidden !important; /* Evita el scroll global de la página */
        }

        /* ── REDUCCIÓN DE ESPACIOS CRÍTICA ── */
        .main .block-container {
            padding-top: 10px !important; /* Casi nada de espacio arriba */
            padding-bottom: 0px !important; 
            padding-left: 20px !important;
            padding-right: 20px !important;
            max-width: 980px !important; /* Un poco más ancho para aprovechar */
            margin: 0 auto !important;
            height: 100vh !important; /* Forzar altura completa */
            display: flex;
            flex-direction: column;
        }

        /* Reducir tamaño del Header */
        h1#mathsolve {
            font-size: 24px !important; /* Más pequeño */
            margin-bottom: 0px !important;
        }
        hr {
            margin-top: 5px !important;
            margin-bottom: 10px !important;
            border-color: #cbd5e1 !important;
        }

        /* ── ESTILO BARRA LATERAL (Sidebar) ── */
        [data-testid="stSidebar"] {
            background-color: #FAF6F0 !important;
            border-right: 1px solid #cbd5e1 !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] h2 {
            color: #0F172A !important;
        }

        /* ── CHAT CONTAINER FIJO Y CON SCROLL ── */
        [data-testid="stVerticalBlock"] > div:has([data-testid="stChatInput"]) {
            /* Este es el contenedor que envuelve el chat y el input. 
               Streamlit lo maneja, pero nos aseguramos de que no empuje hacia abajo */
        }

        /* Forzar color crema en la zona fija de abajo */
        div[data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
            background-color: #FAF6F0 !important;
            background: #FAF6F0 !important;
            padding-bottom: 10px !important;
        }

        /* ── BOTONES COMPACTOS ── */
        div.stButton > button {
            background-color: #FAF6F0 !important;
            color: #8B0000 !important;
            border: 1.5px solid #8B0000 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 13px !important; /* Texto más pequeño */
            padding: 2px 10px !important; /* Relleno mínimo */
            transition: 0.2s all ease-in-out !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background-color: #8B0000 !important;
            color: white !important;
        }
        /* Botón de borrar nubes específico */
        div.stButton > button.btn-borrar-nube {
            border: none !important;
            background-color: transparent !important;
            color: #ef4444 !important; /* Rojo */
            font-size: 16px !important;
            padding: 0 !important;
            width: auto !important;
        }

        /* ── CÁMARA E INPUT COMPACTOS ── */
        [data-testid="stCameraInput"] {
            background-color: #FFFFFF !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 5px !important;
            margin-top: 5px !important;
        }

        /* Chat Input más bajo */
        [data-testid="stChatInput"] { padding-bottom: 5px !important; }
        [data-testid="stChatInput"] > div {
            background-color: #FFFFFF !important;
            border-radius: 15px !important;
            height: 40px !important; /* Altura fija baja */
        }
        [data-testid="stChatInput"] textarea { font-size: 14px !important; line-height: 1.2 !important; }

        /* Ajustar espaciado de herramientas */
        [data-testid="stHorizontalBlock"] { gap: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── ESTADO DE SESIÓN ──
    for key, val in [
        ("page", "teoria"),
        ("sidebar_view", "formulas"),
        ("history", []),
        ("clouds", []),
        ("uploader_key", 0),
        ("cam_active", False)
    ]:
        if key not in st.session_state:
            st.session_state[key] = val

    if "groq_client" not in st.session_state:
        st.session_state.groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    SYSTEM_PROMPT = (
        "Eres un tutor amigable y experto en matemáticas, especializado en inecuaciones. Explica paso a paso, usa ejemplos claros y alienta al estudiante. Responde siempre en español. Sé muy conciso: máximo 3 oraciones por respuesta. NUNCA hables de algo que no sea matemáticas. PROHIBIDO dar la respuesta directamente. NUNCA uses LaTeX. Usa texto plano (ej: 5x ≤ 25)."
    )

    def encode_image(f):
        return base64.b64encode(f.getvalue()).decode('utf-8')

    def get_ai_response(user_text, image_file=None):
        client = st.session_state.groq_client
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.history[-5:]: # Reducido historial para velocidad
            if not msg.get("is_image", False):
                messages.append({"role": msg["role"], "content": msg["content"]})
        if image_file:
            b64 = encode_image(image_file)
            messages.append({"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]})
            model = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            messages.append({"role": "user", "content": user_text})
            model = "llama-3.3-70b-versatile"
        try:
            resp = client.chat.completions.create(messages=messages, model=model, temperature=0.7, max_tokens=1024)
            return resp.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {e}"

    def render_chat_bubble(role, text, image_b64=None):
        is_user = role == "user"
        bg = "#262626" if is_user else "#8B0000"
        radius = "12px 12px 2px 12px" if is_user else "12px 12px 12px 2px"
        align = "flex-end" if is_user else "flex-start"
        safe = html.escape(text).replace('\n', '<br>')
        img_tag = f'<img src="data:image/jpeg;base64,{image_b64}" style="max-width:180px;border-radius:6px;margin-bottom:4px;"><br>' if image_b64 else ""
        st.markdown(f"""
        <div style="display:flex;justify-content:{align};margin-bottom:8px;width:100%;">
          <div style="background:{bg};color:white;padding:8px 12px;border-radius:{radius};max-width:80%;word-wrap:break-word;box-shadow:0 2px 5px rgba(0,0,0,0.05);font-family:sans-serif;font-size:14px;line-height:1.4;">
            {img_tag}{safe}
          </div>
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════
    # HEADER (Ultra-compacto)
    # ══════════════════════════════
    # Botones más pequeños en el header
    c_logo, c_m, c_f, c_n, c_reset = st.columns([2.5, 1.2, 1.2, 1.2, 1.2])
    with c_logo:
        st.markdown("<h1 id='mathsolve' style='color:#8B0000;margin:0;font-weight:900;white-space:nowrap;'>MathSolve.</h1>", unsafe_allow_html=True)
    with c_m:
        if st.button("📖 Teoria", key="h_teoria"): st.session_state.page = "teoria"; st.rerun()
    with c_f:
        if st.button("📐 Formulas", key="h_formulas"): st.session_state.sidebar_view = "formulas"; st.rerun()
    with c_n:
        if st.button("☁️ Nubes", key="h_nubes"): st.session_state.sidebar_view = "nubes"; st.rerun()
    with c_reset:
        if st.button("🔄 Reiniciar", key="h_reset"): st.session_state.history = []; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ══════════════════════════════
    # SIDEBAR
    # ══════════════════════════════
    with st.sidebar:
        if st.session_state.sidebar_view == "formulas":
            # Cambiado de "Apoyo Rápido" a "formulas"
            st.markdown("<h2 style='color:#8B0000; font-weight:800; font-size:20px; margin-bottom:10px;'>formulas</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color:#FFFFFF; border-radius:8px; border:1px solid #cbd5e1; padding:10px; color:#0F172A; font-size:13px;">
              <strong style='color:#8B0000;'>Regla del Negativo</strong><br>
              Al multiplicar o dividir por (−):<br>
              ≤ ↔ ≥ | < ↔ >
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#8B0000; font-weight:800; font-size:20px; margin-bottom:10px;'>☁️ Mis Nubes</h2>", unsafe_allow_html=True)
            if not st.session_state.clouds:
                st.markdown("<span style='color:#64748B; font-size:13px;'>Aún no hay nubes.</span>", unsafe_allow_html=True)
            else:
                # BORRADO INDIVIDUAL DE NUBES
                # Usamos una copia de la lista invertida para iterar y borrar por índice original
                nubes_indexed = list(enumerate(st.session_state.clouds))
                for idx, cloud in reversed(nubes_indexed):
                    col_txt, col_btn = st.columns([0.85, 0.15])
                    with col_txt:
                        # Remplazamos saltos de línea por espacios para que no ocupe tanto
                        cloud_preview = html.escape(cloud).replace('\n', ' ')
                        st.markdown(f"""
                        <div style="background:#FFFFFF;border:1px solid #cbd5e1;border-radius:8px;padding:6px 10px;margin-bottom:5px;font-size:12px;color:#0F172A;line-height:1.3; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                          {cloud_preview}
                        </div>""", unsafe_allow_html=True)
                    with col_btn:
                        # Botón invisible con icono de basura
                        if st.button("🗑️", key=f"del_cloud_{idx}", help="Borrar esta nube"):
                            st.session_state.clouds.pop(idx)
                            st.toast("Nube borrada")
                            st.rerun()

    # ══════════════════════════════
    # VISTAS
    # ══════════════════════════════
    if st.session_state.page == "teoria":
        st.markdown("""
        <div style='text-align:center;padding:5px 10px;'>
            <div style='display:inline-block;border:1.5px solid #8B0000;border-radius:10px;padding:2px 12px;margin-bottom:10px;'>
                <span style='color:#8B0000;font-weight:bold;font-size:11px;'>MÓDULO: INECUACIONES</span>
            </div>
            <h2 style='color:#0f172a;font-size:28px;margin:0 0 10px 0;'>Desigualdades</h2>
            <p style='color:#475569;font-size:14px;line-height:1.5;max-width:600px;margin:0 auto 15px auto;text-align:left;'>
                <b>Básico:</b> Una inecuación es una desigualdad. Buscamos el conjunto de valores (intervalo) que cumple la condición.<br>
                <b>Regla de Oro:</b> Si multiplicas o divides por un número <b>negativo</b>, el símbolo se <b>invierte</b> (ej: de < a >).
            </p>
        </div>
        """, unsafe_allow_html=True)
        col_s1, col_cta, col_s2 = st.columns([1, 1.2, 1]) # Usamos columnas más ajustadas para que no se vea deforme
        with col_cta:
            # Aquí añadí use_container_width=True para que el botón se estire y se centre perfectamente
            if st.button("Comenzar Práctica ➔", type="primary", use_container_width=True):
                st.session_state.page = "practica"
                if not st.session_state.history: st.session_state.history.append({"role": "assistant", "content": "¡Hola! Soy tu Tutor. Escribe una inecuación (ej: -3x + 5 ≤ 20) o sube una foto.", "is_image": False})
                st.rerun()

    elif st.session_state.page == "practica":
        # ── ZONA DE CHAT FIJA (Scroll interno nativo de Streamlit container) ──
        # Reducimos altura para que quepa todo lo de abajo
        chat_scroll = st.container(height=320, border=False) 
        with chat_scroll:
            for msg in st.session_state.history:
                render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))
            
            if st.session_state.history and st.session_state.history[-1]["role"] == "assistant":
                col_sv, _ = st.columns([2, 3])
                with col_sv:
                    if st.button("☁️ Guardar Nube", key="btn_save_cloud"):
                        st.session_state.clouds.append(st.session_state.history[-1]["content"])
                        st.toast("¡Guardado en Nubes!")
                        st.rerun()
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) # Espacio final

        # ── HERRAMIENTAS ULTRA-COMPACTAS FIJAS ABAJO ──
        # Remplazamos hr por un divisor más fino
        st.markdown("<div style='border-top:1px solid #cbd5e1; margin: 5px 0;'></div>", unsafe_allow_html=True)
        
        col_sym, col_up, col_cam = st.columns([2.5, 1.2, 1.5])
        with col_sym:
            st.markdown("""<div style='padding-top:2px;'><span style='color:#8B0000;font-size:11px;font-weight:700;'>Copia:</span><span style='color:#0F172A;font-size:15px;font-family:monospace;letter-spacing:3px;margin-left:5px;'>≤≥≠∞∪∩</span></div>""", unsafe_allow_html=True)
        with col_up:
            uploaded_image = st.file_uploader("Adjuntar", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key=f"up_{st.session_state.uploader_key}")
        with col_cam:
            texto_btn = "❌ Cerrar Cámara" if st.session_state.cam_active else "📷 Abrir Cámara"
            if st.button(texto_btn, key="btn_toggle_cam"):
                st.session_state.cam_active = not st.session_state.cam_active
                st.rerun()

        camera_image = None
        if st.session_state.cam_active:
            # La cámara aparece justo arriba del input, dentro del estuche diseñado
            camera_image = st.camera_input("Capturar", label_visibility="collapsed", key=f"cam_{st.session_state.uploader_key}")

        # ── CHAT INPUT NATIVO (Streamlit lo ancla abajo) ──
        user_input = st.chat_input("Escribe tu duda aquí...")

        if user_input:
            img_activa = uploaded_image if uploaded_image else camera_image
            img_b64 = encode_image(img_activa) if img_activa else None
            st.session_state.history.append({"role": "user", "content": user_input, "image_b64": img_b64, "is_image": bool(img_b64)})
            with st.spinner("Pensando..."): reply = get_ai_response(user_input, img_activa)
            st.session_state.history.append({"role": "assistant", "content": reply, "is_image": False})
            if img_activa:
                st.session_state.uploader_key += 1
                st.session_state.cam_active = False
            st.rerun()

# Para ejecutarlo directamente si pruebas este archivo solo
if __name__ == "__main__":
    st.set_page_config(page_title="MathSolve Tutor", layout="wide")
    mostrar_tutor()