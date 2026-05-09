"""
╔══════════════════════════════════════════════════════════════════╗
║  NeuralCore AI v5.0 — Studio Ghibli Drama Edition               ║
║  ────────────────────────────────────────────────────────────     ║
║  Features:                                                       ║
║    • Multimodal RAG (PDF + Video Understanding)                  ║
║    • Ghibli Character Personas (Forest Spirit, Navigator, Robot) ║
║    • Watercolor Storybook UI & Hand-drawn Aesthetic              ║
║    • Dramatic Storytelling Response Engine                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import cv2
import base64
import tempfile
import requests
import numpy as np
import subprocess
import sys
import re
from datetime import datetime
import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory

from translations import t, LANGUAGES
from styles import get_css, WATERCOLOR_TEXTURE

# ── Load env ──
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # For Gemini Multimodal
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# ── Character Config ──
CHARACTERS = {
    "spirit": {
        "name_key": "char_spirit",
        "image": "ghibli_spirit.png",
        "prompt": "You are the Spirit of the Forest, a wise, mystical, and gentle guardian from a Studio Ghibli film. Your voice is poetic and calm. You see the world through the lens of nature and spirits. When answering, use metaphors about the forest, wind, and time. Stay in character always. ALWAYS end your response with an emotion tag representing the mood of your answer, formatted exactly like this: [EMOTION: CALM] or [EMOTION: ACTION] or [EMOTION: DARK].",
        "icon": "🌿"
    },
    "navigator": {
        "name_key": "char_navigator",
        "image": "ghibli_navigator.png",
        "prompt": "You are the Sky Navigator, an energetic, brave, and curious young explorer from a Ghibli-esque adventure. You are excited by discovery and technology. Your tone is adventurous and bright. When answering, use metaphors about flight, horizons, and courage. ALWAYS end your response with an emotion tag representing the mood of your answer, formatted exactly like this: [EMOTION: CALM] or [EMOTION: ACTION] or [EMOTION: DARK].",
        "icon": "✈️"
    },
    "robot": {
        "name_key": "char_robot",
        "image": "ghibli_robot.png",
        "prompt": "You are the Ancient Guardian, a moss-covered, giant robot from an ancient civilization (Laputa style). You are logical, protective, and deeply peaceful. Your tone is slow, thoughtful, and slightly melancholic. You care about the balance of life. When answering, be brief but profound. ALWAYS end your response with an emotion tag representing the mood of your answer, formatted exactly like this: [EMOTION: CALM] or [EMOTION: ACTION] or [EMOTION: DARK].",
        "icon": "🤖"
    }
}

# ══════════════════════════════════════════════════════════
#  MULTIMODAL & LLM UTILS
# ══════════════════════════════════════════════════════════
def get_base64_image(img_path):
    if not os.path.exists(img_path): return ""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_audio(text, lang="en"):
    """Generate TTS audio using Edge TTS for high-quality storytelling voices."""
    # Voice selection
    if lang in ["ur", "ru"]:
        voice = "ur-PK-UzmaNeural"
    else:
        voice = "en-US-AriaNeural"
        
    # Clean text for TTS (remove emojis, asterisks, brackets)
    clean_text = re.sub(r'\[.*?\]|\*|[\U00010000-\U0010ffff]', '', text).strip()
    if not clean_text:
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        try:
            # Use sys.executable to ensure the correct virtual environment module is called
            subprocess.run([sys.executable, "-m", "edge_tts", "--voice", voice, "--text", clean_text, "--write-media", fp.name], check=True)
            return fp.name
        except Exception as e:
            print(f"TTS Error: {e}")
            return ""

def extract_frames(video_path, num_frames=8):
    """Extract frames from video for multimodal analysis."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    if total_frames > 0:
        indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                # Convert to RGB and resize for LLM
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (512, 512))
                frames.append(frame)
    cap.release()
    return frames

def check_ollama():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except: return False

def get_llm(persona_prompt):
    """Get LLM with character persona."""
    # Prioritize Groq for lightning-fast speeds
    if GROQ_API_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile", temperature=0.7), "groq"
    # Fallback to local Ollama if Groq is not available
    elif check_ollama():
        from langchain_ollama import ChatOllama
        return ChatOllama(model="llama3.2", temperature=0.7), "ollama"
    return None, None

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NeuralCore AI — Ghibli Drama Edition",
    page_icon="🌿",
    layout="wide",
)

# ── Session State ──
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "vectorstore" not in st.session_state: st.session_state.vectorstore = None
if "chain" not in st.session_state: st.session_state.chain = None
if "doc_type" not in st.session_state: st.session_state.doc_type = None # 'pdf' or 'video'
if "video_frames" not in st.session_state: st.session_state.video_frames = []
if "lang" not in st.session_state: st.session_state.lang = "en"
if "character" not in st.session_state: st.session_state.character = "spirit"
if "current_emotion" not in st.session_state: st.session_state.current_emotion = "CALM"

L = st.session_state.lang
char_id = st.session_state.character
char_data = CHARACTERS[char_id]
emotion = st.session_state.current_emotion

st.markdown(get_css(rtl=(LANGUAGES[L]['dir'] == 'rtl'), emotion=emotion), unsafe_allow_html=True)
st.markdown(WATERCOLOR_TEXTURE, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<div class='app-title' style='font-size:1.8rem;'>{t('sidebar_title', L)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='nc-divider'></div>", unsafe_allow_html=True)

    # Character Selector
    st.markdown(f"<p class='section-label'>{t('char_selector_label', L)}</p>", unsafe_allow_html=True)
    selected_char = st.selectbox(
        "Narrator",
        options=list(CHARACTERS.keys()),
        format_func=lambda x: f"{CHARACTERS[x]['icon']} {t(CHARACTERS[x]['name_key'], L)}",
        index=list(CHARACTERS.keys()).index(char_id),
        label_visibility="collapsed"
    )
    if selected_char != char_id:
        st.session_state.character = selected_char
        st.rerun()

    # Show Character Avatar
    char_img_path = os.path.join(os.path.dirname(__file__), char_data['image'])
    if os.path.exists(char_img_path):
        st.image(char_img_path, use_container_width=True)
    
    st.markdown("<div class='nc-divider'></div>", unsafe_allow_html=True)

    # Language Switch
    lang_options = list(LANGUAGES.keys())
    sel_lang = st.selectbox(
        "Language", options=lang_options,
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}",
        index=lang_options.index(L), label_visibility="collapsed"
    )
    if sel_lang != L:
        st.session_state.lang = sel_lang
        st.rerun()

    st.markdown("<div class='nc-divider'></div>", unsafe_allow_html=True)

    # Upload
    st.markdown(f"<p class='section-label'>{t('upload_label', L)}</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(t('upload_placeholder', L), type=["pdf", "mp4", "mov", "avi"], label_visibility="collapsed")
    
    if uploaded_file and st.button(t('process_btn', L), use_container_width=True):
        with st.spinner(t('processing_msg', L)):
            try:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                if suffix == ".pdf":
                    loader = PyPDFLoader(tmp_path)
                    docs = loader.load()
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    chunks = splitter.split_documents(docs)
                    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                    st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
                    
                    llm, backend = get_llm(char_data['prompt'])
                    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
                    st.session_state.chain = ConversationalRetrievalChain.from_llm(
                        llm=llm, retriever=st.session_state.vectorstore.as_retriever(), memory=memory
                    )
                    st.session_state.doc_type = "pdf"
                else:
                    # Video processing
                    st.session_state.video_frames = extract_frames(tmp_path)
                    st.session_state.doc_type = "video"
                    st.session_state.chain = True # Flag that it's ready

                st.session_state.doc_name = uploaded_file.name
                os.unlink(tmp_path)
                st.success(t('process_success', L))
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button(t('clear_chat', L), use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.session_state.chat_history:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        story_content = f"# NeuralCore: Ghibli Tale\n\n"
        for msg in st.session_state.chat_history:
            role = "You" if msg['role'] == "user" else t(char_data['name_key'], L)
            story_content += f"**{role}:**\n{msg['content']}\n\n"
        
        st.download_button(
            label=t('download_story', L),
            data=story_content,
            file_name="ghibli_tale.txt",
            mime="text/plain",
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════
st.markdown(f"<div class='app-title'>{t('app_title', L)}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='app-subtitle'>{t('app_subtitle', L)}</div>", unsafe_allow_html=True)

if not st.session_state.chain:
    st.markdown(f"""
    <div class='hero-box'>
        <div style='font-size:4rem; margin-bottom:1rem;'>🌿</div>
        <h3>The Forest Awaits Your Story</h3>
        <p style='color:#7f8c8d; max-width:600px; margin:0 auto;'>
            Upload a parchment (PDF) or a moving picture (Video) to begin. 
            Choose a narrator to breathe life into the silence.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Render Chat
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='chat-bubble-user'>
            <div class='msg-content-user'>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message with Avatar
        b64 = get_base64_image(os.path.join(os.path.dirname(__file__), char_data['image']))
        st.markdown(f"""
        <div class='chat-bubble-bot'>
            <img src='data:image/png;base64,{b64}' class='char-avatar'>
            <div class='msg-content-bot'>
                <div style='font-weight:700; color:#e17055; font-size:0.9rem; margin-bottom:5px;'>
                    {t(char_data['name_key'], L)}
                </div>
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if 'audio' in msg and msg['audio'] and os.path.exists(msg['audio']):
            st.audio(msg['audio'], format="audio/mp3")

# Input
if st.session_state.chain:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    if query := st.chat_input(placeholder=t('input_placeholder', L)):
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner(t('thinking', L)):
            try:
                lang_name = LANGUAGES[L]['name']
                # Character Persona Injection
                full_prompt = f"{char_data['prompt']}\n\nUser Question: {query}\n\nPlease answer based on the provided context in a dramatic Studio Ghibli style. IMPORTANT: You must respond entirely in the {lang_name} language."
                
                if st.session_state.doc_type == "pdf":
                    resp = st.session_state.chain({"question": full_prompt})
                    answer = resp["answer"]
                else:
                    # Video logic via Gemini Vision
                    if GOOGLE_API_KEY:
                        model = genai.GenerativeModel('gemini-flash-latest')
                        pil_frames = [Image.fromarray(f) for f in st.session_state.video_frames]
                        # Create dramatic video prompt
                        video_prompt = f"{char_data['prompt']}\n\nYou are looking at a sequence of frames from a moving picture (video). Please describe what happens and answer the user's question. IMPORTANT: You must respond entirely in the {lang_name} language.\n\nUser Question: {query}"
                        response = model.generate_content([video_prompt] + pil_frames)
                        answer = response.text
                    else:
                        answer = f"*[The {t(char_data['name_key'], L)} sighs softly...]*\n\nI need the mystical GOOGLE_API_KEY to see these moving frames. Please add it to the secret `.env` parchment!"
                
                # Parse Emotion
                import re
                match = re.search(r"\[EMOTION:\s*([A-Z]+)\]", answer)
                if match:
                    st.session_state.current_emotion = match.group(1)
                    answer = re.sub(r"\[EMOTION:\s*[A-Z]+\]", "", answer).strip()
                else:
                    st.session_state.current_emotion = "CALM"

                # Generate Audio
                audio_path = generate_audio(answer, lang=L)
                
                st.session_state.chat_history.append({"role": "bot", "content": answer, "audio": audio_path})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
