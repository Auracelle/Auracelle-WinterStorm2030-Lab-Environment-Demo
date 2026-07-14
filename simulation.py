import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random

# ══════════════════════════════════════════════════════════
# GUARD — must be logged in via app.py
# ══════════════════════════════════════════════════════════
if not st.session_state.get("authenticated"):
    st.switch_page("app.py")

st.set_page_config(page_title="WinterStorm2030 | Simulation", layout="wide")

st.markdown('''
<style>
.stApp { background: linear-gradient(135deg, #0a1822 0%, #16303f 100%); color: #e8eef2; }
.stButton > button {
    background: #0ed7c4 !important; color: #0a1822 !important; font-weight: 700 !important;
    border: none !important; border-radius: 6px !important; padding: 10px 20px !important;
    box-shadow: 0 4px 0 #0ba894, 0 4px 8px rgba(0,0,0,0.35) !important;
    transition: all 0.1s ease !important; position: relative !important; top: 0 !important;
}
.stButton > button:hover { background: #15e8d4 !important; }
.stButton > button:active { top: 4px !important; box-shadow: 0 0 0 #0ba894 !important; }
div[data-testid="stMetricValue"] { color: #0ed7c4; }
</style>
''', unsafe_allow_html=True)

SHEET_NAME = "WinterStorm2030_Session"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

STATE_HEADERS = ["turn", "cap_gap", "concession_modifier", "narrative_modifier",
                  "doctrine", "scenario_name", "scenario_desc", "treaty_flag", "win_win_active"]
LOG_HEADERS = ["timestamp", "turn", "callsign", "actor", "move_type", "source", "detail", "cap_gap_delta"]
ARB_HEADERS = ["case_id", "status", "violation", "asset", "stage", "opened_by", "opened_at"]

DOCTRINE_LABELS = {"rus": "🇷🇺 Russia — Narrative-First", "prc": "🇨🇳 China — Platform-First", "hybrid": "⬡ Compound Hybrid"}

RED_MOVE_LIBRARY = {
    "rus": [
        {"title": "Maskirovka — Below-Threshold Vessel Activity", "desc": "GRU-linked vessel operates without transponder near the Svalbard EEZ. Attribution deniable.", "tag": "PROBE", "delta": 3},
        {"title": "Article 4 Doubt Narrative", "desc": "AI-generated content questioning Finnish alliance commitment circulates on Nordic-language channels.", "tag": "EXPLOIT", "delta": 5},
        {"title": "Reflexive Control — Greenland Friction", "desc": "Amplifies US–Greenland adversarial framing to widen an existing seam.", "tag": "ESCALATE", "delta": 6},
        {"title": "GRU Signal Interference", "desc": "Below-Article-4 signal jamming reported near the GIUK gap.", "tag": "PROBE", "delta": 2},
    ],
    "prc": [
        {"title": "Dual-Use Station Activation", "desc": "Research/surveillance station near the Polar Connect corridor increases data-collection posture.", "tag": "PROBE", "delta": 3},
        {"title": "CAOFA Leverage Offer", "desc": "Conditional scientific-cooperation support offered in exchange for data-sovereignty concessions.", "tag": "EXPLOIT", "delta": 4},
        {"title": "Platform-Scale Influence Push", "desc": "Coordinated content targeting Greenlandic independence sentiment, framed as economic opportunity.", "tag": "ESCALATE", "delta": 5},
        {"title": "Rare-Earth Investment Conditionality", "desc": "Infrastructure financing offer quietly conditioned on long-term access rights.", "tag": "EXPLOIT", "delta": 4},
    ],
    "hybrid": [
        {"title": "Compound Operation — Cyber + Narrative", "desc": "Coincident cyber probe and narrative push designed to saturate Blue Team attention.", "tag": "ESCALATE", "delta": 7},
        {"title": "Russia–China Narrative Convergence", "desc": "Independently-sourced but mutually reinforcing content questioning NATO Arctic governance legitimacy.", "tag": "EXPLOIT", "delta": 6},
    ],
}

ARB_STAGES = ["Notification", "Joint Verification", "Interim Continuity", "Time-Limited Conciliation", "Binding Arbitration"]
VIOLATION_TYPES = ["Unsafe Interference", "Unauthorized Inspection", "Navigation Obstruction", "Tampering",
                    "Discriminatory Access Restriction", "Data Denial", "Coercive Maintenance Disruption"]
ASSETS = ["GIUK Undersea Cable Corridor", "Svalbard Fibre Link", "Arctic Pipeline Segment",
          "Denmark Strait Shipping Lane", "Northern Sea Route Corridor"]

# ══════════════════════════════════════════════════════════
# GOOGLE SHEETS — shared, persistent state (this is what makes async multiplayer work)
# ══════════════════════════════════════════════════════════
@st.cache_resource
def get_client():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_resource
def get_sheet():
    client = get_client()
    try:
        sh = client.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        st.error(f"Google Sheet '{SHEET_NAME}' not found or not shared with the service account. "
                 f"Create it and share it (Editor access) with the service account email in your secrets.")
        st.stop()
    # ensure worksheets exist
    titles = [ws.title for ws in sh.worksheets()]
    if "state" not in titles:
        ws = sh.add_worksheet(title="state", rows=2, cols=len(STATE_HEADERS))
        ws.append_row(STATE_HEADERS)
        ws.append_row([1, 64, 0, 0, "rus", "", "", "FALSE", "FALSE"])
    if "log" not in titles:
        ws = sh.add_worksheet(title="log", rows=1, cols=len(LOG_HEADERS))
        ws.append_row(LOG_HEADERS)
    if "arbitration" not in titles:
        ws = sh.add_worksheet(title="arbitration", rows=1, cols=len(ARB_HEADERS))
        ws.append_row(ARB_HEADERS)
    return sh

def load_state():
    sh = get_sheet()
    records = sh.worksheet("state").get_all_records()
    if not records:
        return {"turn": 1, "cap_gap": 64, "concession_modifier": 0, "narrative_modifier": 0,
                "doctrine": "rus", "scenario_name": "", "scenario_desc": "", "treaty_flag": "FALSE", "win_win_active": "FALSE"}
    return records[0]

def save_state(state):
    sh = get_sheet()
    ws = sh.worksheet("state")
    row = [state.get(h, "") for h in STATE_HEADERS]
    ws.update("A2", [row])

def append_log(turn, callsign, actor, move_type, source, detail, cap_gap_delta):
    sh = get_sheet()
    ws = sh.worksheet("log")
    ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), turn, callsign, actor, move_type, source, detail, cap_gap_delta])

def load_log():
    sh = get_sheet()
    records = sh.worksheet("log").get_all_records()
    if not records:
        return pd.DataFrame(columns=LOG_HEADERS)
    df = pd.DataFrame(records)
    return df.iloc[::-1]  # most recent first

def load_arbitration():
    sh = get_sheet()
    records = sh.worksheet("arbitration").get_all_records()
    return pd.DataFrame(records) if records else pd.DataFrame(columns=ARB_HEADERS)

def save_arbitration_row(row_dict, row_index=None):
    sh = get_sheet()
    ws = sh.worksheet("arbitration")
    row = [row_dict.get(h, "") for h in ARB_HEADERS]
    if row_index is None:
        ws.append_row(row)
    else:
        ws.update(f"A{row_index+2}", [row])  # +2: header row + 1-indexing

# ══════════════════════════════════════════════════════════
# GAME LOGIC
# ══════════════════════════════════════════════════════════
def recompute_cap_gap(state):
    gap = 50 + int(state.get("concession_modifier", 0)) + int(state.get("narrative_modifier", 0))
    gap = max(0, min(100, gap))
    state["cap_gap"] = gap
    treaty = str(state.get("treaty_flag", "FALSE")) == "TRUE"
    state["win_win_active"] = "TRUE" if (gap < 45 and treaty) else "FALSE"
    return state

def trigger_concession(actor, ctype, desc, callsign, is_red):
    state = load_state()
    type_delta = {"Access": 4, "Resource": 3, "Narrative-Legal": 2}
    delta = type_delta.get(ctype, 3)
    mod = int(state.get("concession_modifier", 0)) + (delta if is_red else -delta)
    state["concession_modifier"] = max(-20, min(20, mod))
    if ctype == "Narrative-Legal" and not is_red:
        state["treaty_flag"] = "TRUE"
    state = recompute_cap_gap(state)
    save_state(state)
    append_log(state["turn"], callsign, actor, f"CONCESSION — {ctype}", "ANALYST", desc, delta if is_red else -delta)
    return state

def generate_ai_move(state):
    doctrine = state.get("doctrine", "rus")
    pool = RED_MOVE_LIBRARY.get(doctrine, RED_MOVE_LIBRARY["rus"])
    move = random.choice(pool)
    mod = int(state.get("narrative_modifier", 0)) + move["delta"]
    state["narrative_modifier"] = max(-15, min(15, mod))
    return state, move

def end_turn(callsign):
    state = load_state()
    state, move = generate_ai_move(state)
    state = recompute_cap_gap(state)
    state["turn"] = int(state["turn"]) + 1
    save_state(state)
    append_log(state["turn"], "Agentic AI", DOCTRINE_LABELS.get(state["doctrine"], state["doctrine"]),
               f"{move['tag']} — {move['title']}", "SIMULATED", move["desc"], move["delta"])
    return state, move

def open_arbitration(violation, asset, callsign):
    save_arbitration_row({
        "case_id": f"{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "OPEN", "violation": violation, "asset": asset,
        "stage": 1, "opened_by": callsign, "opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def advance_arbitration(idx, row):
    df = load_arbitration()
    new_stage = int(row["stage"]) + 1
    df.loc[idx, "stage"] = new_stage
    sh = get_sheet()
    ws = sh.worksheet("arbitration")
    ws.update(f"A{idx+2}", [[row["case_id"], "OPEN", row["violation"], row["asset"], new_stage, row["opened_by"], row["opened_at"]]])
    state = load_state()
    if new_stage == 3:  # Interim Continuity relieves tension slightly
        state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) - 1))
    elif new_stage == 2:
        state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) + 1))
    state = recompute_cap_gap(state)
    save_state(state)

def issue_ruling(idx, row, callsign):
    rulings = [
        {"ruling": "FOR BLUE", "delta": -6, "summary": "The Tribunal finds the violation substantiated. The responsible party shall cease the conduct and provide notification assurances going forward."},
        {"ruling": "SPLIT", "delta": -3, "summary": "The Tribunal finds the violation substantiated in part. Continuity of operations is affirmed; both parties shall provide notification going forward."},
        {"ruling": "FOR RED", "delta": 2, "summary": "The Tribunal finds insufficient evidence to substantiate the claim as framed. Continuity of operations affirmed without further remedy."},
    ]
    result = random.choice(rulings)
    state = load_state()
    state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) + result["delta"]))
    state["treaty_flag"] = "TRUE"
    state = recompute_cap_gap(state)
    save_state(state)
    sh = get_sheet()
    ws = sh.worksheet("arbitration")
    ws.update(f"B{idx+2}", [[f"CLOSED — {result['ruling']}"]])
    append_log(state["turn"], "Arbitration Tribunal", f"{row['violation']} vs {row['asset']}",
               f"BINDING RULING — {result['ruling']}", "ARBITRATION", result["summary"], result["delta"])

# ══════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════
callsign = st.session_state.get("callsign", "PARTICIPANT")
state = load_state()

st.markdown(f"### 🧊 WinterStorm2030 &nbsp;·&nbsp; Logged in as **{callsign}**")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Turn", state["turn"])
c2.metric("NATO Capability Gap", f"{state['cap_gap']}%")
c3.metric("Active Doctrine", DOCTRINE_LABELS.get(state.get("doctrine", "rus"), "—"))
c4.metric("Win-Win", "🌟 YES" if str(state.get("win_win_active")) == "TRUE" else "No")

colA, colB = st.columns([1, 1])
with colA:
    if st.button("🔄 Refresh Shared State"):
        st.cache_resource.clear()
        st.rerun()
with colB:
    if st.button("⏩ End Turn (generate Red Team move)"):
        state, move = end_turn(callsign)
        st.success(f"Turn {state['turn']} — {move['tag']}: {move['title']}")
        st.rerun()

st.divider()

tab_scenario, tab_concession, tab_arbitration, tab_log = st.tabs(
    ["📋 Scenario Setup", "🤝 Concession Engine", "⚖ Arbitration Track", "📜 Shared Move Log"]
)

with tab_scenario:
    st.write("Set once, visible to every participant on refresh.")
    name = st.text_input("Scenario Name", value=state.get("scenario_name", ""))
    desc = st.text_area("Scenario Description", value=state.get("scenario_desc", ""))
    doctrine = st.selectbox("Active Adversary Doctrine", options=list(DOCTRINE_LABELS.keys()),
                             format_func=lambda k: DOCTRINE_LABELS[k],
                             index=list(DOCTRINE_LABELS.keys()).index(state.get("doctrine", "rus")))
    if st.button("Save Scenario"):
        state["scenario_name"] = name
        state["scenario_desc"] = desc
        state["doctrine"] = doctrine
        save_state(state)
        st.success("Scenario saved — visible to all participants on their next refresh.")
        st.rerun()

with tab_concession:
    st.write("Every concession is written to the shared log immediately — other participants see it on refresh.")
    actor = st.selectbox("Triggering Actor", ["Norway", "Denmark/Greenland", "Finland", "Iceland", "Canada",
                                               "United States", "Russia (Red)", "China (Red)"])
    ctype = st.selectbox("Concession Type", ["Access", "Resource", "Narrative-Legal"])
    desc = st.text_area("Description")
    if st.button("Trigger Concession"):
        is_red = "Red" in actor
        state = trigger_concession(actor, ctype, desc or "No description provided", callsign, is_red)
        st.success(f"Logged — Cap Gap now {state['cap_gap']}%")
        st.rerun()

with tab_arbitration:
    st.write("Boundary Waters / Columbia River / Canterbury model — a standing escalation ladder, not a single trigger.")
    with st.expander("Open a new case"):
        violation = st.selectbox("Grey-Zone Violation Type", VIOLATION_TYPES)
        asset = st.selectbox("Strategic Asset", ASSETS)
        if st.button("Open Arbitration Case"):
            open_arbitration(violation, asset, callsign)
            st.success("Case opened.")
            st.rerun()

    arb_df = load_arbitration()
    open_cases = arb_df[arb_df["status"] == "OPEN"] if not arb_df.empty else arb_df
    if open_cases.empty:
        st.info("No open arbitration cases.")
    else:
        for idx, row in open_cases.iterrows():
            with st.container(border=True):
                stage_num = int(row["stage"])
                st.markdown(f"**{row['violation']}** vs **{row['asset']}** — Stage {stage_num}: *{ARB_STAGES[stage_num-1]}*  \n"
                            f"Opened by {row['opened_by']} at {row['opened_at']}")
                cols = st.columns(2)
                if stage_num < 5:
                    if cols[0].button(f"Advance to Next Stage", key=f"adv_{idx}"):
                        advance_arbitration(idx, row)
                        st.rerun()
                else:
                    if cols[0].button("⚖ Issue Binding Ruling", key=f"rule_{idx}"):
                        issue_ruling(idx, row, callsign)
                        st.success("Ruling issued and logged.")
                        st.rerun()

with tab_log:
    st.write("Every participant's moves, most recent first. This is the async multiplayer view — refresh to see others' activity.")
    df = load_log()
    if df.empty:
        st.info("No moves logged yet.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
