import streamlit as st
from groq import Groq
import base64
import html

# ==========================================
# CONFIGURACIÓN (Debe ser lo primero)
# ==========================================
# NOTA: Si este archivo se va a ejecutar a través de main.py, 
# main.py ya tiene su propio st.set_page_config, por lo que podrías 
# necesitar comentar la siguiente línea si te da error al juntarlos.
st.set_page_config(page_title="MathSolve - Inecuaciones SaaS", page_icon="🧮", layout="wide")

# ==========================================
# CSS EXTREMO: RECREANDO EL TEMA PYQT6 (SAGRADO)
# ==========================================
st.markdown("""
<style>
    /* Ocultar elementos nativos de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Gradiente de fondo de la ventana entera (Tono crema #FAF6F0) */
    .stApp {
        background: linear-gradient(180deg, #FAF6F0 0%, #e2e8f0 100%);
        background-attachment: fixed;
    }

    /* MainCard: La tarjeta flotante central */
    .block-container {
        background-color: #FAF6F0; /* Tono crema dominante */
        border: 1px solid #cbd5e1;
        border-radius: 24px;
        padding: 35px 45px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
        margin-bottom: 30px;
        max-width: 1000px;
    }

    /* Modificando la barra lateral (RightPanel) */
    [data-testid="stSidebar"] {
        background-color: #FAF6F0 !important; /* Tono crema dominante */
        border-left: 1px solid #cbd5e1;
        box-shadow: -8px 0 25px rgba(0,0,0,0.05);
    }
   
    /* TipCard (Apoyo rápido) */
    .tip-card {
        background-color: #FAF6F0;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 15px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        color: #475569;
        font-family: 'Consolas', monospace;
    }

    /* Estilo de botones superiores (HeaderButton) */
    div.stButton > button {
        background-color: #FAF6F0; /* Tono crema dominante */
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        font-weight: bold;
        font-family: sans-serif;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: 0.2s all ease-in-out;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #8B0000;
        color: white;
        border-color: #8B0000;
    }

    /* Estilo Botón CTA (Comenzar Práctica) */
    div.stButton > button[kind="primary"] {
        background-color: #8B0000;
        color: white;
        border-radius: 12px;
        border: none;
        box-shadow: 0 5px 15px rgba(139,0,0,0.3);
        height: 55px;
        font-size: 18px;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #b91c1c;
    }

    /* ELIMINAR EL FONDO OSCURO INFERIOR NATIVO DE STREAMLIT */
    [data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
    }
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    /* UPLOADER MINIMALISTA (Adiós a la franja gris gigante) */
    [data-testid="stFileUploader"] {
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] section {
        padding: 5px 15px !important;
        border: 1px solid #cbd5e1 !important; /* Borde limpio, nada de dashed */
        border-radius: 12px !important;
        background-color: #FAF6F0 !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] svg {
        display: none !important; /* Oculta textos e ícono de nube */
    }

    /* InputWrapper nativo de Streamlit (Chat Input) */
    [data-testid="stChatInput"] {
        background-color: #64748b !important; /* Tono claro (Slate 500) para contraste del blanco */
        border: 1px solid #cbd5e1 !important; /* Sin rastro del borde rojo inicial */
        border-radius: 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #cbd5e1 !important; /* Mantiene el borde neutro al escribir, NADA ROJO */
    }
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 16px !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #ffffff !important; /* Placeholder blanco inmaculado */
        opacity: 0.9 !important;
    }
    /* Flecha siempre rojo #8B0000, sin opacidad (no se pone oscura) */
    [data-testid="stChatInputSubmitButton"] {
        color: #8B0000 !important;
        opacity: 1 !important; /* Forzar 100% de luz siempre */
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
# RENDERIZADO DE BURBUJAS HTML CUSTOM
# ==========================================
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
# UI: HEADER
# ==========================================
# Agregamos col_back al principio para el botón de regresar
col_back, col_logo, col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1.5, 1, 1, 1, 1])

with col_back:
    if st.button("⬅ Inicio"):
        st.session_state.pagina = "home"
        st.rerun()

with col_logo:
    st.markdown("<h1 style='color: #8B0000; margin-top: -15px; font-weight: bold;'>MathSolve.</h1>", unsafe_allow_html=True)

with col_btn1:
    if st.button("Módulo Teórico"):
        st.session_state.page = "teoria"
        st.rerun()
with col_btn2:
    if st.button("Fórmulas"):
        st.session_state.sidebar_view = "formulas"
        st.rerun()
with col_btn3:
    if st.button("Mis Nubes ☁️"):
        st.session_state.sidebar_view = "nubes"
        st.rerun()
with col_btn4:
    if st.button("Reiniciar"):
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
# VISTA 2: PRÁCTICA
# ==========================================
elif st.session_state.page == "practica":
   
    for msg in st.session_state.history:
        render_chat_bubble(msg["role"], msg["content"], msg.get("image_b64"))

    # Botón flotante para guardar el último insight
    if len(st.session_state.history) > 0 and st.session_state.history[-1]["role"] == "assistant":
        col_space, col_save = st.columns([4, 1])
        with col_save:
            if st.button("☁️ Guardar Nube"):
                is_first_cloud = len(st.session_state.clouds) == 0
                st.session_state.clouds.append(st.session_state.history[-1]["content"])
               
                # Aquí está la lógica de la notificación de primera nube
                if is_first_cloud:
                    st.toast("¡Primer insight guardado! ☁️ Haz clic en el botón 'Mis Nubes ☁️' de arriba para repasar.")
                else:
                    st.toast("¡Guardado en Mis Nubes!")
                   
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<span style='color: #475569; font-size: 13px;'>Copia rápido: ≤ | ≥ | ≠ | ∞ | ∪ | ∩</span>", unsafe_allow_html=True)
   
    # El key dinámico es lo que evita el bucle de subida
    uploaded_image = st.file_uploader(
        "📎 Adjuntar Ejercicio (Opcional)",
        type=['png', 'jpg', 'jpeg'],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )
   
    # El usuario debe usar el chat input para enviar el mensaje + la imagen adjunta
    user_input = st.chat_input("Escribe tu duda y presiona Enter...")

    if user_input:
        prompt_text = user_input
        img_b64 = encode_image(uploaded_image) if uploaded_image else None
       
        st.session_state.history.append({
            "role": "user",
            "content": prompt_text,
            "image_b64": img_b64,
            "is_image": True if img_b64 else False
        })
       
        render_chat_bubble("user", prompt_text, img_b64)

        with st.spinner("MathSolve está analizando..."):
            ai_reply = get_ai_response(prompt_text, uploaded_image)
           
        st.session_state.history.append({
            "role": "assistant",
            "content": ai_reply,
            "is_image": False
        })
       
        # Incrementamos el key para resetear el uploader si se subió una imagen
        if uploaded_image:
            st.session_state.uploader_key += 1
       
        st.rerun()