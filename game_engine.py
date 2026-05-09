"""
╔══════════════════════════════════════════════════════════════╗
║  DocBot AI — Game Engine                                     ║
║  XP System, Levels, Achievements, Quests                     ║
╚══════════════════════════════════════════════════════════════╝
"""

# ── Level Definitions ──
LEVELS = [
    {"name": "Novice",      "icon": "🌱", "xp": 0,    "key": "level_novice"},
    {"name": "Explorer",    "icon": "🗺️", "xp": 50,   "key": "level_explorer"},
    {"name": "Researcher",  "icon": "🔬", "xp": 150,  "key": "level_researcher"},
    {"name": "Scholar",     "icon": "📚", "xp": 350,  "key": "level_scholar"},
    {"name": "Master",      "icon": "🏆", "xp": 600,  "key": "level_master"},
]

# ── Achievement Definitions ──
ACHIEVEMENTS = [
    {"id": "first_q",    "icon": "❓", "key": "ach_first_question", "desc_en": "Ask your first question"},
    {"id": "doc_load",   "icon": "📄", "key": "ach_doc_loaded",    "desc_en": "Load a document"},
    {"id": "five_q",     "icon": "🧠", "key": "ach_5_questions",   "desc_en": "Ask 5 questions"},
    {"id": "ten_q",      "icon": "🎯", "key": "ach_10_questions",  "desc_en": "Ask 10 questions"},
    {"id": "master",     "icon": "🏆", "key": "ach_master",        "desc_en": "Reach Master level"},
    {"id": "streak_5",   "icon": "🔥", "key": "ach_streak",        "desc_en": "Get a 5x streak"},
]

# ── XP Rewards ──
XP_PER_QUESTION = 15
XP_PER_DOC = 25
XP_STREAK_BONUS = 5  # Extra XP per streak level


def get_level(xp):
    """Return current level info based on XP."""
    current = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl["xp"]:
            current = lvl
    return current


def get_level_index(xp):
    """Return current level index (0-based)."""
    idx = 0
    for i, lvl in enumerate(LEVELS):
        if xp >= lvl["xp"]:
            idx = i
    return idx


def get_xp_progress(xp):
    """Return (current_xp_in_level, xp_needed_for_next, progress_pct)."""
    idx = get_level_index(xp)
    if idx >= len(LEVELS) - 1:
        return xp, xp, 100.0
    current_threshold = LEVELS[idx]["xp"]
    next_threshold = LEVELS[idx + 1]["xp"]
    in_level = xp - current_threshold
    needed = next_threshold - current_threshold
    pct = min(100.0, (in_level / needed) * 100) if needed > 0 else 100.0
    return in_level, needed, pct


def check_achievements(state):
    """Check and return newly unlocked achievements."""
    unlocked = state.get("achievements_unlocked", [])
    new_unlocks = []
    q_count = state.get("total_questions", 0)
    docs = state.get("total_docs", 0)
    streak = state.get("streak", 0)
    xp = state.get("xp", 0)

    checks = [
        ("first_q",  q_count >= 1),
        ("doc_load", docs >= 1),
        ("five_q",   q_count >= 5),
        ("ten_q",    q_count >= 10),
        ("master",   get_level_index(xp) >= 4),
        ("streak_5", streak >= 5),
    ]

    for ach_id, condition in checks:
        if condition and ach_id not in unlocked:
            unlocked.append(ach_id)
            new_unlocks.append(ach_id)

    state["achievements_unlocked"] = unlocked
    return new_unlocks


def get_quests(state):
    """Return list of active quests with progress."""
    q_count = state.get("total_questions", 0)
    docs = state.get("total_docs", 0)
    streak = state.get("streak", 0)

    quests = []
    # Quest 1: Ask 3 questions
    q1_prog = min(q_count, 3)
    quests.append({
        "key": "quest_ask_3",
        "progress": q1_prog,
        "target": 3,
        "done": q1_prog >= 3,
        "icon": "❓",
    })
    # Quest 2: Load a document
    quests.append({
        "key": "quest_load_doc",
        "progress": min(docs, 1),
        "target": 1,
        "done": docs >= 1,
        "icon": "📄",
    })
    # Quest 3: 3x streak
    q3_prog = min(streak, 3)
    quests.append({
        "key": "quest_streak_3",
        "progress": q3_prog,
        "target": 3,
        "done": q3_prog >= 3,
        "icon": "🔥",
    })
    return quests


def award_xp(state, amount):
    """Add XP and return (new_xp, leveled_up)."""
    old_level = get_level_index(state.get("xp", 0))
    streak = state.get("streak", 0)
    bonus = streak * XP_STREAK_BONUS
    state["xp"] = state.get("xp", 0) + amount + bonus
    new_level = get_level_index(state["xp"])
    return state["xp"], new_level > old_level
