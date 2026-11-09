"""
Voyager AI — Travel Planner Frontend
Design: Inspired by Trava AI (ChatGPT-style layout)
Compatible: graph.py + agents.py + state.py (7-agent LangGraph architecture)
"""

import os
import uuid
import hashlib
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import app

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Voyager AI · Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Trava-AI-inspired light + purple design
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');

/* ══════════════════════════════════════
   BASE
══════════════════════════════════════ */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #f0f2ff;
    color: #1a1a2e;
    margin: 0; padding: 0;
}
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #e8ebff; }
::-webkit-scrollbar-thumb { background: #a78bfa; border-radius: 10px; }
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════════════════════════════
   SIDEBAR  (left nav)
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7f5 !important;
    min-width: 240px !important;
    max-width: 260px !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

/* Logo */
.sb-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 1.4rem 1.3rem 0.6rem;
    font-family: 'Poppins', sans-serif;
    font-size: 1.3rem; font-weight: 700; color: #1a1a2e;
}
.sb-logo-icon {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; color: #fff;
}

/* Nav items */
.sb-nav { padding: 0.5rem 0.9rem; }
.sb-nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 0.6rem 0.9rem; border-radius: 12px;
    font-size: 0.88rem; font-weight: 500; color: #4b5563;
    cursor: pointer; margin-bottom: 2px;
    transition: background 0.15s;
}
.sb-nav-item:hover { background: #f3f0ff; color: #7c3aed; }
.sb-nav-item.active {
    background: #ede9fe; color: #7c3aed; font-weight: 600;
}
.sb-nav-badge {
    margin-left: auto;
    background: #7c3aed; color: #fff;
    font-size: 0.65rem; font-weight: 700;
    border-radius: 20px; padding: 1px 7px;
}

/* New Chat button */
.sb-new-chat-wrap {
    padding: 0.6rem 1.2rem 0.8rem;
}
.sb-new-chat {
    display: flex; align-items: center; justify-content: center; gap: 8px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: #fff; border-radius: 14px;
    padding: 0.65rem 0; width: 100%;
    font-size: 0.88rem; font-weight: 700;
    cursor: pointer; border: none;
    box-shadow: 0 4px 16px rgba(124,58,237,0.35);
    transition: box-shadow 0.2s, transform 0.15s;
}
.sb-new-chat:hover {
    box-shadow: 0 6px 24px rgba(124,58,237,0.5);
    transform: translateY(-1px);
}

/* Conversation history */
.sb-section-label {
    padding: 0.5rem 1.3rem 0.3rem;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #9ca3af;
}
.sb-conv-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 0.55rem 1.1rem; border-radius: 12px;
    margin: 1px 0.6rem; cursor: pointer;
    transition: background 0.15s;
}
.sb-conv-item:hover { background: #f3f0ff; }
.sb-conv-item.active-conv { background: #ede9fe; }
.sb-conv-icon {
    width: 30px; height: 30px; border-radius: 8px;
    background: linear-gradient(135deg, #ddd6fe, #c4b5fd);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0; margin-top: 1px;
}
.sb-conv-title {
    font-size: 0.82rem; font-weight: 600; color: #1a1a2e;
    line-height: 1.3; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis; max-width: 140px;
}
.sb-conv-sub {
    font-size: 0.72rem; color: #9ca3af; margin-top: 1px;
}

/* Trending card in sidebar */
.sb-trending {
    margin: 0.5rem 0.9rem 0;
    border-radius: 16px; overflow: hidden;
    position: relative; height: 110px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
.sb-trending img {
    width: 100%; height: 100%;
    object-fit: cover; filter: brightness(0.65);
}
.sb-trending-label {
    position: absolute; bottom: 10px; left: 12px;
    color: #fff; font-size: 0.8rem; font-weight: 700;
}
.sb-trending-badge {
    position: absolute; top: 10px; right: 10px;
    background: rgba(124,58,237,0.85);
    color: #fff; font-size: 0.65rem; font-weight: 700;
    border-radius: 20px; padding: 2px 8px; letter-spacing: 0.08em;
}

/* Logout */
.sb-logout {
    padding: 1rem 1.3rem;
    display: flex; align-items: center; gap: 8px;
    font-size: 0.84rem; color: #9ca3af; cursor: pointer;
    border-top: 1px solid #f0f0f8; margin-top: 0.5rem;
}
.sb-logout:hover { color: #ef4444; }

/* ══════════════════════════════════════
   MAIN CONTENT AREA
══════════════════════════════════════ */
.main-wrap {
    display: flex; gap: 0;
    min-height: 100vh;
}

/* Centre panel */
.centre-panel {
    flex: 1;
    padding: 1.5rem 2rem;
    background: #f4f5ff;
    min-height: 100vh;
}

/* Top bar */
.topbar {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-bottom: 1.8rem;
}
.topbar-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.3rem; font-weight: 700; color: #1a1a2e;
}
.topbar-search {
    display: flex; align-items: center;
    background: #fff; border: 1.5px solid #e5e7f5;
    border-radius: 24px; padding: 0.4rem 1rem;
    gap: 0.5rem; min-width: 220px;
    font-size: 0.84rem; color: #9ca3af;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Hero — "Where to next?" */
.hero-centre {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 2.5rem 1rem 1.5rem;
    text-align: center;
}
.hero-centre h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.4rem; font-weight: 800;
    color: #1a1a2e; margin: 1rem 0 0.5rem;
    line-height: 1.1;
}
.hero-centre p {
    color: #6b7280; font-size: 0.95rem;
    max-width: 420px; line-height: 1.6; margin-bottom: 1.5rem;
}
.hero-illustration {
    width: 180px; height: 150px;
    background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 100%);
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 5rem;
    box-shadow: 0 8px 32px rgba(124,58,237,0.15);
    margin-bottom: 0.5rem;
}

/* Quick chips */
.chip-row {
    display: flex; gap: 0.6rem; flex-wrap: wrap;
    justify-content: center; margin-bottom: 1.5rem;
}
.chip {
    background: #fff; border: 1.5px solid #e5e7f5;
    border-radius: 24px; padding: 0.4rem 1.1rem;
    font-size: 0.82rem; font-weight: 500; color: #374151;
    cursor: pointer; white-space: nowrap;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: all 0.18s;
}
.chip:hover { border-color: #a78bfa; color: #7c3aed; background: #faf5ff; }

/* Chat input bar */
.chat-input-wrap {
    background: #fff;
    border: 1.5px solid #e5e7f5;
    border-radius: 20px;
    padding: 0.9rem 1.2rem;
    display: flex; align-items: center; gap: 0.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    max-width: 640px; width: 100%; margin: 0 auto;
}
.chat-disclaimer {
    color: #9ca3af; font-size: 0.72rem;
    text-align: center; margin-top: 0.6rem;
}

/* Generate button */
.gen-btn-wrap > button {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 16px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1rem !important; font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transition: all 0.2s !important;
}
.gen-btn-wrap > button:hover {
    box-shadow: 0 6px 28px rgba(124,58,237,0.6) !important;
    transform: translateY(-2px) !important;
}

/* ══════════════════════════════════════
   RIGHT PANEL
══════════════════════════════════════ */
.right-panel {
    width: 320px; min-width: 300px;
    background: #fff;
    border-left: 1px solid #e5e7f5;
    padding: 1.5rem 1.2rem;
    min-height: 100vh;
    overflow-y: auto;
}
.rp-section-title {
    font-size: 1rem; font-weight: 700; color: #1a1a2e;
    margin-bottom: 0.3rem;
}
.rp-section-sub {
    font-size: 0.75rem; color: #9ca3af; margin-bottom: 0.9rem;
}
.smart-picks-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem; margin-bottom: 1.5rem;
}
.smart-pick-card {
    border-radius: 12px; overflow: hidden;
    position: relative; height: 80px;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.smart-pick-card:hover { transform: scale(1.03); }
.smart-pick-card img {
    width: 100%; height: 100%;
    object-fit: cover; filter: brightness(0.75);
}
.smart-pick-name {
    position: absolute; bottom: 5px; left: 6px;
    color: #fff; font-size: 0.65rem; font-weight: 600;
}
.continue-card {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    border-radius: 16px; padding: 1rem 1.1rem;
    margin-bottom: 1.5rem; position: relative;
    overflow: hidden; cursor: pointer;
    box-shadow: 0 4px 16px rgba(124,58,237,0.35);
}
.continue-card::before {
    content: ''; position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.continue-card-title {
    font-size: 1rem; font-weight: 700; color: #fff;
    margin-bottom: 0.2rem;
}
.continue-card-sub {
    font-size: 0.75rem; color: rgba(255,255,255,0.75);
}
.continue-card-arrow {
    position: absolute; right: 12px; top: 50%;
    transform: translateY(-50%);
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 1rem;
}
.inspire-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
}
.inspire-card {
    border-radius: 14px; overflow: hidden;
    position: relative; height: 90px; cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.inspire-card:hover { transform: scale(1.03); }
.inspire-card img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.7); }
.inspire-card-name {
    position: absolute; bottom: 7px; left: 8px;
    color: #fff; font-size: 0.72rem; font-weight: 600;
}
.rp-see-all {
    font-size: 0.75rem; font-weight: 600;
    color: #7c3aed; cursor: pointer; float: right;
    margin-top: -1.4rem; margin-bottom: 0.9rem;
}

/* ══════════════════════════════════════
   AGENT PIPELINE — results view
══════════════════════════════════════ */
.pipeline-label {
    font-family: 'Poppins', sans-serif;
    font-size: 1rem; font-weight: 700; color: #1a1a2e;
    display: flex; align-items: center; gap: 8px;
    margin: 1.2rem 0 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1.5px solid #e5e7f5;
}
[data-testid="stStatusWidget"] {
    background: #fff !important;
    border: 1.5px solid #e5e7f5 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #fff !important;
    border-radius: 16px 16px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #faf8ff !important;
    color: #374151 !important;
}
[data-testid="stStatusWidget"] * { color: #374151 !important; }

/* Result tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #fff !important;
    border-radius: 14px !important;
    padding: 0.3rem !important;
    gap: 0.3rem !important;
    border: 1.5px solid #e5e7f5 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #6b7280 !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    border: none !important;
    font-size: 0.84rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#7c3aed,#a855f7) !important;
    color: #fff !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #fff !important;
    border-radius: 0 0 14px 14px !important;
    border: 1.5px solid #e5e7f5 !important;
    border-top: none !important;
    padding: 1.4rem !important;
    color: #374151 !important;
}

/* Result content */
.result-card {
    background: #fafbff;
    border: 1.5px solid #ede9fe;
    border-radius: 14px; padding: 1.3rem 1.5rem;
    color: #374151; font-size: 0.9rem; line-height: 1.8;
}
.supervisor-banner {
    background: #f0ebff;
    border: 1.5px solid #c4b5fd;
    border-left: 4px solid #7c3aed;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    color: #4c1d95; font-size: 0.87rem;
    margin-bottom: 1rem; line-height: 1.6;
}

/* Final plan */
.final-card {
    background: linear-gradient(160deg, #fdf8ff 0%, #f0ebff 100%);
    border: 1.5px solid #c4b5fd;
    border-left: 5px solid #7c3aed;
    border-radius: 18px;
    padding: 2rem 2.2rem;
    color: #1a1a2e; line-height: 1.9; font-size: 0.95rem;
    box-shadow: 0 8px 32px rgba(124,58,237,0.1);
}

/* Metrics */
.metrics-row { display: flex; gap: 0.8rem; margin: 1.5rem 0; }
.metric-box {
    flex: 1; background: #fff;
    border: 1.5px solid #e5e7f5;
    border-radius: 16px; padding: 1rem 0.8rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s;
}
.metric-box:hover { transform: translateY(-2px); }
.metric-icon { font-size: 1.3rem; }
.metric-val { font-size: 1.6rem; font-weight: 800; color: #7c3aed; }
.metric-lbl { font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }

/* Approval card */
.approval-card {
    background: #fffbeb;
    border: 1.5px solid #fcd34d;
    border-left: 5px solid #f59e0b;
    border-radius: 18px; padding: 1.6rem 1.8rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(245,158,11,0.1);
}
.approval-title {
    font-size: 1.05rem; font-weight: 700; color: #92400e;
    display: flex; align-items: center; gap: 8px; margin-bottom: 0.4rem;
}
.approval-sub { color: #78350f; font-size: 0.85rem; margin-bottom: 1rem; }
.itinerary-preview {
    background: #fff; border: 1.5px solid #fde68a;
    border-radius: 12px; padding: 1.1rem 1.3rem;
    color: #374151; font-size: 0.88rem; line-height: 1.8;
    max-height: 400px; overflow-y: auto;
    margin-bottom: 1rem; white-space: pre-wrap;
}
.approve-btn > button {
    background: linear-gradient(135deg,#059669,#10b981) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    padding: 0.75rem !important; width: 100% !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.4) !important;
}
.reject-btn > button {
    background: linear-gradient(135deg,#dc2626,#ef4444) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    padding: 0.75rem !important; width: 100% !important;
    box-shadow: 0 4px 14px rgba(239,68,68,0.3) !important;
}

/* Download & save */
.save-bar {
    background: #f0ebff; border: 1.5px solid #ddd6fe;
    border-radius: 10px; padding: 0.65rem 1.1rem;
    color: #5b21b6; font-size: 0.84rem; margin-top: 0.5rem;
}
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg,#7c3aed,#a855f7) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
}

/* Inputs */
.stTextArea textarea {
    background: #fff !important;
    border: 1.5px solid #e5e7f5 !important;
    border-radius: 14px !important;
    color: #1a1a2e !important; font-size: 0.95rem !important;
    resize: none !important; line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
}
.stTextArea textarea::placeholder { color: #9ca3af !important; }
input[type="text"], .stTextInput input {
    background: #fff !important;
    border: 1.5px solid #e5e7f5 !important;
    border-radius: 10px !important; color: #1a1a2e !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: #6b7280 !important; font-size: 0.78rem !important; font-weight: 600 !important;
}
.stMarkdown p, .stMarkdown li { color: #374151 !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #1a1a2e !important; }
.stMarkdown code { background: #f0ebff !important; color: #7c3aed !important; border-radius: 4px; padding: 0.1em 0.4em; }
.stMarkdown strong { color: #1a1a2e !important; }
.stAlert { background: #f0ebff !important; border-radius: 12px !important; }
.stAlert p { color: #4c1d95 !important; }
hr { border-color: #e5e7f5 !important; }
.streamlit-expanderHeader { background: #fff !important; border-radius: 12px !important; color: #374151 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #7c3aed !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & HELPERS
# ─────────────────────────────────────────────────────────────────────────────

AGENT_META = {
    "supervisor":      ("🧭", "Supervisor Agent",    "Analysing & routing your request"),
    "flight_agent":    ("✈️", "Flight Agent",         "Airports, airlines & routes"),
    "hotel_agent":     ("🏨", "Hotel Agent",          "Best stays & neighbourhoods"),
    "weather_agent":   ("🌤️", "Weather Agent",        "Current weather & forecast"),
    "budget_agent":    ("💰", "Budget Agent",         "Cost analysis & savings tips"),
    "itinerary_agent": ("🗓️", "Itinerary Agent",      "Day-by-day travel plan"),
    "human_approval":  ("👤", "Your Review",          "Waiting for your feedback"),
    "final_response":  ("🎯", "Final Response Agent", "Polishing your complete plan"),
}

SMART_PICKS = [
    ("🇯🇵 Tokyo",    "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇬🇧 London",   "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=300&q=70"),
    ("🏔️ Alps",      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&q=70"),
]

INSPIRE_PICKS = [
    ("🤿 Maldives Dive", "https://images.unsplash.com/photo-1573843981267-be1ceea393e8?w=300&q=70"),
    ("🏄 Adventure",     "https://images.unsplash.com/photo-1530870110042-98b2cb110834?w=300&q=70"),
]

CONTINUE_DEST = None   # will be populated from history

QUICK_CHIPS = [
    "🎒 Trip under $100/day",
    "🧳 Solo travel places",
    "🏝️ 5 days in Bali itinerary",
    "🌸 Japan in April",
    "🗼 Paris weekend",
    "🏔️ Mountain retreat",
]

NAV_ITEMS = [
    ("💬", "Chats",       True),
    ("✈️", "Trips",       False),
    ("🔭", "Explore",     False),
    ("❤️", "Saved",       False),
    ("💡", "Inspiration", False),
    ("👥", "Community",   False),
]


def make_conversation_name(query: str) -> str:
    """Generate a short human-readable conversation name from the query."""
    q = query.strip()
    if not q:
        return "New Trip"
    words = q.split()
    # Pick up to 5 meaningful words
    stop = {"a","an","the","to","from","for","in","on","at","and","or","with","i","me","my","us","we","want","plan","trip","travel","visit"}
    keep = [w.capitalize() for w in words if w.lower() not in stop][:5]
    name  = " ".join(keep) if keep else " ".join(words[:4]).title()
    return name if len(name) <= 32 else name[:30] + "…"


def new_thread(query: str = ""):
    """Reset state for a fresh conversation with a new UUID thread."""
    name = make_conversation_name(query) if query else "New Trip"
    tid  = str(uuid.uuid4())
    st.session_state.thread_id            = tid
    st.session_state.conv_name            = name
    st.session_state.waiting_for_approval = False
    st.session_state.draft_itinerary      = ""
    st.session_state.approval_request     = ""
    st.session_state.collected            = {}
    st.session_state.run_complete         = False
    st.session_state.final_plan           = ""
    st.session_state.supervisor_reasoning = ""
    st.session_state.selected_agents      = []
    st.session_state.agent_logs           = {}
    st.session_state.metrics              = {"agents_run": 0, "llm_calls": 0, "status": "Ready"}
    st.session_state.active_query         = ""


def init_session():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    defaults = {
        "conv_name":             "New Chat",
        "waiting_for_approval":  False,
        "draft_itinerary":       "",
        "approval_request":      "",
        "collected":             {},
        "run_complete":          False,
        "final_plan":            "",
        "supervisor_reasoning":  "",
        "selected_agents":       [],
        "agent_logs":            {},
        "metrics":               {"agents_run": 0, "llm_calls": 0, "status": "Ready"},
        "active_query":          "",
        "trip_history":          [],   # [{name, query, date, thread, final}]
        "auto_approve":          False,
        "current_view":          "home",  # "home" | "results"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


def save_plan(query: str, content: str) -> str:
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn  = f"travel_plan_{ts}.md"
    d   = os.path.join(os.path.dirname(__file__), "travel_plans")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
        f.write(content)
    return fn


def build_export(query: str, c: dict) -> str:
    return f"""# ✈️ Voyager AI — Travel Plan
**Trip:** {c.get('conv_name', query)}
**Query:** {query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Thread:** {st.session_state.thread_id}

---
## 🧭 Supervisor Reasoning
{c.get("supervisor_reasoning", "N/A")}

---
## ✈️ Flights
{c.get("flight_results", "N/A")}

---
## 🏨 Hotels
{c.get("hotel_results", "N/A")}

---
## 🌤️ Weather
{c.get("weather_results", "N/A")}

---
## 💰 Budget
{c.get("budget_results", "N/A")}

---
## 🗓️ Itinerary
{c.get("itinerary", "N/A")}

---
## 🎯 Final Plan
{c.get("final_response", "N/A")}

---
*Agents: {c.get("agents_run",0)} · LLM Calls: {c.get("llm_calls",0)}*
*Voyager AI — LangGraph · Groq · LLaMA 3*
"""


# ─────────────────────────────────────────────────────────────────────────────
# THREE-COLUMN LAYOUT  (sidebar | centre | right-panel)
# ─────────────────────────────────────────────────────────────────────────────

left_col, centre_col, right_col = st.columns([1.1, 3.4, 1.8])


# ══════════════════════════════════════════════════════════════════════════════
# LEFT SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with left_col:

    # Logo
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">✈</div>
        Voyager AI
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sb-nav">', unsafe_allow_html=True)
    for icon, label, active in NAV_ITEMS:
        cls = "sb-nav-item active" if active else "sb-nav-item"
        badge = '<span class="sb-nav-badge">3</span>' if label == "Chats" and st.session_state.trip_history else ""
        st.markdown(f'<div class="{cls}">{icon}&nbsp;&nbsp;{label}{badge}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.5rem 0.9rem;'>", unsafe_allow_html=True)

    # New Chat button
    st.markdown('<div class="sb-new-chat-wrap">', unsafe_allow_html=True)
    if st.button("＋  New Chat", key="sb_new_chat", use_container_width=True):
        new_thread()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Conversation history (ChatGPT-style with names)
    if st.session_state.trip_history:
        st.markdown('<div class="sb-section-label">Recent</div>', unsafe_allow_html=True)
        for i, item in enumerate(reversed(st.session_state.trip_history[-8:])):
            is_active = item["thread"] == st.session_state.thread_id
            cls = "sb-conv-item active-conv" if is_active else "sb-conv-item"
            emoji = "🌍" if i % 3 == 0 else ("✈️" if i % 3 == 1 else "🏖️")
            st.markdown(f"""
            <div class="{cls}">
                <div class="sb-conv-icon">{emoji}</div>
                <div>
                    <div class="sb-conv-title">{item['name']}</div>
                    <div class="sb-conv-sub">{item['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Trending destination card
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Trending</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-trending">
        <img src="https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&q=70" alt="Bangkok"/>
        <div class="sb-trending-label">🇹🇭 Bangkok</div>
        <div class="sb-trending-badge">TRENDING</div>
    </div>
    """, unsafe_allow_html=True)

    # Settings (auto-approve)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚙️ Settings"):
        st.session_state.auto_approve = st.toggle(
            "Auto-approve itinerary",
            value=st.session_state.auto_approve,
        )
        st.caption("When ON, skips the human review step.")

    # Logout
    st.markdown("""
    <div class="sb-logout">⬅️&nbsp; Logout</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CENTRE PANEL
# ══════════════════════════════════════════════════════════════════════════════

with centre_col:

    # ── Top bar ──────────────────────────────────────────────────────────────
    conv_display = st.session_state.conv_name
    top_l, top_r = st.columns([2, 1])
    with top_l:
        st.markdown(f"""
        <div class="topbar-title">
            {conv_display}
        </div>
        """, unsafe_allow_html=True)
    with top_r:
        st.markdown("""
        <div class="topbar-search">
            🔍&nbsp; Search Locations…
        </div>
        """, unsafe_allow_html=True)

    has_results = any(
        st.session_state.collected.get(k)
        for k in ["flight_results","hotel_results","weather_results",
                  "budget_results","itinerary","final_response"]
    )

    # ── HOME VIEW (no results yet) ───────────────────────────────────────────
    if not has_results and not st.session_state.waiting_for_approval:

        # Hero illustration
        st.markdown("""
        <div class="hero-centre">
            <div class="hero-illustration">🏖️</div>
            <h1>Where to next?</h1>
            <p>Plan your perfect trip with AI.<br>
            Discover places, build itineraries, and explore smarter.</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick chips as Streamlit buttons in a row
        chip_cols = st.columns(len(QUICK_CHIPS))
        quick_fill = ""
        for cc, chip_label in zip(chip_cols, QUICK_CHIPS):
            with cc:
                if st.button(chip_label, key=f"chip_{chip_label}"):
                    quick_fill = chip_label.split(" ", 1)[1] if " " in chip_label else chip_label

    # ── RESULTS VIEW (after run) ─────────────────────────────────────────────
    else:
        quick_fill = ""

        # Agent pipeline live outputs
        c = st.session_state.collected

        if has_results:
            # Metrics
            m = st.session_state.metrics
            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-icon">🤖</div>
                    <div class="metric-val">{m["agents_run"]}</div>
                    <div class="metric-lbl">Agents Run</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon">🔁</div>
                    <div class="metric-val">{m["llm_calls"]}</div>
                    <div class="metric-lbl">LLM Calls</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon">📊</div>
                    <div class="metric-val" style="font-size:0.9rem;padding-top:.5rem">{m["status"]}</div>
                    <div class="metric-lbl">Status</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon">🧵</div>
                    <div class="metric-val" style="font-size:0.75rem;padding-top:.6rem">{st.session_state.thread_id[:8]}…</div>
                    <div class="metric-lbl">Thread ID</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Supervisor banner
            if c.get("supervisor_reasoning"):
                st.markdown(f"""
                <div class="supervisor-banner">
                    🧭 <strong>Supervisor:</strong> {c["supervisor_reasoning"]}
                </div>
                """, unsafe_allow_html=True)

            # Tabs for agent outputs
            tab_labels, tab_keys = [], []
            for key, lbl in [("flight_results","✈️ Flights"),("hotel_results","🏨 Hotels"),
                             ("weather_results","🌤️ Weather"),("budget_results","💰 Budget"),
                             ("itinerary","🗓️ Itinerary")]:
                if c.get(key):
                    tab_labels.append(lbl); tab_keys.append(key)

            if tab_labels:
                st.markdown('<div class="pipeline-label">📋 Agent Outputs</div>', unsafe_allow_html=True)
                tabs = st.tabs(tab_labels)
                for tab, key in zip(tabs, tab_keys):
                    with tab:
                        st.markdown(f'<div class="result-card">{c[key]}</div>', unsafe_allow_html=True)

        # Approval section
        if st.session_state.waiting_for_approval:
            st.markdown("""
            <div class="approval-card">
                <div class="approval-title">👤 Review Your Draft Itinerary</div>
                <div class="approval-sub">
                    Your AI agents have finished planning. Please review the itinerary below,
                    then approve it or request revisions.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.draft_itinerary:
                with st.expander("📋 Draft Itinerary", expanded=True):
                    st.markdown(
                        f'<div class="itinerary-preview">{st.session_state.draft_itinerary}</div>',
                        unsafe_allow_html=True,
                    )

            if st.session_state.auto_approve:
                feedback_text = "Auto-approved."
                approve = True
            else:
                feedback_text = st.text_area(
                    "✍️ Your feedback (optional — only needed for revision requests)",
                    placeholder="Looks great, approve it!\n— OR —\nPlease swap Day 3 to include shopping, and add more budget hotels.",
                    height=100, key="feedback_ta",
                )
                ca, cr = st.columns(2)
                approve = None
                with ca:
                    st.markdown('<div class="approve-btn">', unsafe_allow_html=True)
                    if st.button("✅  Approve — Build Final Plan", key="btn_approve", use_container_width=True):
                        approve = True
                    st.markdown('</div>', unsafe_allow_html=True)
                with cr:
                    st.markdown('<div class="reject-btn">', unsafe_allow_html=True)
                    if st.button("🔄  Request Revision", key="btn_reject", use_container_width=True):
                        approve = False
                    st.markdown('</div>', unsafe_allow_html=True)

            if approve is not None:
                config   = {"configurable": {"thread_id": st.session_state.thread_id}}
                feedback_payload = {
                    "approved": approve,
                    "feedback": (feedback_text.strip() if feedback_text
                                 else ("Approved." if approve else "Please revise.")),
                }
                st.session_state.waiting_for_approval = False
                st.session_state.metrics["status"]    = "Resuming…"
                st.markdown('<div class="pipeline-label">🎯 Final Response Agent</div>', unsafe_allow_html=True)
                try:
                    for chunk in app.stream(
                        Command(resume=feedback_payload), config=config, stream_mode="updates"
                    ):
                        for node_name, state_update in chunk.items():
                            icon, label, desc = AGENT_META.get(node_name, ("🔧", node_name, ""))
                            with st.status(f"{icon}  {label}", state="complete", expanded=True):
                                if node_name == "final_response":
                                    text = state_update.get("final_response", "")
                                    st.session_state.final_plan = text
                                    st.session_state.collected["final_response"] = text
                                    st.markdown(text or "_No final response._")
                                lc = state_update.get("llm_calls", 0)
                                if lc:
                                    st.session_state.metrics["llm_calls"] = lc
                                    st.session_state.collected["llm_calls"] = lc
                except Exception as exc:
                    st.error(f"⚠️ Error resuming graph: `{exc}`")
                st.session_state.run_complete         = True
                st.session_state.metrics["status"]    = "✅ Complete"
                st.session_state.collected["agents_run"] = st.session_state.metrics["agents_run"]
                st.session_state.trip_history.append({
                    "name":   st.session_state.conv_name,
                    "query":  st.session_state.active_query,
                    "date":   datetime.now().strftime("%d %b %Y, %H:%M"),
                    "thread": st.session_state.thread_id,
                    "final":  st.session_state.final_plan[:120],
                })
                st.rerun()

        # Final plan
        if st.session_state.run_complete and c.get("final_response"):
            st.markdown("---")
            st.markdown('<div class="pipeline-label">🎯 Your Complete Travel Plan</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="final-card">{c["final_response"]}</div>',
                unsafe_allow_html=True,
            )

            # Save & download
            q          = st.session_state.active_query
            export_md  = build_export(q, c)
            fname      = f"travel_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            saved_fn   = save_plan(q, export_md)

            d1, d2, d3 = st.columns([1, 2, 1])
            with d1:
                st.download_button(
                    "⬇️ Download Plan",
                    data=export_md, file_name=fname,
                    mime="text/markdown", use_container_width=True,
                )
            with d2:
                st.markdown(
                    f'<div class="save-bar">📁 Saved → <code>travel_plans/{saved_fn}</code></div>',
                    unsafe_allow_html=True,
                )
            with d3:
                if st.button("🆕 New Trip", key="btn_new_trip", use_container_width=True):
                    new_thread()
                    st.rerun()

    # ── CHAT INPUT (always at bottom of centre panel) ─────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    user_query = st.text_area(
        "",
        value=quick_fill,
        placeholder="✈️  Ask me anything… e.g. Plan a 7-day Japan trip from India under ₹2 Lakhs",
        height=90,
        label_visibility="collapsed",
        key="main_query_input",
    )

    gen_col, clr_col = st.columns([6, 1])
    with gen_col:
        st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
        generate = st.button(
            "🚀  Generate My Travel Plan",
            key="btn_generate",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with clr_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️", key="btn_clear", help="Clear results"):
            new_thread()
            st.rerun()

    st.markdown(
        '<div class="chat-disclaimer">⚠️ Voyager AI can make mistakes. Always verify critical travel info.</div>',
        unsafe_allow_html=True,
    )


# ── GENERATE HANDLER ──────────────────────────────────────────────────────────

if generate:
    if not user_query.strip():
        with centre_col:
            st.warning("Please describe your trip first.")
    else:
        # Give this conversation a human-readable name
        conv_name = make_conversation_name(user_query)
        st.session_state.conv_name    = conv_name
        st.session_state.active_query = user_query
        st.session_state.collected    = {}
        st.session_state.run_complete = False
        st.session_state.final_plan   = ""
        st.session_state.waiting_for_approval = False
        st.session_state.supervisor_reasoning = ""
        st.session_state.selected_agents      = []
        st.session_state.agent_logs           = {}
        st.session_state.metrics = {"agents_run": 0, "llm_calls": 0, "status": "Running…"}

        config  = {"configurable": {"thread_id": st.session_state.thread_id}}
        initial = {
            "messages":        [HumanMessage(content=user_query)],
            "user_query":      user_query,
            "user_id":         st.session_state.thread_id,
            "flight_results":  "",
            "hotel_results":   "",
            "weather_results": "",
            "budget_results":  "",
            "itinerary":       "",
            "llm_calls":       0,
        }

        with centre_col:
            st.markdown('<div class="pipeline-label">🤖 Agent Pipeline — Live</div>', unsafe_allow_html=True)

        agents_run  = 0
        llm_calls   = 0
        interrupted = False

        try:
            for chunk in app.stream(initial, config=config, stream_mode="updates"):

                if "__interrupt__" in chunk:
                    interrupted = True
                    interrupt_val = chunk["__interrupt__"]
                    if isinstance(interrupt_val, (list, tuple)) and len(interrupt_val) > 0:
                        payload = interrupt_val[0].value if hasattr(interrupt_val[0], "value") else interrupt_val[0]
                    else:
                        payload = interrupt_val

                    if isinstance(payload, dict):
                        st.session_state.draft_itinerary  = payload.get("draft_itinerary", "")
                        st.session_state.approval_request = payload.get("approval_request", "")
                    else:
                        st.session_state.draft_itinerary  = st.session_state.collected.get("itinerary", "")
                        st.session_state.approval_request = "Please review the draft itinerary."
                    st.session_state.waiting_for_approval = True
                    st.session_state.metrics["status"]    = "⏳ Awaiting approval"
                    break

                for node_name, state_update in chunk.items():
                    icon, label, desc = AGENT_META.get(node_name, ("🔧", node_name, ""))
                    with centre_col:
                        with st.status(f"{icon}  {label}", state="complete", expanded=True):
                            st.caption(desc)

                            if node_name == "supervisor":
                                reasoning = state_update.get("supervisor_reasoning", "")
                                selected  = state_update.get("selected_agents", [])
                                st.session_state.supervisor_reasoning = reasoning
                                st.session_state.selected_agents      = selected
                                st.session_state.collected["supervisor_reasoning"] = reasoning
                                if reasoning:
                                    st.markdown(f"**Reasoning:** {reasoning}")
                                if selected:
                                    st.markdown(f"**Agents selected:** `{'` · `'.join(selected)}`")

                            elif node_name == "flight_agent":
                                text = state_update.get("flight_results", "")
                                st.session_state.collected["flight_results"] = text
                                st.markdown(text or "_No flight data._")
                                agents_run += 1

                            elif node_name == "hotel_agent":
                                text = state_update.get("hotel_results", "")
                                st.session_state.collected["hotel_results"] = text
                                st.markdown(text or "_No hotel data._")
                                agents_run += 1

                            elif node_name == "weather_agent":
                                text = state_update.get("weather_results", "")
                                st.session_state.collected["weather_results"] = text
                                st.markdown(text or "_No weather data._")
                                agents_run += 1

                            elif node_name == "budget_agent":
                                text = state_update.get("budget_results", "")
                                st.session_state.collected["budget_results"] = text
                                st.markdown(text or "_No budget data._")
                                agents_run += 1

                            elif node_name == "itinerary_agent":
                                text = state_update.get("itinerary", "")
                                st.session_state.collected["itinerary"] = text
                                if not st.session_state.draft_itinerary:
                                    st.session_state.draft_itinerary = text
                                st.markdown(text or "_No itinerary._")
                                agents_run += 1

                            elif node_name == "final_response":
                                text = state_update.get("final_response", "")
                                st.session_state.final_plan = text
                                st.session_state.collected["final_response"] = text
                                st.markdown(text or "_No final response._")
                                agents_run += 1

                    lc = state_update.get("llm_calls", 0)
                    if lc: llm_calls = lc

        except Exception as exc:
            with centre_col:
                st.error(f"⚠️ Agent error: `{exc}`")

        # Update metrics
        st.session_state.metrics["agents_run"] = agents_run
        st.session_state.metrics["llm_calls"]  = llm_calls
        st.session_state.collected["agents_run"] = agents_run
        st.session_state.collected["llm_calls"]  = llm_calls
        st.session_state.collected["conv_name"]  = conv_name

        if not interrupted and not st.session_state.waiting_for_approval:
            st.session_state.run_complete = True
            st.session_state.metrics["status"] = "✅ Complete"
            st.session_state.trip_history.append({
                "name":   conv_name,
                "query":  user_query,
                "date":   datetime.now().strftime("%d %b %Y, %H:%M"),
                "thread": st.session_state.thread_id,
                "final":  st.session_state.final_plan[:120],
            })

        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════

with right_col:

    # ── Smart picks for you ───────────────────────────────────────────────────
    st.markdown("""
    <div class="rp-section-title">Smart picks for you</div>
    <div class="rp-section-sub">Curated based on your travel style and recent searches</div>
    """, unsafe_allow_html=True)

    pick_cols = st.columns(3)
    for pc, (name, img) in zip(pick_cols, SMART_PICKS):
        with pc:
            st.markdown(f"""
            <div class="smart-pick-card">
                <img src="{img}" alt="{name}"/>
                <div class="smart-pick-name">{name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Continue Planning ─────────────────────────────────────────────────────
    if st.session_state.trip_history:
        last = st.session_state.trip_history[-1]
        st.markdown("""
        <div class="rp-section-title">Continue Planning</div>
        <div class="rp-section-sub">Pick up where you left off and finish your trip</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="continue-card">
            <div class="continue-card-title">🌍 {last["name"]}</div>
            <div class="continue-card-sub">{last.get("final","")[:60]}{"…" if len(last.get("final",""))>60 else ""}</div>
            <div class="continue-card-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="rp-section-title">Continue Planning</div>
        <div class="rp-section-sub">Your recent trips will appear here</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="continue-card">
            <div class="continue-card-title">🗺️ Japan Adventure</div>
            <div class="continue-card-sub">Start your first plan below ↓</div>
            <div class="continue-card-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Get Inspired ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;">
        <div class="rp-section-title">Get inspired</div>
        <div class="rp-see-all">See All</div>
    </div>
    """, unsafe_allow_html=True)

    inspire_cols = st.columns(2)
    for ic, (name, img) in zip(inspire_cols, INSPIRE_PICKS):
        with ic:
            st.markdown(f"""
            <div class="inspire-card">
                <img src="{img}" alt="{name}"/>
                <div class="inspire-card-name">{name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Agent Pipeline Status ─────────────────────────────────────────────────
    st.markdown("""
    <div class="rp-section-title">⚡ Agent Status</div>
    <div class="rp-section-sub">Your 7-agent AI pipeline</div>
    """, unsafe_allow_html=True)

    pipeline_steps = [
        ("🧭", "Supervisor"),
        ("✈️", "Flight"),
        ("🏨", "Hotel"),
        ("🌤️", "Weather"),
        ("💰", "Budget"),
        ("🗓️", "Itinerary"),
        ("👤", "You Review"),
        ("🎯", "Final Plan"),
    ]
    logs = st.session_state.agent_logs
    for icon, name in pipeline_steps:
        key_match = name.lower().replace(" ", "_")
        done = any(key_match in k for k in logs.keys()) or (
            name == "Final Plan" and st.session_state.run_complete
        )
        dot  = "🟢" if done else "⚪"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:0.3rem 0;
                    font-size:0.82rem;color:#374151;border-bottom:1px solid #f0f0f8;">
            {dot} {icon} {name}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chase the Experiences tag ─────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#7c3aed,#a855f7);
                border-radius:16px;padding:1rem 1.2rem;text-align:center;
                box-shadow:0 4px 16px rgba(124,58,237,0.3);">
        <div style="font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:0.3rem;">
            🌟 Chase the Experiences
        </div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.8);">
            Life is short. The world is big.<br>Start planning today.
        </div>
    </div>
    """, unsafe_allow_html=True)
