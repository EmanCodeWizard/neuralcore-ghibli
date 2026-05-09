"""
╔══════════════════════════════════════════════════════════════╗
║  NeuralCore AI — Studio Ghibli Edition Translations          ║
║  Multilingual support with dramatic character personas       ║
╚══════════════════════════════════════════════════════════════╝
"""

LANGUAGES = {
    "en": {"flag": "🇺🇸", "name": "English",    "dir": "ltr"},
    "ru": {"flag": "🇵🇰", "name": "Roman Urdu", "dir": "ltr"},
    "ur": {"flag": "🇵🇰", "name": "اردو",        "dir": "rtl"},
}

T = {
    "app_title": {
        "en": "NeuralCore — Ghibli Edition",
        "ru": "NeuralCore — Ghibli Edition",
        "ur": "نیورل کور — جیبلی ایڈیشن",
    },
    "app_subtitle": {
        "en": "A Dramatic Tale of Documents & Videos",
        "ru": "A Dramatic Tale of Documents & Videos",
        "ur": "دستاویزات اور ویڈیوز کی ایک ڈرامائی کہانی",
    },
    "sidebar_title": {
        "en": "Studio Ghibli AI",
        "ru": "Studio Ghibli AI",
        "ur": "اسٹوڈیو جیبلی اے آئی",
    },
    "upload_label": {
        "en": "📜 UPLOAD STORY (PDF/VIDEO)",
        "ru": "📜 UPLOAD STORY (PDF/VIDEO)",
        "ur": "📜 کہانی اپ لوڈ کریں",
    },
    "upload_placeholder": {
        "en": "Drop a PDF or Video file...",
        "ru": "Drop a PDF or Video file...",
        "ur": "پی ڈی ایف یا ویڈیو فائل ڈراپ کریں...",
    },
    "char_selector_label": {
        "en": "🎭 CHOOSE YOUR NARRATOR",
        "ru": "🎭 CHOOSE YOUR NARRATOR",
        "ur": "🎭 اپنا راوی منتخب کریں",
    },
    "char_spirit": {
        "en": "Spirit of the Forest (Sage)",
        "ru": "Spirit of the Forest",
        "ur": "جنگل کی روح",
    },
    "char_navigator": {
        "en": "Sky Navigator (Adventurer)",
        "ru": "Sky Navigator",
        "ur": "آسمانی نیویگیٹر",
    },
    "char_robot": {
        "en": "Ancient Guardian (Protector)",
        "ru": "Ancient Guardian",
        "ur": "قدیم محافظ",
    },
    "process_btn": {
        "en": "✨ Breathe Life into it",
        "ru": "✨ Breathe Life into it",
        "ur": "✨ اس میں جان ڈالیں",
    },
    "processing_msg": {
        "en": "🌿 Brewing the story... (Extraction in progress)",
        "ru": "🌿 Brewing the story...",
        "ur": "🌿 کہانی تیار ہو رہی ہے...",
    },
    "process_success": {
        "en": "✅ The story is ready to be told.",
        "ru": "✅ The story is ready.",
        "ur": "✅ کہانی سنانے کے لیے تیار ہے۔",
    },
    "thinking": {
        "en": "The narrator is consulting the spirits...",
        "ru": "Narrator is thinking...",
        "ur": "راوی روحوں سے مشورہ کر رہا ہے...",
    },
    "input_placeholder": {
        "en": "Ask the narrator anything...",
        "ru": "Ask the narrator anything...",
        "ur": "راوی سے کچھ بھی پوچھیں...",
    },
    "send_btn": {
        "en": "Ask →",
        "ru": "Ask →",
        "ur": "پوچھیں →",
    },
    "clear_chat": {
        "en": "🗑️ Erase the Memory",
        "ru": "🗑️ Erase the Memory",
        "ur": "🗑️ یادداشت مٹائیں",
    },
    "download_story": {
        "en": "📥 Download Storybook",
        "ru": "📥 Download Storybook",
        "ur": "📥 کہانی ڈاؤن لوڈ کریں",
    },
    "tech_stack": {
        "en": "Alchemy Stack",
        "ru": "Alchemy Stack",
        "ur": "ٹیک اسٹیک",
    },
    "version": {
        "en": "v5.0 — The Ghibli Drama",
        "ru": "v5.0 — The Ghibli Drama",
        "ur": "ورژن 5.0 — جیبلی ڈرامہ",
    },
}

def t(key, lang="en", **kwargs):
    entry = T.get(key, {})
    text = entry.get(lang, entry.get("en", f"[{key}]"))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except:
            pass
    return text
