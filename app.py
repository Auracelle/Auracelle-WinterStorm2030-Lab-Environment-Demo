import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="WinterStorm2030", layout="wide")

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

DEFAULT_DATA = {
    "state": {"turn": 1, "cap_gap": 64, "concession_modifier": 0, "narrative_modifier": 0,
              "doctrine": "rus", "scenario_name": "", "scenario_desc": "", "treaty_flag": False, "win_win_active": False},
    "log": [],
    "arbitration": []
}

# ══════════════════════════════════════════════════════════
# JSONBIN.IO — shared, persistent state (this is what makes async multiplayer work)
# One JSON document, one API key. No SQL, no schema, no service-account file.
# ══════════════════════════════════════════════════════════
def _bin_url():
    return f"https://api.jsonbin.io/v3/b/{st.secrets['jsonbin']['bin_id']}"

def _headers():
    return {"X-Master-Key": st.secrets["jsonbin"]["master_key"], "Content-Type": "application/json"}

def load_all():
    resp = requests.get(f"{_bin_url()}/latest", headers=_headers(), timeout=10)
    resp.raise_for_status()
    data = resp.json()["record"]
    # backfill any missing top-level keys so an incomplete starter bin doesn't break the app
    for k, v in DEFAULT_DATA.items():
        if k not in data:
            data[k] = v
    return data

def save_all(data):
    resp = requests.put(_bin_url(), headers=_headers(), json=data, timeout=10)
    resp.raise_for_status()

def load_state():
    return load_all()["state"]

def save_state(state):
    data = load_all()
    data["state"] = state
    save_all(data)

def append_log(turn, callsign, actor, move_type, source, detail, cap_gap_delta):
    data = load_all()
    data["log"].append({
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "turn": turn, "callsign": callsign,
        "actor": actor, "move_type": move_type, "source": source, "detail": detail, "cap_gap_delta": cap_gap_delta
    })
    save_all(data)

def load_log():
    log = load_all()["log"]
    if not log:
        return pd.DataFrame(columns=["ts", "turn", "callsign", "actor", "move_type", "source", "detail", "cap_gap_delta"])
    return pd.DataFrame(list(reversed(log)))

def load_arbitration():
    arb = load_all()["arbitration"]
    if not arb:
        return pd.DataFrame(columns=["id", "case_id", "status", "violation", "asset", "stage", "opened_by", "opened_at"])
    return pd.DataFrame(arb)

def open_arbitration(violation, asset, callsign):
    data = load_all()
    next_id = max([c["id"] for c in data["arbitration"]], default=0) + 1
    data["arbitration"].append({
        "id": next_id, "case_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "status": "OPEN", "violation": violation, "asset": asset, "stage": 1,
        "opened_by": callsign, "opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_all(data)

def update_arbitration(case_row_id, fields):
    data = load_all()
    for c in data["arbitration"]:
        if c["id"] == case_row_id:
            c.update(fields)
    save_all(data)

# ══════════════════════════════════════════════════════════
# GAME LOGIC
# ══════════════════════════════════════════════════════════
def recompute_cap_gap(state):
    gap = 50 + int(state.get("concession_modifier", 0)) + int(state.get("narrative_modifier", 0))
    gap = max(0, min(100, gap))
    state["cap_gap"] = gap
    treaty = bool(state.get("treaty_flag", False))
    state["win_win_active"] = bool(gap < 45 and treaty)
    return state

def trigger_concession(actor, ctype, desc, callsign, is_red):
    state = load_state()
    type_delta = {"Access": 4, "Resource": 3, "Narrative-Legal": 2}
    delta = type_delta.get(ctype, 3)
    mod = int(state.get("concession_modifier", 0)) + (delta if is_red else -delta)
    state["concession_modifier"] = max(-20, min(20, mod))
    if ctype == "Narrative-Legal" and not is_red:
        state["treaty_flag"] = True
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

def advance_arbitration(row):
    new_stage = int(row["stage"]) + 1
    update_arbitration(row["id"], {"stage": new_stage})
    state = load_state()
    if new_stage == 3:
        state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) - 1))
    elif new_stage == 2:
        state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) + 1))
    state = recompute_cap_gap(state)
    save_state(state)

def issue_ruling(row, callsign):
    rulings = [
        {"ruling": "FOR BLUE", "delta": -6, "summary": "The Tribunal finds the violation substantiated. The responsible party shall cease the conduct and provide notification assurances going forward."},
        {"ruling": "SPLIT", "delta": -3, "summary": "The Tribunal finds the violation substantiated in part. Continuity of operations is affirmed; both parties shall provide notification going forward."},
        {"ruling": "FOR RED", "delta": 2, "summary": "The Tribunal finds insufficient evidence to substantiate the claim as framed. Continuity of operations affirmed without further remedy."},
    ]
    result = random.choice(rulings)
    state = load_state()
    state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) + result["delta"]))
    state["treaty_flag"] = True
    state = recompute_cap_gap(state)
    save_state(state)
    update_arbitration(row["id"], {"status": f"CLOSED — {result['ruling']}"})
    append_log(state["turn"], "Arbitration Tribunal", f"{row['violation']} vs {row['asset']}",
               f"BINDING RULING — {result['ruling']}", "ARBITRATION", result["summary"], result["delta"])

# ══════════════════════════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════════════════════════
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🧊 WinterStorm2030")
    st.subheader("NATO STO SAS-219 — High North Scenarios for Wargaming & Analysis")

    with st.form("login_form"):
        callsign_input = st.text_input("Callsign")
        access_code = st.text_input("Access Code", type="password")

        st.markdown("#### 🎯 Purpose")
        st.info(
            "A governance capacity instrument, not a combat simulator. WinterStorm2030 tracks a "
            "live NATO Capability Gap as NATO/Nordic actors and adversaries (Russia, China) trade "
            "concessions, narratives, and grey-zone moves across the High North — below the "
            "threshold of open conflict."
        )
        st.markdown("**🧭 This Session Supports:**")
        st.markdown('''
        1️⃣ Asynchronous play — participants take turns on their own schedule
        2️⃣ A shared, persistent move log every participant can see
        3️⃣ Concession Engine — Access / Resource / Narrative-Legal
        4️⃣ Agentic AI Red Team moves, tied to an active adversary doctrine
        5️⃣ Arbitration Track — Boundary Waters / Columbia River / Canterbury model
        6️⃣ Live NATO Capability Gap composite
        ''')
        submit = st.form_submit_button("🚀 Launch WinterStorm2030")

    if submit:
        if access_code == "WinterStorm2030!":
            st.session_state["authenticated"] = True
            st.session_state["callsign"] = callsign_input or "PARTICIPANT"
            st.rerun()
        else:
            st.error("❌ Access Denied — Credentials Not Recognized")
    st.stop()

# ══════════════════════════════════════════════════════════
# UI — only reached once authenticated
# ══════════════════════════════════════════════════════════
callsign = st.session_state.get("callsign", "PARTICIPANT")

live_mode = st.toggle("🔴 Live Mode — auto-refresh every 15s (for a facilitated synchronous session)", value=False)
if live_mode:
    st_autorefresh(interval=15000, key="live_refresh_tick")
    st.caption("Live Mode is on — this page refreshes itself every 15 seconds. Turn it off for async solo play to avoid unnecessary requests.")

state = load_state()

st.markdown(f"### 🧊 WinterStorm2030 &nbsp;·&nbsp; Logged in as **{callsign}**")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Turn", state["turn"])
c2.metric("NATO Capability Gap", f"{state['cap_gap']}%")
c3.metric("Active Doctrine", DOCTRINE_LABELS.get(state.get("doctrine", "rus"), "—"))
c4.metric("Win-Win", "🌟 YES" if state.get("win_win_active") else "No")

colA, colB, colC = st.columns([1, 1, 2])
with colA:
    if st.button("🔄 Refresh Shared State"):
        st.rerun()
with colB:
    if st.button("⏩ End Turn (generate Red Team move)"):
        state, move = end_turn(callsign)
        st.success(f"Turn {state['turn']} — {move['tag']}: {move['title']}")
        st.rerun()
with colC:
    if st.button("🚪 Log Out"):
        st.session_state["authenticated"] = False
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
        for _, row in open_cases.iterrows():
            with st.container(border=True):
                stage_num = int(row["stage"])
                st.markdown(f"**{row['violation']}** vs **{row['asset']}** — Stage {stage_num}: *{ARB_STAGES[stage_num-1]}*  \n"
                            f"Opened by {row['opened_by']} at {row['opened_at']}")
                cols = st.columns(2)
                if stage_num < 5:
                    if cols[0].button("Advance to Next Stage", key=f"adv_{row['id']}"):
                        advance_arbitration(row)
                        st.rerun()
                else:
                    if cols[0].button("⚖ Issue Binding Ruling", key=f"rule_{row['id']}"):
                        issue_ruling(row, callsign)
                        st.success("Ruling issued and logged.")
                        st.rerun()

with tab_log:
    st.write("Every participant's moves, most recent first. This is the async multiplayer view — refresh to see others' activity.")
    df = load_log()
    if df.empty:
        st.info("No moves logged yet.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
