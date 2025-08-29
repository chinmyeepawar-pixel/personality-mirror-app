import streamlit as st
import numpy as np
import random
from textwrap import fill
import json
import os

def save_user_profile(user_id, data):
    filename = "user_profiles.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_profiles = json.load(f)
    else:
        all_profiles = {}

    all_profiles[user_id] = data

    with open(filename, "w") as f:
        json.dump(all_profiles, f, indent=4)

def load_user_profile(user_id):
    filename = "user_profiles.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_profiles = json.load(f)
        return all_profiles.get(user_id, None)
    return None


# ---------- Page Config ----------
st.set_page_config(page_title="Personality Mirror 🪞 • Mythic Archetypes + Shadow Horror",
                   page_icon="🪞", layout="wide")


import streamlit as st
import base64

# Load mist GIF and encode to base64
with open("mist_animation.gif", "rb") as image_file:
    mist_bytes = image_file.read()
mist_base64 = base64.b64encode(mist_bytes).decode()

st.markdown(f"""
    <style>
    /* Background for the main content */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/gif;base64,{mist_base64}") no-repeat center center fixed !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    /* Remove solid backgrounds from main and blocks */
    [data-testid="stAppViewContainer"], .main, [data-testid="stSidebar"], .css-1dp5vir {{
        background-color: rgba(0,0,0,0) !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    #mist-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        background: rgba(0, 0, 0, 0.85);   /* 0.85 = 85% dark overlay, adjust to taste */
    }
    </style>
    <div id="mist-overlay"></div>
    """, unsafe_allow_html=True
)


# Add audio player for local music file

st.sidebar.markdown("#### 🎵 Ambient Music")
st.sidebar.audio("background_music.mp3.mp3", format="audio/mp3")



# --- Combined Styling for Dark Mythical Theme and UI polish ---
st.markdown("""
    <style>
    /* Background Gradient */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #3a0ca3 50%, #0f3460 100%);
        color: #e0e0ff;
        min-height: 100vh;
        padding: 1rem;
    }
    /* Headings with emoji style */
    h1, h2, h3, h4 {
        font-family: 'Georgia', serif;
        color: #b68eff;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    /* Radio question labels larger and spaced */
    .stRadio > label,
    .stRadio label {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    .stRadio {
        margin-bottom: 1.2em !important;
    }
    /* Styled Horror Story Box */
    .story-box {
        background: rgba(58, 12, 163, 0.15);
        border-left: 5px solid #b68eff;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        font-style: italic;
        margin-bottom: 1rem;
        color: #e0e0ff;
    }
    /* Button hover glow */
    button:hover {
        box-shadow: 0 0 8px 1px #b68eff;
        transition: box-shadow 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)




# Display styled horror story text somewhere in your story tab:
# st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)


# ---------- Helper Data ----------
LIKERT = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

# 20 questions (4 per trait) – some reversed
QUESTIONS = [
    # Openness (O)
    {"text": "I enjoy exploring new ideas, art, or philosophy.", "trait": "O", "reverse": False},
    {"text": "I prefer routine over trying new things.", "trait": "O", "reverse": True},
    {"text": "I consider myself imaginative and curious.", "trait": "O", "reverse": False},
    {"text": "I avoid unusual topics or abstract thinking.", "trait": "O", "reverse": True},

    # Conscientiousness (C)
    {"text": "I plan ahead and keep to-do lists.", "trait": "C", "reverse": False},
    {"text": "My workspace is often messy and I misplace things.", "trait": "C", "reverse": True},
    {"text": "I finish tasks long before the deadline.", "trait": "C", "reverse": False},
    {"text": "I tend to procrastinate until the last moment.", "trait": "C", "reverse": True},

    # Extraversion (E)
    {"text": "Group activities energize me.", "trait": "E", "reverse": False},
    {"text": "I prefer quiet nights alone to social events.", "trait": "E", "reverse": True},
    {"text": "I start conversations easily with strangers.", "trait": "E", "reverse": False},
    {"text": "I rarely speak up in groups.", "trait": "E", "reverse": True},

    # Agreeableness (A)
    {"text": "I’m empathetic and try to see others’ viewpoints.", "trait": "A", "reverse": False},
    {"text": "I argue to win, even if it upsets people.", "trait": "A", "reverse": True},
    {"text": "Helping others comes naturally to me.", "trait": "A", "reverse": False},
    {"text": "I find it hard to trust people’s intentions.", "trait": "A", "reverse": True},

    # Neuroticism (N)
    {"text": "I worry often about mistakes or the future.", "trait": "N", "reverse": False},
    {"text": "I bounce back quickly after setbacks.", "trait": "N", "reverse": True},
    {"text": "Criticism affects me more than it should.", "trait": "N", "reverse": False},
    {"text": "Stress doesn’t linger; I move on easily.", "trait": "N", "reverse": True},
]

# --- Mythic archetypes & taglines ---
# (Kept logical mapping to traits, but with a gentle mythic vibe.)
ARCHETYPE_TAGLINES = {
    "Bannerbearer": "Where hearts gather, momentum follows.",
    "Wayfinder": "Curiosity draws the map as you walk.",
    "Runesmith": "Imagination, hammered into craft.",
    "Hearthwarden": "Order kept warm for company.",
    "Iron Architect": "Calm hands. Exact lines. Quiet triumph.",
    "Seer of Depths": "Listening where daylight does not reach.",
    "Grovekeeper": "Quiet roots, sheltering boughs.",
    "Sentinel": "Steady watch in shifting times.",
    "Nightblade": "Solitude sharpens the edge.",
    "Aether Weaver": "Between opposites, you braid balance."
}

def likert_to_score(idx: int, reverse: bool) -> int:
    raw = idx + 1  # 1..5
    return (6 - raw) if reverse else raw

def score_traits(responses):
    sums = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    counts = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    for ans, q in zip(responses, QUESTIONS):
        score = likert_to_score(ans, q["reverse"])
        sums[q["trait"]] += score
        counts[q["trait"]] += 1
    scaled = {}
    for t in sums:
        min_raw, max_raw = 4, 20
        scaled[t] = round((sums[t] - min_raw) / (max_raw - min_raw) * 100, 1)
    return scaled

def archetype_from_traits(T):
    high = lambda x: T[x] >= 60
    low  = lambda x: T[x] <= 40
    # Priority rules → mythic names
    if high("E") and high("A"): return "Bannerbearer"      # (Champion)
    if high("O") and high("E"): return "Wayfinder"         # (Explorer)
    if high("O") and high("C"): return "Runesmith"         # (Strategist)
    if high("C") and high("A"): return "Hearthwarden"      # (Guardian)
    if high("C") and low("N"):  return "Iron Architect"    # (Architect)
    if high("O") and high("N"): return "Seer of Depths"    # (Seeker)
    if low("E") and high("A"):  return "Grovekeeper"       # (Mediator)
    if low("O") and high("C") and T["N"] <= 60: return "Sentinel"
    if low("E") and low("A") and high("N"): return "Nightblade"
    return "Aether Weaver"                                 # (Balanced Synthesizer)

def trait_badges(T):
    parts = []
    for k,label in zip(["O","C","E","A","N"], ["Openness","Conscientiousness","Extraversion","Agreeableness","Neuroticism"]):
        parts.append(f"**{label}**: {T[k]}")
    return " · ".join(parts)

def recs_from_traits(T, archetype):
    books = set()
    movies = set()
    study, organize, meditations, general = [], [], [], []

    # Books
    if T["C"] >= 60: books.update(["Deep Work — Cal Newport", "Atomic Habits — James Clear", "Essentialism — Greg McKeown"])
    else: books.update(["The Now Habit — Neil Fiore", "The War of Art — Steven Pressfield"])
    if T["O"] >= 60: books.update(["The Alchemist — Paulo Coelho", "Range — David Epstein"])
    else: books.update(["Make It Stick — Brown, Roediger, McDaniel"])
    if T["E"] <= 40: books.add("Quiet — Susan Cain")
    if T["N"] >= 60: books.update(["Mindset — Carol Dweck", "Daring Greatly — Brené Brown", "Man’s Search for Meaning — Viktor Frankl"])

    # Movies (PG-13ish, motivational/reflective)
    if T["O"] >= 60: movies.update(["Interstellar", "The Martian", "Dead Poets Society"])
    if T["C"] >= 60: movies.update(["Hidden Figures", "The Social Network"])
    if T["E"] <= 40: movies.update(["The Imitation Game"])
    if T["N"] >= 60: movies.update(["Inside Out", "Good Will Hunting"])

    # Study strategies
    if T["C"] >= 60:
        study += ["Timebox tasks on a calendar (30–60 min blocks).",
                  "Weekly review: plan → execute → reflect."]
    else:
        study += ["Pomodoro (25/5) with a 2-minute starter task.",
                  "Study trigger: same desk, same playlist, same hour."]

    if T["O"] >= 60:
        study += ["Use concept maps + ‘teach-back’.",
                  "Interleave topics to feed curiosity."]
    else:
        study += ["Follow a structured outline; start with end-of-chapter problems.",
                  "Worked-example → attempt → self-explain cycle."]

    if T["E"] >= 60:
        study += ["Short group sessions; explain problems aloud.",
                  "Use a whiteboard for live problem solving."]
    else:
        study += ["Protect quiet deep-work windows (phone in another room).",
                  "Batch communication after study blocks."]

    if T["N"] >= 60:
        study += ["Begin with one easy win to lower anxiety.",
                  "After each session, jot one line: ‘What went well?’"]

    # Organization tips
    if T["C"] >= 60:
        organize += ["Single trusted system (Notion/Obsidian/Google Tasks).",
                     "Theme weekdays (e.g., DSA Mon, ML Wed)."]
    else:
        organize += ["Visual kanban (To-Do/Doing/Done) with WIP limit = 2.",
                     "Lay out tomorrow’s first task today."]

    if T["O"] <= 40:
        organize += ["Use consistent templates for notes & labs."]

    # Meditations
    meditations += ["Box Breathing (4-4-4-4, 3–5 mins)"]
    if T["N"] >= 60: meditations += ["Body Scan (8–10 mins)",
                                     "Cognitive defusion: label thoughts (‘I’m having the thought that…’)"]
    if T["A"] >= 60: meditations += ["Loving-Kindness (send warmth to self & others)"]

    # General tips
    if T["E"] >= 60: general += ["Schedule ‘no plans’ recovery time."]
    if T["A"] >= 60: general += ["Practice a ‘kind no’ to protect study time."]
    if T["C"] >= 60: general += ["Define ‘good enough’ to avoid perfectionism."]
    if T["O"] >= 60: general += ["Keep an Idea Inbox; review weekly."]
    if T["N"] >= 60: general += ["Limit caffeine after 2 PM; 10–15 min walk before study."]

    tagline = ARCHETYPE_TAGLINES.get(archetype, "Between opposites, you braid balance.")
    return {
        "books": sorted(books),
        "movies": sorted(movies),
        "study": study,
        "organize": organize,
        "meditations": meditations,
        "general_tips": general,
        "tagline": tagline
    }


def shadow_from_traits(T):
    fears, shadows, sugg = [], [], []

    if T["N"] >= 60:
        fears += ["fear of failure", "fear of rejection"]
        shadows += ["catastrophizing", "rumination"]
        sugg += ["Keep a 3-column thought record (Situation → Thought → Alternative).",
                 "4-7-8 breathing; then one tiny action in 2 minutes."]

    if T["C"] <= 40:
        fears += ["fear of commitment", "timelines slipping"]
        shadows += ["procrastination", "chaotic routines"]
        sugg += ["Design your environment (prep desk, remove distractions).",
                 "Daily top-1 task before messages."]

    if T["A"] <= 40:
        fears += ["fear of dependency", "vulnerability in relationships"]
        shadows += ["defensiveness", "abrasive communication"]
        sugg += ["Nonviolent Communication (Obs → Feel → Need → Request).",
                 "Write before you speak when upset; then shorten."]

    if T["E"] <= 40:
        fears += ["social scrutiny", "being misunderstood"]
        shadows += ["avoidance of groups", "missing helpful feedback"]
        sugg += ["Micro-goals: 1 question per class / 5-min group join.",
                 "Record yourself explaining a concept; iterate."]

    if T["O"] <= 40:
        fears += ["change", "ambiguity"]
        shadows += ["rigidity", "over-reliance on templates"]
        sugg += ["One ‘new thing’ a week (tiny novelty reps).",
                 "Study one topic’s ‘why’, not just ‘how’."]

    if T["O"] >= 60:
        shadows += ["idea hopping", "boredom with maintenance"]
        sugg += ["Zettelkasten/atomic notes; schedule maintenance blocks."]

    if T["C"] >= 60:
        shadows += ["perfectionism", "over-control"]
        sugg += ["Define done-criteria; cap quality at 90% for speed."]

    if T["A"] >= 60:
        shadows += ["over-giving", "people-pleasing"]
        sugg += ["Boundary script: ‘I can help after 5 PM, not before.’"]

    if T["E"] >= 60:
        shadows += ["FOMO", "over-committing"]
        sugg += ["Plan with buffers; a weekly solo reset block."]

    def uniq(seq):
        out, seen = [], set()
        for x in seq:
            if x not in seen:
                out.append(x); seen.add(x)
        return out

    return {
        "fears": uniq(fears) or ["ordinary fears and doubts"],
        "shadows": uniq(shadows) or ["balanced tendencies"],
        "suggestions": uniq(sugg) or ["Keep doing what works; iterate weekly."]
    }

def pick_setting(archetype):
    mapping = {
        "Wayfinder": "a moonlit ruin with stairways that end in stars",
        "Runesmith": "a forge where anvils ring without hammers",
        "Hearthwarden": "a long hall of lanterns that never quite go out",
        "Bannerbearer": "an empty coliseum whose banners breathe",
        "Seer of Depths": "a black-water lake with a patient pier",
        "Iron Architect": "a crystal tower of silent gears",
        "Grovekeeper": "a forest cloister humming like bees in winter",
        "Sentinel": "a dust-heavy archive that remembers footsteps",
        "Nightblade": "a narrow path between sleeping stones",
        "Aether Weaver": "a corridor of doors that argue softly"
    }
    return mapping.get(archetype, "a dimly lit archive")



def horror_story(name, archetype, fears, T, length_paras=8, pg13=True, seed=None):
    random.seed(seed)
    setting = pick_setting(archetype)
    you = (name or "You")
    senses = [
        "A faint hum threads the air, steady as a held breath.",
        "Dust swirls in your torchlight like slow snow.",
        "Somewhere a hinge creaks, then decides to keep quiet.",
        "Your footsteps echo, overlapping like someone walking just behind.",
        "Cold gathers around your wrists as if measuring your pulse."
    ]
    motifs = {
        "fear of failure": ["red ink stains", "half-graded papers", "a metronome that never beats exactly on time"],
        "fear of rejection": ["locked doors with your name scratched off", "phones that ring once and die"],
        "social scrutiny": ["rows of empty chairs facing you", "a camera’s red light that never turns off"],
        "change": ["hallways that shuffle when you look away", "maps that redraw themselves"],
        "ambiguity": ["signs with two arrows pointing opposite ways"],
        "timelines slipping": ["clocks that skip numbers", "calendars with bleeding weeks"],
    }
    pool = []
    for f in fears:
        pool += motifs.get(f, [])
    if not pool:
        pool = ["a corridor that narrows behind you", "a door that returns to where you started"]

    para = []
    para.append(f"{you} step into {setting}. The lights don’t fail; they merely refuse certainty.")
    para.append(random.choice(senses))

    tension = [
        f"You test a door. It opens, but to a copy of this hallway—only the shadows are facing the wrong way.",
        f"A whisper rides the ventilation: not words, just the shape of someone deciding them.",
        f"You find {random.choice(pool)}. It looks like evidence left for you to interpret, or ignore."
    ]
    if T["C"] >= 60:
        tension.append("You scribe marks on the wall. When you look back, they have moved two inches to the left.")
    else:
        tension.append("You promise to mark your path, but the thought slides off like chalk on wet slate.")
    if T["E"] <= 40:
        tension.append("Silence presses close, friendly at first, then expectant, like a question you owe an answer.")
    else:
        tension.append("Your hello returns from the dark—cheerful, a little too familiar.")
    if T["N"] >= 60:
        tension.append("Your heartbeat counts steps. The corridor counts faster.")
    else:
        tension.append("A calm pocket opens inside your chest, stubborn as a lighthouse.")

    para += random.sample(tension, k=min(3, len(tension)))

    para.append(f"On a metal table sits a folder with your initials. Inside: {random.choice(pool)}, and a photo of {you.lower()} standing exactly here, only the timestamp is five minutes from now.")
    para.append("You wait without meaning to. The photo does not change. Time does.")

    main_fear = fears[0] if fears else "something unnamed"
    lines = {
        "fear of failure": f"A door opens to a hall of ledgers. Each line is almost right; each total disagrees by one.",
        "fear of rejection": f"You dial a phone that shouldn’t have service. It rings once; behind you, a door locks.",
        "social scrutiny": f"Spotlights blink on, gentle as snowfall, and you realize there are no seats—just a stage.",
        "change": f"You draw a map as you walk. The lines slither, pleased to be alive.",
        "ambiguity": f"Two staircases descend. Both hum the same note. Both promise to be the wrong one.",
        "timelines slipping": f"Clocks bud on the walls like fruit. They ripen into alarms you don’t remember setting."
    }
    para.append(lines.get(main_fear, "A new corridor grows where a wall used to be, shy but insistent."))

    growth = []
    if T["C"] >= 60:
        growth.append("You set a simple rule: one step, then the next, no auditions.")
    else:
        growth.append("You pick the smallest door and promise nothing except to turn the handle.")
    if T["O"] >= 60:
        growth.append("Curiosity outruns dread; you list questions, then answer one.")
    else:
        growth.append("You choose the corridor that stays still when you blink.")
    if T["A"] >= 60:
        growth.append("You speak softly into the dark: ‘Come with me, if you like.’ The echo sounds relieved.")
    else:
        growth.append("You speak clearly: ‘Not tonight.’ The echo respects the boundary.")
    if T["N"] >= 60:
        growth.append("Fear arrives again, punctual. You nod, and walk anyway.")
    else:
        growth.append("Calm expands, a warm coat in borrowed weather.")

    para += growth
    para.append(f"At last, a door marked ‘Exit’ opens to a corridor brighter than you remember. The chalk mark is exactly where you left it.")
    end_line = f"{you} step through. The handle is warm. Behind you, {setting} inhales—and lets you go."
    if not pg13:
        end_line += " (You asked for uncensored; the shadows disagree.)"
    para.append(end_line)

    story = "\n\n".join(fill(p, width=90) for p in para[:max(4, length_paras)])
    return story

def radar_chart(fig_ax, T):
    import matplotlib.pyplot as plt
    labels = ["Openness","Conscientiousness","Extraversion","Agreeableness","Neuroticism"]
    values = [T["O"], T["C"], T["E"], T["A"], T["N"]]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    ax = fig_ax
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_rlabel_position(0)
    ax.set_yticks([20,40,60,80])
    ax.set_yticklabels(["20","40","60","80"])
    ax.set_ylim(0,100)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)

# ---------- UI State ----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "scores" not in st.session_state:
    st.session_state.scores = None
if "archetype" not in st.session_state:
    st.session_state.archetype = None
if "recs" not in st.session_state:
    st.session_state.recs = None
if "shadow" not in st.session_state:
    st.session_state.shadow = None

# ---------- Layout ----------
st.title("🪞 Mythic Personality Mirror: Archetype + Shadow Horror")

with st.sidebar:
    st.header("About")
    st.write("Non-clinical, educational tool for your mini-project. Uses a short Big-Five style questionnaire to generate a mythic archetype, study tips, and a personalized PG-13 horror story.")
    user_name = st.text_input("Your name (optional, for story):", "")
    story_len = st.slider("Story length (paragraphs):", 6, 14, 8)
    st.caption("Disclaimer: Educational only — not a clinical diagnostic.")

tabs = st.tabs([
    "Take Test",
    "Results & Guidance",
    "Horror Story",
    "Dashboard",              # <-- Dashboard after Horror Story
    "Challenges & Quests",
    "Mood & Habit Tracker",
    "Content Recommendations",
    "Mindfulness",
    "Worksheets & Journals"
])
# ---------- Tab 1: Test ----------
with tabs[0]:
    # User ID input for saving/loading profiles
    user_id = st.text_input("Enter your username or email to save/load your profile", key="user_id")

    # Load saved profile if available
    if user_id:
        loaded_profile = load_user_profile(user_id)
        if loaded_profile:
            st.session_state["scores"] = loaded_profile.get("scores", {})
            st.session_state["archetype"] = loaded_profile.get("archetype", None)
            st.session_state["recs"] = loaded_profile.get("recs", {})
            st.session_state["shadow"] = loaded_profile.get("shadow", {})
            st.success(f"Loaded profile data for {user_id}.")
    
    # --- Your existing test UI code starts here ---
    st.markdown("""
    <div style="background:rgba(35,28,56,0.97); border-radius:14px; padding:32px 28px 20px 28px; margin-bottom:18px; box-shadow:0 6px 20px #20163355;">
        <h2 style='color:#b68eff; margin-bottom:0.5em;'>Take the Personality Test</h2>
        <h4 style='color:#e0c3fc; margin-top:0; font-weight:400;'>Answer honestly (first thought is usually best)</h4>
    """, unsafe_allow_html=True)

    # ... rest of your tab 0 code ...

    st.markdown("""
    <div style="background:rgba(35,28,56,0.97); border-radius:14px; padding:32px 28px 20px 28px; margin-bottom:18px; box-shadow:0 6px 20px #20163355;">
        <h2 style='color:#b68eff; margin-bottom:0.5em;'>Take the Personality Test</h2>
        <h4 style='color:#e0c3fc; margin-top:0; font-weight:400;'>Answer honestly (first thought is usually best)</h4>
    """, unsafe_allow_html=True)
    
    with st.expander("Tips for Taking the Test"):
        st.write("• Go with your first instinct.\n• Be honest with yourself.\n• No right or wrong answers.")

    st.markdown("<hr style='border-top:1px solid #342a5c;'>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)
    responses = []
    for i, q in enumerate(QUESTIONS):
        col = left_col if i % 2 == 0 else right_col
        with col:
            idx = st.radio(
                f"{i+1}. {q['text']}",
                options=list(range(5)),
                format_func=lambda x: LIKERT[x],
                index=2,  # Neutral preselected
                key=f"q{i}",
            )
            responses.append(idx)

    st.markdown("<hr style='border-top:1px solid #342a5c;'>", unsafe_allow_html=True)

    compute_btn = st.button("🪞 Compute My Personality Profile")
    st.markdown("</div>", unsafe_allow_html=True)

    if compute_btn:
        with st.spinner("Calculating your profile... 🧠"):
            T = score_traits(responses)
            arch = archetype_from_traits(T)
            rec = recs_from_traits(T, arch)
            sh = shadow_from_traits(T)
            st.session_state.submitted = True
            st.session_state.scores = T
            st.session_state.archetype = arch
            st.session_state.recs = rec
            st.session_state.shadow = sh
        st.success(f"Profile generated! Your archetype: {arch} 🛡️")


# ---------- Tab 2: Results ----------
with tabs[1]:
    if not st.session_state.submitted:
        st.info("Please complete the test in the first tab.")
    else:
        # Load user data from session state (must be set in the test tab)
        T = st.session_state.scores
        arch = st.session_state.archetype
        rec = st.session_state.recs
        sh = st.session_state.shadow

        # Layout: Columns for results
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.5,1])

        with col1:
            st.markdown(f"""
            <div style="background:rgba(35,28,56,0.97); border-radius:14px; padding:28px; margin-bottom:18px; box-shadow:0 6px 20px #20163355;">
                <h2 style='color:#b68eff;'>Archetype: {arch}</h2>
                <em>{rec['tagline']}</em><br>
                <b>Openness:</b> {T['O']} &nbsp; <b>Conscientiousness:</b> {T['C']} &nbsp; <b>Extraversion:</b> {T['E']} &nbsp; <b>Agreeableness:</b> {T['A']} &nbsp; <b>Neuroticism:</b> {T['N']}
                <hr style="border: none; border-top: 1px solid #342a5c;">
                <h3 style='color:#e0c3fc;'>What Do These Traits Mean?</h3>
                <ul style='color:#e1dee8; font-size:1.09rem;'>
                  <li><b>Openness (Curiosity):</b> Willingness to try new things and explore new experiences.</li>
                  <li><b>Conscientiousness (Responsibility):</b> How organized, careful, and reliable a person is.</li>
                  <li><b>Extraversion (Sociability):</b> Tendency to enjoy socializing and spending time with people.</li>
                  <li><b>Agreeableness (Kindness):</b> How friendly, cooperative, and compassionate one is.</li>
                  <li><b>Neuroticism (Emotional Sensitivity):</b> Sensitivity to stress, how often someone feels worried or moody.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(111, polar=True)
            radar_chart(ax, T)
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.markdown(f"""
            <div style="background:rgba(35,28,56,0.97); border-radius:14px; padding:28px; margin-bottom:18px; box-shadow:0 6px 20px #20163355;">
                <h2 style='color:#e0c3fc;'>Recommendations</h2>
                <h3>Study Strategies</h3>
            """, unsafe_allow_html=True)

            for s in rec["study"]:
                st.write("• " + s)

            st.markdown("<h3>Organization Tips</h3>", unsafe_allow_html=True)
            for s in rec["organize"]:
                st.write("• " + s)

            st.markdown("<h3>Meditations</h3>", unsafe_allow_html=True)
            for s in rec["meditations"]:
                st.write("• " + s)

            st.markdown("<h3>General Tips</h3>", unsafe_allow_html=True)
            for s in rec["general_tips"]:
                st.write("• " + s)

            st.markdown("<h3>Books to Explore</h3>", unsafe_allow_html=True)
            st.write(", ".join(rec["books"]))

            st.markdown("<h3>Movies to Watch</h3>", unsafe_allow_html=True)
            st.write(", ".join(rec["movies"]))

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background:rgba(35,28,56,0.89); border-radius:14px; padding:18px; margin-bottom:18px; box-shadow:0 3px 10px #20163344;">
                <h3 style='color:#ff71f2;'>Shadow Self (Blind Spots) & Gentle Support</h3>
                <b>Likely Fears:</b> {', '.join(sh['fears'])}<br>
                <b>Shadow Patterns:</b> {', '.join(sh['shadows'])}<br>
                <b>Suggestions:</b>
            </div>
        """, unsafe_allow_html=True)

        for s in sh["suggestions"]:
            st.write("• " + s)

        import urllib.parse

        # Social Sharing
        import urllib.parse

        app_url = "https://personalitymirror.streamlit.app"  # Replace with your real app URL

        share_text = (
        f"My Mythic Personality Mirror archetype is {arch} – {rec['tagline']}. Discover yours! {app_url}"
        )

        whatsapp_url = "https://api.whatsapp.com/send?text=" + urllib.parse.quote(share_text)

        st.markdown(f"""
        ### Share Your Results
        [📱 Share on WhatsApp]({whatsapp_url})
        """, unsafe_allow_html=True)

        st.text_input("🔗 Copyable share text:", value=share_text, help="Copy and share this manually!", key="sharetext")

         # Save profile button
        if user_id:
            if st.button("Save My Profile"):
                profile_data = {
                    "scores": T,
                    "archetype": arch,
                    "recs": rec,
                    "shadow": sh,
                }
                save_user_profile(user_id, profile_data)
                st.success(f"Profile saved for {user_id}!")

        # Downloadable report
        report = []
        report.append(f"Name: {st.session_state.get('user_name', 'Anonymous')}")
        report.append(f"Archetype: {arch}")
        report.append(f"Tagline: {rec['tagline']}")
        report.append("Traits (0-100): " + ", ".join([f"{k}={T[k]}" for k in ["O","C","E","A","N"]]))
        report.append("\nStudy Strategies:\n- " + "\n- ".join(rec["study"]))
        report.append("\nOrganization Tips:\n- " + "\n- ".join(rec["organize"]))
        report.append("\nMeditations:\n- " + "\n- ".join(rec["meditations"]))
        report.append("\nGeneral Tips:\n- " + "\n- ".join(rec["general_tips"]))
        report.append("\nBooks:\n- " + "\n- ".join(rec["books"]))
        report.append("\nMovies:\n- " + "\n- ".join(rec["movies"]))
        report.append("\nShadow Fears:\n- " + "\n- ".join(sh["fears"]))
        report.append("\nShadow Patterns:\n- " + "\n- ".join(sh["shadows"]))
        report.append("\nShadow Suggestions:\n- " + "\n- ".join(sh["suggestions"]))
        report_txt = "\n".join(report)
        st.download_button("Download My Guidance (.txt)", data=report_txt, file_name="personality_guidance.txt")



# ---------- Tab 3: Horror Story ----------
import time
import random
import streamlit as st

with tabs[2]:
    if not st.session_state.submitted:
        st.info("Please complete the test in the first tab.")
    else:
        # Play ambient music on user click
        if st.button("▶️ Play Ambient Horror Music"):
            st.audio(
                "horror-background.mp3.mp3",
                format="audio/mp3",
                start_time=0
            )

        T = st.session_state.scores
        arch = st.session_state.archetype
        sh = st.session_state.shadow
        fears = sh["fears"]

        story_text = horror_story(st.session_state.get("user_name", "You"), arch, fears, T, length_paras=8, pg13=True, seed=random.randint(0, 1_000_000))

        st.markdown("### Your Personalized Horror (PG-13, mythic tone)")

        # Animated paragraph reveal
        paragraphs = story_text.split("\n\n")
        placeholder = st.empty()
        for para in paragraphs:
            placeholder.markdown(para)
            time.sleep(2)  # pause 2 seconds before next paragraph
            placeholder.empty()
        # Show the full story at the end for scrolling
        st.write(story_text)

        st.markdown("---")

        # Interactive reader choices
        choice1 = st.radio("You see two doors ahead. Do you take the left or the right?", ["Left Door", "Right Door"])

        if choice1 == "Left Door":
            st.write("You enter a dimly lit corridor, the walls whispering secrets.")
            st.write("A chilling breeze passes and you feel unseen eyes watching.")
        else:
            st.write("The right door creaks open to reveal a shifting maze of mirrors.")
            st.write("Reflections twist and distort, questioning your reality.")

        choice2 = st.radio("You find a mysterious key. Do you keep it or leave it?", ["Keep the key", "Leave it"])

        if choice2 == "Keep the key":
            st.write("The key glows faintly, unlocking memories you long forgot.")
        else:
            st.write("You leave the key behind. The shadows seem to sigh in relief.")

        st.markdown("---")
        st.write("The story continues in the folds of your imagination...")

        st.download_button("Download Story (.txt)", data=story_text, file_name="shadow_story.txt")



with tabs[3]:
    st.title("Dashboard: Personality & Mood Insights")

    if not st.session_state.submitted:
        st.info("Complete the quiz first to unlock dashboard analytics.")
    else:
        T = st.session_state.scores

        st.subheader("Big Five Trait Scores")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Openness", f"{T['O']}%")
            st.progress(int(T['O']))
            st.metric("Conscientiousness", f"{T['C']}%")
            st.progress(int(T['C']))
        with col2:
            st.metric("Extraversion", f"{T['E']}%")
            st.progress(int(T['E']))
            st.metric("Agreeableness", f"{T['A']}%")
            st.progress(int(T['A']))
        with col3:
            st.metric("Neuroticism", f"{T['N']}%")
            st.progress(int(T['N']))

        st.divider()

        st.subheader("Mood Tracking Overview")

        # Example: sample mood history data (replace with real user data)
        sample_mood_data = {
            "Happy": 5,
            "Neutral": 3,
            "Sad": 2
        }

        st.bar_chart(sample_mood_data)
        st.info("Mood tracking data updates as you log daily mood in the Mood & Habit Tracker tab.")



            # ----- Challenges & Quests -----
with tabs[4]:
    st.header("Custom Challenges & Quests")
    st.write("Based on your archetype, here are daily/weekly challenges:")

    arch = st.session_state.get("archetype", None)

    challenges_map = {
        "Bannerbearer": [
            "Organize a group study session or help a friend with homework.",
            "Lead a small group activity this week."
        ],
        "Wayfinder": [
            "Explore a new subject outside your curriculum.",
            "Try a creative brainstorming session and record 5 ideas."
        ],
        "Runesmith": [
            "Work on a detailed plan for your next project.",
            "Review and improve your study notes."
        ],
        "Hearthwarden": [
            "Create a comfortable study space.",
            "Schedule regular breaks and stick to them."
        ],
        "Iron Architect": [
            "Set and follow a new routine for one week.",
            "Complete an assignment ahead of deadline."
        ],
        "Nightblade": [
            "Practice solo meditation for 3 days.",
            "Journal your thoughts daily."
        ],
        # Add other archetypes as needed
        "default": [
            "Complete all your habits for 5 consecutive days.",
            "List three things you learned about yourself this week."
        ]
    }

    chosen_challenges = challenges_map.get(arch, challenges_map["default"])

    # Show checkboxes for challenges
    completed = 0
    for i, challenge in enumerate(chosen_challenges):
        key = f"challenge_{i}"
        completed_challenge = st.checkbox(challenge, key=key)
        if completed_challenge:
            completed += 1

    st.success(f"You have completed {completed} out of {len(chosen_challenges)} challenges!")

    # Motivational message
    st.markdown("🚩 Keep going! Every small victory counts!")


# ----- Mood & Habit Tracker -----

from datetime import datetime, timedelta
import pandas as pd

with tabs[5]:
    st.header("Mood & Habit Tracker")

    if 'mood_history' not in st.session_state:
        st.session_state.mood_history = []

    col1, col2 = st.columns(2)
    with col1:
        mood = st.selectbox("Today's mood", ["😊 Happy", "😐 Neutral", "😞 Sad"])
    with col2:
        habit_done = st.checkbox("Completed your target habit today?")

    if st.button("Log Mood & Habit"):
        today_str = datetime.now().strftime("%Y-%m-%d")
        st.session_state.mood_history.append({
            "date": today_str,
            "mood": mood,
            "habit": habit_done
        })
        st.success("Logged your mood and habit for today!")

    if st.session_state.mood_history:
        df = pd.DataFrame(st.session_state.mood_history)

        st.subheader("Mood & Habit Log")
        st.write(df)

        st.subheader("Mood Overview")
        mood_counts = df['mood'].value_counts()
        st.bar_chart(mood_counts)

        # Weekly habit summary
        one_week_ago = datetime.now() - timedelta(days=7)
        df['date_dt'] = pd.to_datetime(df['date'])
        recent = df[df['date_dt'] >= one_week_ago]
        completed_count = recent['habit'].sum()
        st.info(f"You've completed your habit **{completed_count}** out of the last 7 days. Keep it up!")

    



# ----- Content Recommendations -----
with tabs[6]:
    st.header("Content Recommendations")
    st.write("Personalized books, podcasts, videos, and music for you.")

    arch = st.session_state.get("archetype", "default")
    T = st.session_state.get("scores", None)

    # Example recommendations by archetype
    recommendations = {
        "Bannerbearer": {
            "Books": ["Leaders Eat Last — Simon Sinek", "Drive — Daniel Pink"],
            "Podcasts": ["The Tony Robbins Podcast"],
            "Videos": ["TED Talk: 'Why Good Leaders Make You Feel Safe'"],
            "Music": ["Eye of the Tiger — Survivor"]
        },
        "Wayfinder": {
            "Books": ["The Alchemist — Paulo Coelho", "Range — David Epstein"],
            "Podcasts": ["Freakonomics Radio"],
            "Videos": ["TED Talk: 'The Power of Curiosity'"],
            "Music": ["Adventure of a Lifetime — Coldplay"]
        },
        "Iron Architect": {
            "Books": ["Atomic Habits — James Clear"],
            "Podcasts": ["Deep Work by Cal Newport (Audiobook Excerpts)"],
            "Videos": ["TED Talk: 'The Art of Being Yourself'"],
            "Music": ["Hall of Fame — The Script"]
        },
        "default": {
            "Books": ["Mindset — Carol Dweck"],
            "Podcasts": ["The Happiness Lab"],
            "Videos": ["MotivationHub Compilation"],
            "Music": ["On Top of the World — Imagine Dragons"]
        }
    }

    rec = recommendations.get(arch, recommendations["default"])

    # Display recommendations by type
    st.subheader("🎧 Podcasts")
    for p in rec["Podcasts"]:
        st.markdown(f"- {p}")

    st.subheader("📚 Books")
    for b in rec["Books"]:
        st.markdown(f"- {b}")

    st.subheader("▶️ Videos")
    for v in rec["Videos"]:
        st.markdown(f"- {v}")

    st.subheader("🎵 Music")
    for m in rec["Music"]:
        st.markdown(f"- {m}")

    st.divider()
    st.info("Explore new content matched to your personality archetype!")

    


# ----- Mindfulness -----
with tabs[7]:
    st.header("Guided Meditations & Mindfulness")
    st.write("Try these meditation/audiovisual guides to boost your focus and calm.")

    # Select from multiple mindfulness exercises
    exercise = st.selectbox(
        "Choose a mindfulness exercise:",
        ["Box Breathing (4-4-4-4)", "Body Scan Meditation", "Loving-Kindness", "Mindful Music"]
    )

    # Provide instructions or embed media based on selection
    if exercise == "Box Breathing (4-4-4-4)":
        st.markdown("""
        **Instructions:**  
        1. Inhale for 4 seconds  
        2. Hold your breath for 4 seconds  
        3. Exhale slowly for 4 seconds  
        4. Pause for 4 seconds  
        Repeat for 3-5 minutes.
        """)
    elif exercise == "Body Scan Meditation":
        st.markdown("""
        **Instructions:**  
        Focus your attention on each part of your body, starting from the toes up to the head. Notice sensations without judgment.  
        """)
        st.video("https://www.youtube.com/embed/w6T02g5hnT4") # Example video
    elif exercise == "Loving-Kindness":
        st.markdown("""
        **Instructions:**  
        Silently repeat phrases like 'May I be happy. May I be safe. May you be happy. May you be safe.' Send kindness to yourself and others.
        """)
    elif exercise == "Mindful Music":
        st.markdown("Play peaceful music to help create a mindful atmosphere.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")  # Example mp3

    st.divider()

    # Completion/Reflection
    if st.button("Mark This Exercise Completed"):
        st.success("Great job! Consistency is key to mindfulness.")
    st.info("“Breathe, relax, repeat.” 🧘‍♂️")

    # Optional: Add daily quote or motivation
    import random
    quotes = [
        "Be present for each breath.",
        "Small mindful moments add up.",
        "Peace begins with a single breath."
    ]
    st.caption(random.choice(quotes))

# ----- Worksheets & Journals -----
with tabs[8]:
    st.header("Downloadable Worksheets & Journals")
    st.write("Download self-reflection journals and CBT exercises. Choose a worksheet to get started:")

    # Select worksheet type
    worksheet_types = {
        "Self-Reflection Journal": "Date: ______\nHow did I feel today?\nWhat thoughts stood out?\nWhat am I grateful for?\n",
        "CBT Thought Record": "Date: ______\nSituation:\nEmotion:\nAutomatic Thought:\nEvidence For:\nEvidence Against:\nAlternative Thought:\nOutcome:\n",
        "Habit Tracker": "Date: ______\nHabit (describe):\nDid you complete it today? (Y/N)\nBarriers today:\nPlan for tomorrow:\n",
        "Gratitude Worksheet": "Date: ______\n3 things I'm grateful for today:\n1.\n2.\n3.\nHow can I express more gratitude?"
    }
    selection = st.selectbox("Select Worksheet Type", list(worksheet_types.keys()))
    content = worksheet_types[selection]

    st.subheader("Preview")
    st.code(content)

    st.download_button(
        "Download Worksheet",
        data=content,
        file_name=f"{selection.replace(' ','_').lower()}_template.txt"
    )

    st.divider()

    st.subheader("Write Here (Journaling)")
    entry = st.text_area("Write your thoughts or reflections. Download your entry when ready:")
    if entry:
        st.download_button(
            "Download My Journal Entry",
            data=entry,
            file_name="my_journal_entry.txt"
        )