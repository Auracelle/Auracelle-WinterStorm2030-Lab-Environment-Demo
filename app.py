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

DOMAIN_NAMES = ["Infrastructure & Stockpiles", "Industrial Capacity (Icebreakers)",
                "Command & Communications", "Undersea Surveillance", "Nordic Burden Sharing"]

ACTOR_BASELINES = [
    {"actor": "Finland", "g_gwc": 75.6, "iic": 76, "asi": 68, "esi": 72, "cd": 64, "exposure": "MEDIUM", "concession": "STABLE", "seam": "Article 5 commitment narratives"},
    {"actor": "Norway", "g_gwc": 74.8, "iic": 73, "asi": 65, "esi": 75, "cd": 61, "exposure": "MEDIUM", "concession": "STABLE", "seam": "Svalbard sovereignty"},
    {"actor": "Sweden", "g_gwc": 73.0, "iic": 74, "asi": 64, "esi": 71, "cd": 60, "exposure": "MEDIUM", "concession": "STABLE", "seam": "Neutrality reactivation"},
    {"actor": "Denmark/Greenland", "g_gwc": 68.7, "iic": 70, "asi": 58, "esi": 68, "cd": 55, "exposure": "HIGH", "concession": "CRITICAL", "seam": "US adversarial framing"},
    {"actor": "Iceland", "g_gwc": 59.3, "iic": 42, "asi": 56, "esi": 58, "cd": 38, "exposure": "CRITICAL", "concession": "VULNERABLE", "seam": "CD gap -44pts vs Russia"},
    {"actor": "Canada", "g_gwc": 71.2, "iic": 66, "asi": 62, "esi": 69, "cd": 63, "exposure": "MEDIUM", "concession": "STABLE", "seam": "Northwest Passage sovereignty — NORAD modernization"},
]

DEFAULT_DATA = {
    "state": {
        "turn": 1, "cap_gap": 64, "concession_modifier": 0, "narrative_modifier": 0,
        "doctrine": "rus", "scenario_name": "", "scenario_desc": "", "treaty_flag": False, "win_win_active": False,
        "domains": [
            {"name": DOMAIN_NAMES[0], "gap": 61},
            {"name": DOMAIN_NAMES[1], "gap": 70},
            {"name": DOMAIN_NAMES[2], "gap": 58},
            {"name": DOMAIN_NAMES[3], "gap": 72},
            {"name": DOMAIN_NAMES[4], "gap": 59},
        ],
    },
    "log": [],
    "arbitration": [],
    "article4_log": [],
    "calib_log": []
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

def load_article4_log():
    log = load_all()["article4_log"]
    return pd.DataFrame(list(reversed(log))) if log else pd.DataFrame(columns=["turn", "ts", "domain", "source", "title", "url"])

def append_article4(turn, domain_name, source, title, url=""):
    data = load_all()
    data["article4_log"].append({
        "turn": turn, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "domain": domain_name, "source": source, "title": title, "url": url
    })
    save_all(data)

def load_calib_log():
    log = load_all()["calib_log"]
    return pd.DataFrame(list(reversed(log))) if log else pd.DataFrame(columns=["ts", "violation", "title", "domain", "url"])

def append_calib(violation, title, domain, url=""):
    data = load_all()
    data["calib_log"].append({
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "violation": violation, "title": title, "domain": domain, "url": url
    })
    save_all(data)

# ══════════════════════════════════════════════════════════
# GAME LOGIC
# ══════════════════════════════════════════════════════════
def recompute_cap_gap(state):
    domains = state.get("domains", [])
    domain_avg = round(sum(d["gap"] for d in domains) / len(domains)) if domains else 50
    gap = domain_avg + int(state.get("concession_modifier", 0)) + int(state.get("narrative_modifier", 0))
    gap = max(0, min(100, gap))
    state["cap_gap"] = gap
    treaty = bool(state.get("treaty_flag", False))
    state["win_win_active"] = bool(gap < 45 and treaty)
    return state

def adjust_domain(domain_idx, delta, is_red, callsign):
    state = load_state()
    domains = state["domains"]
    domains[domain_idx]["gap"] = max(0, min(100, domains[domain_idx]["gap"] + (delta if is_red else -delta)))
    state = recompute_cap_gap(state)
    save_state(state)
    append_log(state["turn"], callsign, domains[domain_idx]["name"],
               "RED EXPLOIT" if is_red else "BLUE CLOSE", "ANALYST",
               f"{domains[domain_idx]['name']} {'+' if is_red else '-'}{delta}", delta if is_red else -delta)
    return state

def trigger_concession(actor, ctype, desc, callsign, is_red, source="ANALYST"):
    state = load_state()
    type_delta = {"Access": 4, "Resource": 3, "Narrative-Legal": 2}
    delta = type_delta.get(ctype, 3)
    mod = int(state.get("concession_modifier", 0)) + (delta if is_red else -delta)
    state["concession_modifier"] = max(-20, min(20, mod))
    if ctype == "Narrative-Legal" and not is_red:
        state["treaty_flag"] = True
    state = recompute_cap_gap(state)
    save_state(state)
    append_log(state["turn"], callsign, actor, f"CONCESSION — {ctype}", source, desc, delta if is_red else -delta)
    return state

# ══════════════════════════════════════════════════════════
# OSINT FEED — GDELT Project, no API key, no LLM call
# Server-side request from Streamlit, so no browser CORS concerns at all.
# ══════════════════════════════════════════════════════════
def fetch_osint(query, timespan):
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {"query": query, "mode": "artlist", "maxrecords": 15, "format": "json", "timespan": timespan}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        if not articles:
            raise ValueError("empty")
        return [{"title": a.get("title", ""), "domain": a.get("domain", ""), "seendate": a.get("seendate", ""),
                  "url": a.get("url", ""), "tone": a.get("tone")} for a in articles], True
    except Exception:
        fallback = {
            "arctic": [
                {"title": "Norway tracks unidentified vessel activity near Svalbard fishing protection zone", "domain": "highnorthnews.com", "seendate": "20260703T090000Z", "tone": -3.2, "url": ""},
                {"title": "NATO allies discuss undersea cable protection after Baltic incidents", "domain": "reuters.com", "seendate": "20260706T110000Z", "tone": -4.1, "url": ""},
                {"title": "China-flagged research vessel logged near Northern Sea Route", "domain": "thebarentsobserver.com", "seendate": "20260709T160000Z", "tone": -2.6, "url": ""},
            ],
            "hormuz": [
                {"title": "IRGC boards and briefly detains commercial tanker transiting Strait of Hormuz", "domain": "reuters.com", "seendate": "20260702T070000Z", "tone": -6.1, "url": ""},
                {"title": "GPS spoofing incidents reported by multiple vessels near Hormuz shipping lanes", "domain": "maritime-executive.com", "seendate": "20260704T120000Z", "tone": -4.4, "url": ""},
            ],
        }
        key = "hormuz" if "hormuz" in query.lower() else "arctic"
        return fallback[key], False

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

mode = st.radio(
    "Mode",
    ["◆ Decision-Maker (breadth — act on it)", "◇ Decision-Support (full depth — including Arbitration Track)"],
    horizontal=True, index=1
)
is_dm = mode.startswith("◆")
if is_dm:
    st.caption("Decision-Maker mode: Scenario is read-only, and the Arbitration Track (a procedural escalation ladder) is hidden. "
               "Switch to Decision-Support to edit the scenario or work an arbitration case.")

tab_names = ["📋 Scenario Setup", "🧑‍🤝‍🧑 Actor Analysis", "🤝 Concession Engine", "📡 NATO Cap Gap", "🛰️ OSINT Feed"]
if not is_dm:
    tab_names.append("⚖ Arbitration Track")
tab_names.append("📜 Shared Move Log")
tabs = st.tabs(tab_names)

tab_scenario, tab_actors, tab_concession, tab_capgap, tab_osint = tabs[0], tabs[1], tabs[2], tabs[3], tabs[4]
if not is_dm:
    tab_arbitration = tabs[5]
    tab_log = tabs[6]
else:
    tab_log = tabs[5]

with tab_scenario:
    if is_dm:
        st.write("Read-only in Decision-Maker mode. Switch to Decision-Support to edit.")
        st.markdown(f"**Scenario:** {state.get('scenario_name') or '_(not set)_'}")
        st.markdown(f"**Description:** {state.get('scenario_desc') or '_(not set)_'}")
        st.markdown(f"**Active Adversary Doctrine:** {DOCTRINE_LABELS.get(state.get('doctrine', 'rus'))}")
    else:
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

with tab_actors:
    st.write("Arctic theatre baselines — G-GWC, IIC, ASI, ESI, CD, exposure, concession status, and primary seam per actor. Reference data, panel validation invited.")
    st.dataframe(pd.DataFrame(ACTOR_BASELINES), use_container_width=True, hide_index=True)

with tab_capgap:
    st.write(f"**Overall NATO Capability Gap: {state['cap_gap']}%** — average of the five domains below, adjusted by the Concession Modifier and Narrative Pressure Modifier. Every tab writes to the same number.")
    st.progress(state["cap_gap"] / 100)
    domain_df = pd.DataFrame(state["domains"])
    st.dataframe(domain_df, use_container_width=True, hide_index=True)

    if is_dm:
        st.caption("Domain-level adjustment is Decision-Support depth tooling. Switch to Decision-Support to see or change what's behind this number.")
    else:
        st.markdown("**Adjust a domain**")
        dcols = st.columns(3)
        domain_idx = dcols[0].selectbox("Domain", options=range(len(DOMAIN_NAMES)), format_func=lambda i: DOMAIN_NAMES[i])
        adj_type = dcols[1].selectbox("Type", ["Blue — Close Gap", "Red — Widen Gap"])
        delta_val = dcols[2].selectbox("Delta", [3, 7, 12, 18])
        if st.button("Apply Domain Adjustment"):
            is_red = adj_type.startswith("Red")
            state = adjust_domain(domain_idx, delta_val, is_red, callsign)
            st.success(f"{'Widened' if is_red else 'Closed'} {DOMAIN_NAMES[domain_idx]} — Composite now {state['cap_gap']}%")
            st.rerun()

with tab_osint:
    st.write("Real event data from the GDELT Project — free, unclassified, no API key, no generative AI. A direct substitute for the Anthropic API where that can't be cleared.")
    ocols = st.columns(3)
    theatre = ocols[0].selectbox("Theatre", ["Arctic High North (live session)", "Strait of Hormuz (calibration baseline)"])
    is_hormuz = theatre.startswith("Strait")
    default_query = "Strait of Hormuz Iran IRGC tanker seizure" if is_hormuz else "Arctic Svalbard Greenland NATO Russia"
    timespan = ocols[1].selectbox("Window", ["1d", "3d", "7d", "30d"], index=2, format_func=lambda t: {"1d": "Last 24 hours", "3d": "Last 3 days", "7d": "Last 7 days", "30d": "Last 30 days"}[t])
    query = st.text_input("Search Terms", value=default_query)

    if is_hormuz:
        st.info("Hormuz events feed a standalone Calibration Log, not the live Arctic Cap Gap — data-rich theatre used to sanity-check the scoring model, kept separate so it can't quietly contaminate the Arctic session.")
    else:
        acols = st.columns(2)
        tag_actor = acols[0].selectbox("Actor (for Concession tagging)", ["Norway", "Denmark/Greenland", "Finland", "Iceland", "Canada", "United States", "Russia (Red)", "China (Red)"], index=6)
        tag_type = acols[1].selectbox("Concession Type", ["Access", "Resource", "Narrative-Legal"], index=2)

    if st.button("Pull Feed"):
        articles, was_live = fetch_osint(query, timespan)
        st.session_state["osint_articles"] = articles
        st.session_state["osint_live"] = was_live
        st.session_state["osint_hormuz"] = is_hormuz

    if "osint_articles" in st.session_state:
        status = "Live GDELT pull." if st.session_state.get("osint_live") else "GDELT pull unavailable — showing cached sample events so the workflow is still testable."
        st.caption(status)
        for i, a in enumerate(st.session_state["osint_articles"]):
            with st.container(border=True):
                tone = a.get("tone")
                tone_label = "" if tone is None else (" 🔴 negative" if tone < -2 else " 🟢 positive" if tone > 2 else " ⚪ neutral")
                st.markdown(f"**{a['title']}**{tone_label}  \n*{a.get('domain','')} — {str(a.get('seendate',''))[:8]}*")
                if a.get("url"):
                    st.caption(a["url"])
                if st.session_state.get("osint_hormuz"):
                    violation = st.selectbox("Grey-zone violation type", VIOLATION_TYPES, key=f"viol_{i}")
                    if st.button("→ Calibration Log", key=f"calib_{i}"):
                        append_calib(violation, a["title"], a.get("domain", ""), a.get("url", ""))
                        st.success("Tagged into the Hormuz Calibration Log.")
                        st.rerun()
                else:
                    bcols = st.columns(2)
                    if bcols[0].button("→ Concession", key=f"conc_{i}"):
                        is_red = "Red" in tag_actor
                        state = trigger_concession(tag_actor, tag_type, f"[OSINT: {a.get('domain','')}] {a['title']}", callsign, is_red, source="REAL")
                        st.success(f"Tagged as a real event — Cap Gap now {state['cap_gap']}%")
                        st.rerun()
                    if bcols[1].button("→ Article 4 Log", key=f"art4_{i}"):
                        append_article4(state["turn"], a.get("domain", ""), "REAL", a["title"], a.get("url", ""))
                        st.success("Tagged into the Article 4 Stress Test Log.")
                        st.rerun()

    st.divider()
    st.markdown(f"**Article 4 Stress Test Log**")
    st.warning("**KNOWN GAP** — A written legal rubric for what counts as \"below Article 4\" — ideally reviewed by outside eyes, not just this tool's tagging judgment — is still open, and is still the most important gap before WinterStorm2030's output can be called sound empirical evidence rather than illustrative analysis.")
    a4_df = load_article4_log()
    if a4_df.empty:
        st.info("No Article 4 events tagged yet.")
    else:
        st.dataframe(a4_df, use_container_width=True, hide_index=True)

    st.markdown(f"**Strait of Hormuz — Calibration Baseline**")
    st.caption("Standalone, non-scoring log — does not affect the live Arctic Cap Gap.")
    calib_df = load_calib_log()
    if calib_df.empty:
        st.info("No Hormuz calibration events tagged yet.")
    else:
        st.dataframe(calib_df, use_container_width=True, hide_index=True)

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

if not is_dm:
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
