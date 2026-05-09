"""
╔══════════════════════════════════════════════════════════════╗
║  NeuralCore AI — Studio Ghibli Watercolor Theme              ║
║  Hand-painted paper textures, meadow colors, storybook feel  ║
╚══════════════════════════════════════════════════════════════╝
"""

def get_css(rtl=False, emotion="CALM"):
    direction = "rtl" if rtl else "ltr"
    text_align = "right" if rtl else "left"
    msg_user_margin = "10px 0 10px 0" if rtl else "10px 0 10px 15%"
    msg_bot_margin  = "10px 0 10px 0" if rtl else "10px 15% 10px 0"

    if emotion == "ACTION":
        bg_color1 = "rgba(225, 112, 85, 0.08)"
        bg_color2 = "rgba(253, 203, 110, 0.1)"
    elif emotion == "DARK":
        bg_color1 = "rgba(45, 52, 54, 0.08)"
        bg_color2 = "rgba(108, 92, 231, 0.06)"
    else: # CALM
        bg_color1 = "rgba(120, 165, 90, 0.05)"
        bg_color2 = "rgba(142, 185, 208, 0.08)"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap');

/* ── Ghibli Palette ── */
:root {{
    --gh-paper:     #fdfcf5;
    --gh-ink:       #2d3436;
    --gh-meadow:    #78a55a;
    --gh-sky:       #8eb9d0;
    --gh-sun:       #f9d460;
    --gh-coral:     #e17055;
    --gh-border:    rgba(45, 52, 54, 0.15);
    --gh-texture:   url('https://www.transparenttextures.com/patterns/paper-fibers.png');
}}

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Crimson Pro', serif;
    background-color: var(--gh-paper);
    color: var(--gh-ink);
    direction: {direction};
    text-align: {text_align};
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 2rem; max-width: 1000px; }}

.stApp {{
    background-image: var(--gh-texture);
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: #f7f3e3;
    border-right: 2px solid var(--gh-border);
    background-image: var(--gh-texture);
}}

/* ── Typography ── */
h1, h2, h3, .app-title {{
    font-family: 'Crimson Pro', serif;
    font-weight: 700;
    color: #4a4e4d;
}}

.app-title {{
    font-size: 2.8rem;
    margin-bottom: 0;
    letter-spacing: -0.01em;
    background: linear-gradient(135deg, #4a4e4d, #e17055);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.app-subtitle {{
    font-size: 1.1rem;
    color: #7f8c8d;
    font-style: italic;
    margin-bottom: 2rem;
}}

/* ── Character Avatars ── */
.char-avatar {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 10px;
    background-color: white;
    object-fit: cover;
}}

.chat-bubble-bot {{
    display: flex;
    gap: 15px;
    margin: {msg_bot_margin};
    animation: fadeIn 0.6s ease;
}}

.chat-bubble-user {{
    display: flex;
    justify-content: flex-end;
    margin: {msg_user_margin};
    animation: fadeIn 0.4s ease;
}}

/* ── Messages ── */
.msg-content-bot {{
    background: white;
    padding: 20px;
    border-radius: 0 20px 20px 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    border: 1px solid var(--gh-border);
    font-size: 1.1rem;
    line-height: 1.6;
    position: relative;
}}

.msg-content-user {{
    background: #edf2f4;
    padding: 15px 20px;
    border-radius: 20px 20px 0 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    font-size: 1.05rem;
    color: #2d3436;
}}

/* ── Buttons ── */
.stButton > button {{
    background-color: var(--gh-meadow) !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    font-family: 'Crimson Pro', serif !important;
    font-weight: 600 !important;
    padding: 10px 25px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 0 #5d8145 !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 0 #5d8145 !important;
}}
.stButton > button:active {{
    transform: translateY(2px) !important;
    box-shadow: 0 0px 0 #5d8145 !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input {{
    background: white !important;
    border: 2px solid var(--gh-border) !important;
    border-radius: 15px !important;
    padding: 12px 20px !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.1rem !important;
}}

/* ── Watercolor Animation ── */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.watercolor-bg {{
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2;
    background: radial-gradient(circle at 10% 20%, {bg_color1} 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, {bg_color2} 0%, transparent 40%);
    transition: background 2s ease-in-out;
}}

/* ── Source Labels ── */
.source-tag {{
    display: inline-block;
    padding: 2px 10px;
    background: #f1f2f6;
    border-radius: 10px;
    font-size: 0.8rem;
    color: #7f8c8d;
    margin-top: 10px;
    font-family: 'Inter', sans-serif;
}}

/* ── Hero ── */
.hero-box {{
    text-align: center;
    padding: 4rem 2rem;
    background: rgba(255,255,255,0.5);
    border-radius: 30px;
    border: 2px dashed var(--gh-border);
    margin-bottom: 2rem;
}}
</style>
<div class="watercolor-bg"></div>
"""

WATERCOLOR_TEXTURE = """
<div style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:1000; opacity:0.03; background-image:url('https://www.transparenttextures.com/patterns/handmade-paper.png');"></div>
"""
