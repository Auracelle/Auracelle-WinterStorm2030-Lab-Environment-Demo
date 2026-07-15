import streamlit as st
import pandas as pd
import requests
import html
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="WinterStorm2030 | High North Governance Wargame",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Rajdhani:wght@500;600;700&display=swap');
:root{--cyan:#55e5de;--cyan2:#9bf6f0;--amber:#ffc867;--red:#ff727f;--green:#7ee2a8;--text:#edf7fa;--muted:#9eb6c2;--line:rgba(96,204,222,.18);--line2:rgba(87,229,222,.52)}
html,body,[class*="css"]{font-family:'Inter',sans-serif}.stApp{color:var(--text);background:radial-gradient(circle at 78% 8%,rgba(21,118,146,.26),transparent 29%),radial-gradient(circle at 18% 20%,rgba(31,80,126,.22),transparent 28%),linear-gradient(145deg,#020a11 0%,#061622 45%,#0a2230 100%)}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(106,212,225,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(106,212,225,.028) 1px,transparent 1px);background-size:42px 42px}.block-container{max-width:1540px;padding-top:1.3rem;padding-bottom:3rem;position:relative}header[data-testid="stHeader"]{background:transparent}#MainMenu,footer{visibility:hidden}
h1,h2,h3,h4{font-family:'Rajdhani',sans-serif;color:var(--text)}
.ws-hero{position:relative;overflow:hidden;border:1px solid var(--line2);border-radius:22px;padding:1.35rem 1.55rem 1.25rem;margin:.2rem 0 1rem;background:linear-gradient(115deg,rgba(8,31,47,.96),rgba(5,22,34,.88));box-shadow:0 18px 55px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.04)}.ws-hero:after{content:"";position:absolute;width:360px;height:360px;right:-95px;top:-190px;border-radius:50%;border:1px solid rgba(85,229,222,.22);box-shadow:0 0 90px rgba(85,229,222,.12),inset 0 0 70px rgba(85,229,222,.06)}
.ws-kicker{color:var(--cyan);font-size:.76rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase}.ws-title{font-family:'Rajdhani',sans-serif;font-size:clamp(2rem,4vw,3.5rem);line-height:.95;font-weight:700;margin:.22rem 0 .35rem}.ws-subtitle{color:var(--muted);font-size:.96rem;max-width:970px}.ws-badges{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.8rem}.ws-badge{padding:.32rem .62rem;border:1px solid rgba(85,229,222,.25);border-radius:999px;background:rgba(85,229,222,.075);color:#c8fffb;font-size:.72rem;font-weight:650;letter-spacing:.04em}.ws-section-label{margin:.35rem 0 .7rem;color:var(--cyan);font-size:.75rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}.ws-callout{border:1px solid var(--line);border-left:3px solid var(--cyan);border-radius:12px;padding:.9rem 1rem;background:rgba(6,28,42,.62);color:var(--muted)}.ws-status{display:inline-flex;align-items:center;gap:.42rem;font-size:.73rem;color:var(--muted)}.ws-dot{width:8px;height:8px;border-radius:50%;display:inline-block;background:var(--green);box-shadow:0 0 12px var(--green)}.ws-risk-low{color:var(--green)}.ws-risk-med{color:var(--amber)}.ws-risk-high{color:var(--red)}
div[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(11,37,54,.92),rgba(6,24,37,.88));border:1px solid var(--line);border-radius:16px;padding:1rem 1.05rem;min-height:118px;box-shadow:0 12px 26px rgba(0,0,0,.2),inset 0 1px 0 rgba(255,255,255,.03)}div[data-testid="stMetricLabel"]{color:var(--muted);font-size:.74rem;text-transform:uppercase;letter-spacing:.09em;font-weight:700}div[data-testid="stMetricValue"]{color:var(--cyan2);font-family:'Rajdhani',sans-serif;font-weight:700;font-size:2rem}
.stButton>button,.stFormSubmitButton>button{min-height:2.9rem;background:linear-gradient(135deg,#59ece3,#25bfb8)!important;color:#032024!important;font-weight:800!important;border:1px solid rgba(175,255,250,.65)!important;border-radius:10px!important;padding:.7rem 1.15rem!important;position:relative!important;top:0!important;box-shadow:0 4px 0 #12867e,0 4px 8px 2px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.45)!important;transition:top .08s ease,box-shadow .08s ease,filter .16s ease!important}.stButton>button:hover,.stFormSubmitButton>button:hover{filter:brightness(1.08)}.stButton>button:active,.stFormSubmitButton>button:active{top:4px!important;box-shadow:0 0 0 #12867e,0 2px 4px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.45)!important}
div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{background:rgba(5,23,35,.88)!important;border-color:rgba(109,199,216,.28)!important;border-radius:10px!important}input,textarea{color:var(--text)!important}.stTextInput label,.stTextArea label,.stSelectbox label,.stRadio label{color:var(--muted)!important;font-weight:650!important}
.stTabs [data-baseweb="tab-list"]{gap:.4rem;padding:.45rem;border:1px solid var(--line);border-radius:15px;background:rgba(4,18,29,.72);overflow-x:auto}.stTabs [data-baseweb="tab"]{height:3.5rem;border-radius:10px;padding:0 1.3rem;color:var(--muted);font-weight:700;font-size:1rem}.stTabs [aria-selected="true"]{background:rgba(85,229,222,.12)!important;color:var(--cyan2)!important}.stTabs [data-baseweb="tab-highlight"]{background-color:var(--cyan)}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;border-radius:14px!important;background:rgba(7,27,41,.55)}div[data-testid="stExpander"]{border:1px solid var(--line);border-radius:12px;background:rgba(7,26,39,.56)}div[data-testid="stAlert"]{border-radius:12px;border-width:1px}[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}[data-testid="stDataFrame"] *{font-size:.88rem}hr{border-color:rgba(95,179,196,.18)!important}.stProgress>div>div>div>div{background:linear-gradient(90deg,#4edfd7,#ffc867,#ff727f)}.stProgress>div>div{background:rgba(138,199,211,.13)}
.ws-feature-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;margin:.75rem 0 .2rem}.ws-feature{padding:.72rem .78rem;border:1px solid var(--line);border-radius:11px;background:rgba(13,42,57,.5);color:var(--muted);font-size:.8rem}.ws-feature strong{color:var(--text);display:block;margin-bottom:.18rem}@media(max-width:900px){.block-container{padding-left:.9rem;padding-right:.9rem}.ws-feature-grid{grid-template-columns:1fr}.ws-title{font-size:2.35rem}}
section[data-testid="stSidebar"]{background:linear-gradient(160deg,#050f18,#0a1e2c)!important;border-right:1px solid var(--line2)}section[data-testid="stSidebar"] .block-container{padding-top:1.2rem}
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

COGWAR_ASSESSMENTS = {
    "rus": {
        "intent": 78, "autonomy": 82, "interaction": 61, "governance": 74,
        "analysis": "Consistent with Russia's narrative-first doctrine: high-intent content targeting Nordic alliance solidarity via legal/sovereignty ambiguity, amplified through low-attribution channels.",
        "blue_response": "Joint Nordic attribution statement recommended within T+4hrs to blunt narrative traction."
    },
    "prc": {
        "intent": 64, "autonomy": 71, "interaction": 69, "governance": 58,
        "analysis": "Consistent with China's platform-first doctrine: lower overt intent, higher reliance on infrastructure/data leverage and long-horizon economic access rather than direct narrative attack.",
        "blue_response": "Monitor data-sovereignty and infrastructure-access terms attached to any cooperative offers before accepting."
    },
    "hybrid": {
        "intent": 85, "autonomy": 80, "interaction": 74, "governance": 80,
        "analysis": "Compound signature: narrative and platform pressure arriving together, designed to saturate Blue Team attention across more than one domain at once.",
        "blue_response": "Prioritize triage — resolve the highest Cap Gap domain impact first rather than responding to both fronts equally."
    }
}

WASHINGTON_TREATY_ARTICLES = [
    {"article": "Article 1", "summary": "Parties settle disputes by peaceful means; refrain from the threat or use of force."},
    {"article": "Article 2", "summary": "Parties contribute to peaceful/friendly international relations; economic collaboration."},
    {"article": "Article 3", "summary": "Self-help and mutual aid — maintain and develop individual/collective capacity to resist armed attack."},
    {"article": "Article 4", "summary": "Consultation whenever territorial integrity, political independence, or security of any Party is threatened."},
    {"article": "Article 5", "summary": "Collective defense — an armed attack against one is an attack against all."},
    {"article": "Article 6", "summary": "Defines the geographic scope of Articles 5/6 (North America, Europe, North Atlantic area)."},
    {"article": "Article 7", "summary": "Does not affect, and shall not be interpreted as affecting, UN Charter rights/obligations."},
    {"article": "Article 8", "summary": "Parties will not enter international engagements conflicting with this Treaty."},
    {"article": "Article 9", "summary": "Establishes the North Atlantic Council and its subsidiary bodies."},
    {"article": "Article 10", "summary": "Accession — any other European state may be invited to accede."},
    {"article": "Article 11", "summary": "Ratification in accordance with constitutional processes."},
    {"article": "Article 12", "summary": "After 10 years, Parties may consult on revising the Treaty."},
    {"article": "Article 13", "summary": "After 20 years, a Party may withdraw with one year's notice."},
    {"article": "Article 14", "summary": "Deposit of the Treaty; certified copies to signatories."},
]

PRECEDENT_LIBRARY = [
    {"treaty": "Boundary Waters Treaty (1909, US-Canada)", "focus": "Canals, dams, diversions, navigation, hydropower",
     "why": "Standing International Joint Commission catches disputes before they become political crises. Best model for a standing bilateral grey-zone incident body."},
    {"treaty": "Columbia River Treaty (1961, US-Canada)", "focus": "Dams, flood control, hydropower",
     "why": "Permanent Engineering Board supplies facts; short deadline; then compulsory binding arbitration if unresolved."},
    {"treaty": "Treaty of Canterbury (1986, UK-France)", "focus": "Channel Tunnel",
     "why": "Continuous joint supervision of one specific strategic asset, plus treaty-based arbitration rules."},
    {"treaty": "Treaty of Peace and Friendship (1984, Argentina-Chile)", "focus": "Beagle Channel, southern straits, navigation",
     "why": "Settled a near-war over islands/channels; detailed conciliation-and-arbitration annex. High value for contested access and de-escalation design."},
    {"treaty": "Convention of Mannheim (1868)", "focus": "Rhine navigation, ports, inland waterway rules",
     "why": "Standing multistate navigation regime converting recurring friction into technical decisions rather than sovereignty crises."},
    {"treaty": "Indus Waters Treaty (1960, India-Pakistan)", "focus": "Dams, hydropower, river infrastructure",
     "why": "Canonical ladder: Permanent Commission -> Neutral Expert -> ad hoc Court of Arbitration. Has endured wars, though currently contested."},
    {"treaty": "UNCLOS (1982), Part XV / Annex VII", "focus": "Straits, maritime access, offshore infrastructure",
     "why": "Global fallback: Annex VII arbitration where other settlement routes fail. Best as a legal backstop beneath a tailored regional agreement."},
    {"treaty": "Israel-Jordan Peace Treaty (1994)", "focus": "Shared rivers, diversions, water infrastructure, border crossings",
     "why": "Joint water committee, prior-notification duty, data exchange. Shows how to manage routine violations before they become security incidents."},
    {"treaty": "Mekong Agreement (1995)", "focus": "River development, dams, navigation",
     "why": "Lower-intensity model: disputes go through the Mekong River Commission first. Better for confidence-building than coercive enforcement."},
    {"treaty": "Energy Charter Treaty (1994)", "focus": "Pipelines, grids, cross-border energy transit",
     "why": "Strongest multilateral pipeline analogue: expedited transit conciliation plus inter-state arbitration. Mixed record — borrow the mechanics, not the deterrent claim."},
]
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
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
    "calib_log": [],
    "govlab_docs": []
}

def capability_posture(gap):
    """Return a human-readable readiness posture for the composite gap."""
    if gap < 35:
        return "RESILIENT", "ws-risk-low"
    if gap < 55:
        return "CONTESTED", "ws-risk-med"
    if gap < 75:
        return "ELEVATED", "ws-risk-high"
    return "CRITICAL", "ws-risk-high"

def styled_actor_table():
    df = pd.DataFrame(ACTOR_BASELINES).rename(columns={
        "actor": "Actor", "g_gwc": "G-GWC", "iic": "IIC", "asi": "ASI",
        "esi": "ESI", "cd": "CD", "exposure": "Exposure",
        "concession": "Concession Status", "seam": "Primary Seam"
    })
    return df.style.map(
        lambda v: "color:#ff727f;font-weight:700" if v in {"HIGH", "CRITICAL", "VULNERABLE"}
        else ("color:#ffc867;font-weight:700" if v == "MEDIUM" else "color:#7ee2a8;font-weight:700"),
        subset=["Exposure", "Concession Status"]
    ).format({"G-GWC": "{:.1f}"})

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
    # backfill any missing top-level keys so an incomplete/older starter bin doesn't break the app
    for k, v in DEFAULT_DATA.items():
        if k not in data:
            data[k] = v
    # also backfill missing keys *inside* state -- older bins were saved before fields like
    # "domains" existed, so state itself can be present but incomplete
    for k, v in DEFAULT_DATA["state"].items():
        if k not in data["state"]:
            data["state"][k] = v
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

def render_move_feed():
    st.markdown("<div class='ws-section-label'>📜 Shared Move Feed</div>", unsafe_allow_html=True)
    st.caption("Agentic AI moves in human-vs-AI play, or other participants' moves in human-vs-human play — always visible here, no matter which tab you're on.")
    raw_log = load_all()["log"]
    if not raw_log:
        st.info("No moves logged yet.")
        return
    source_colors = {"REAL": "#55e5de", "SIMULATED": "#ff727f", "ANALYST": "#ffc867", "ARBITRATION": "#c9a6f7"}
    items_html = ""
    for entry in reversed(raw_log):
        src = entry.get("source", "ANALYST")
        color = source_colors.get(src, "#9eb6c2")
        delta = entry.get("cap_gap_delta", 0)
        delta_str = f"{delta:+d}%" if delta else "±0%"
        detail = html.escape(str(entry.get("detail", "")))
        actor = html.escape(str(entry.get("actor", "")))
        move_type = html.escape(str(entry.get("move_type", "")))
        callsign_e = html.escape(str(entry.get("callsign", "")))
        items_html += f"""
        <div style="border:1px solid var(--line);border-left:3px solid {color};border-radius:10px;padding:.6rem .7rem;margin-bottom:.5rem;background:rgba(13,42,57,.45);">
          <div style="font-size:.68rem;color:var(--muted);letter-spacing:.03em;">Turn {entry.get('turn','?')} · {entry.get('ts','')} · {callsign_e}</div>
          <div style="margin:.2rem 0;"><span style="color:{color};font-weight:700;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;">{src}</span><br>
            <strong style="color:var(--text);">{actor}</strong>
            <span style="color:var(--muted);"> — {move_type}</span></div>
          <div style="color:var(--muted);font-size:.82rem;">{detail}</div>
          <div style="font-size:.72rem;color:{'#ff727f' if delta>0 else '#7ee2a8' if delta<0 else 'var(--muted)'};margin-top:.2rem;">Cap Gap impact: {delta_str}</div>
        </div>"""
    st.markdown(f'<div style="max-height:78vh;overflow-y:auto;padding-right:.3rem;">{items_html}</div>', unsafe_allow_html=True)

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

def load_govlab_docs():
    docs = load_all()["govlab_docs"]
    return list(reversed(docs))

def append_govlab_doc(doc_record):
    data = load_all()
    data["govlab_docs"].append(doc_record)
    save_all(data)

# ══════════════════════════════════════════════════════════
# GOVERNANCE LAB — document scoring engine
# Rules-based (keyword/overlap) scoring against NATO doctrine language and the live
# session's own generated evidence. Explicitly NOT an LLM call — same security posture
# as everything else in this deployment. Labeled as indicative, not legal analysis.
# ══════════════════════════════════════════════════════════
def score_document(doc_text, doc_title, callsign):
    text_lower = doc_text.lower()

    # 1. Washington Treaty article relevance -- keyword overlap per article
    article_matches = []
    for art in WASHINGTON_TREATY_ARTICLES:
        keywords = [w.strip(".,()").lower() for w in art["summary"].replace("/", " ").split() if len(w) > 5]
        hits = sum(1 for kw in set(keywords) if kw in text_lower)
        if hits > 0:
            article_matches.append({"article": art["article"], "summary": art["summary"], "keyword_hits": hits})
    article_matches.sort(key=lambda x: -x["keyword_hits"])

    # 2. Grey-zone violation category coverage
    violation_hits = {}
    for v in VIOLATION_TYPES:
        terms = v.lower().replace("-", " ").split()
        count = sum(text_lower.count(t) for t in terms if len(t) > 4)
        violation_hits[v] = count
    covered_violations = [v for v, c in violation_hits.items() if c > 0]

    # 3. Precedent library alignment -- which comparative treaties share vocabulary with this document
    precedent_matches = []
    for p in PRECEDENT_LIBRARY:
        focus_words = [w.strip(",.()").lower() for w in p["focus"].split() if len(w) > 5]
        hits = sum(1 for w in set(focus_words) if w in text_lower)
        if hits > 0:
            precedent_matches.append({"treaty": p["treaty"], "hits": hits})
    precedent_matches.sort(key=lambda x: -x["hits"])

    # 4. Session relevance -- overlap with real events already tagged into the Article 4 Stress Test Log
    a4_log = load_all()["article4_log"]
    session_hits = 0
    for e in a4_log:
        title_words = [w.strip(".,()").lower() for w in e.get("title", "").split() if len(w) > 5]
        session_hits += sum(1 for w in set(title_words) if w in text_lower)

    # 5. Composite indicative score (0-100) -- NOT a legal or AI judgment, purely lexical overlap
    fit_score = min(100, len(article_matches) * 6 + len(covered_violations) * 8 + len(precedent_matches) * 5 + min(session_hits, 10) * 2)

    result = {
        "title": doc_title, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "uploaded_by": callsign,
        "excerpt": doc_text[:220], "fit_score": fit_score,
        "article_matches": article_matches[:5], "covered_violations": covered_violations,
        "precedent_matches": precedent_matches[:3], "session_hits": session_hits,
    }
    append_govlab_doc(result)
    return result

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

def run_cogwar_analysis(doctrine, narrative_text, callsign):
    state = load_state()
    state["doctrine"] = doctrine
    assessment = COGWAR_ASSESSMENTS.get(doctrine, COGWAR_ASSESSMENTS["rus"])
    mod = int(state.get("narrative_modifier", 0)) + round((assessment["governance"] - 50) / 6)
    state["narrative_modifier"] = max(-15, min(15, mod))
    state = recompute_cap_gap(state)
    state["turn"] = int(state["turn"]) + 1
    save_state(state)
    append_log(state["turn"], callsign, DOCTRINE_LABELS.get(doctrine, doctrine),
               "COGNITIVE WARFARE ANALYSIS", "SIMULATED",
               f"Narrative: \"{narrative_text[:120]}\" — {assessment['analysis']}", 0)
    return state, assessment

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
    st.markdown("""
    <div class="ws-hero">
      <div class="ws-kicker">Auracelle AI Governance Labs · High North Decision Environment</div>
      <div class="ws-title">WINTERSTORM<span style="color:#55e5de">2030</span></div>
      <div class="ws-subtitle">An asynchronous governance wargame for stress-testing NATO and Nordic capacity under grey-zone pressure—before strategic seams become operational failures.</div>
      <div class="ws-badges"><span class="ws-badge">AGENTIC AI RED TEAM</span><span class="ws-badge">CONTESTED NEGOTIATION TABLE</span><span class="ws-badge">ASYNCHRONOUS MULTIPLAYER</span><span class="ws-badge">CAPABILITY-GAP ANALYTICS</span></div>
    </div>
    <div class="ws-feature-grid">
      <div class="ws-feature"><strong>Strategic Purpose</strong>Test governance capacity below the threshold of open conflict.</div>
      <div class="ws-feature"><strong>Decision Mechanics</strong>Trade concessions, counter narratives, close gaps, and escalate disputes.</div>
      <div class="ws-feature"><strong>Shared Environment</strong>Persistent state and move history support distributed play over time.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        callsign_input = st.text_input("Callsign")
        access_code = st.text_input("Access Code", type="password")

        st.markdown("<div class='ws-section-label'>Secure Participant Access</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='ws-callout'><strong>Governance capacity instrument</strong> — not a combat simulator. "
            "WinterStorm2030 measures how policy, institutional capacity, alliance cohesion, concessions, "
            "narratives, and grey-zone actions alter the live NATO Capability Gap.</div>",
            unsafe_allow_html=True,
        )
        st.caption("Shared persistent state · Concession Engine · Agentic AI Red Team · arbitration ladder · live composite scoring")
        submit = st.form_submit_button("🚀 Launch WinterStorm2030")

    if submit:
        if access_code == "WinterStorm2030!":
            st.session_state["authenticated"] = True
            st.session_state["callsign"] = callsign_input or "PARTICIPANT"
            st.rerun()
        else:
            st.error("Access denied — verify the session access code and try again.")
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
posture, posture_class = capability_posture(state["cap_gap"])
scenario_label = state.get("scenario_name") or "Scenario awaiting configuration"

with st.sidebar:
    render_move_feed()

st.markdown(f"""
<div class="ws-hero">
  <div class="ws-kicker">NATO STO SAS-219 · High North Scenarios for Wargaming & Analysis</div>
  <div class="ws-title" style="font-size:2.7rem">WINTERSTORM<span style="color:#55e5de">2030</span></div>
  <div class="ws-subtitle"><strong style="color:#edf7fa">{scenario_label}</strong><br>Governance capacity · grey-zone competition · strategic concession analysis · asynchronous decision-testing</div>
  <div class="ws-badges"><span class="ws-badge">CALLSIGN: {callsign.upper()}</span><span class="ws-badge">TURN {state['turn']}</span><span class="ws-badge">SHARED STATE ACTIVE</span><span class="ws-badge">POSTURE: <span class="{posture_class}">{posture}</span></span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='ws-section-label'>Operational Status</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Turn", state["turn"], help="Shared simulation turn visible to all participants.")
c2.metric("NATO Capability Gap", f"{state['cap_gap']}%", help="Lower scores indicate a smaller capability gap and stronger collective resilience.")
c3.metric("Adversary Doctrine", DOCTRINE_LABELS.get(state.get("doctrine", "rus"), "—"), help="Doctrine governing Agentic AI Red Team behavior.")
c4.metric("Negotiated Stability", "ACHIEVED" if state.get("win_win_active") else "NOT YET", help="Achieved below a 45% gap with an active treaty/legal mechanism.")
st.markdown(f"<div class='ws-status'><span class='ws-dot'></span> Shared state online &nbsp;·&nbsp; Capability posture: <strong class='{posture_class}'>{posture}</strong> &nbsp;·&nbsp; Concession modifier: {state.get('concession_modifier',0):+d} &nbsp;·&nbsp; Narrative pressure: {state.get('narrative_modifier',0):+d}</div>", unsafe_allow_html=True)

colA, colB, colC = st.columns([1, 1, 2])
with colA:
    if st.button("🔄 Refresh Shared State"):
        st.rerun()
with colB:
    if st.button("⏩ End Turn (generate Red Team move)"):
        state, move = end_turn(callsign)
        st.success(f"Agentic AI Red Team move generated · Turn {state['turn']} · {move['tag']}: {move['title']}")
        st.rerun()
with colC:
    if st.button("🚪 Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

st.divider()

st.markdown("<div class='ws-section-label'>Decision Environment</div>", unsafe_allow_html=True)
mode = st.radio(
    "Mode",
    ["◆ Decision-Maker (breadth — act on it)", "◇ Decision-Support (full depth — including Arbitration Track)"],
    horizontal=True, index=1
)
is_dm = mode.startswith("◆")
if is_dm:
    st.caption("Decision-Maker mode: Scenario is read-only, and the Arbitration Track (a procedural escalation ladder) is hidden. "
               "Switch to Decision-Support to edit the scenario or work an arbitration case.")

tab_names = ["📋 Scenario Setup", "🧑‍🤝‍🧑 Actor Analysis", "🤝 Concession Engine", "📡 NATO Cap Gap",
             "📈 Dynamic Governance Tracking", "🛰️ OSINT Feed"]
if not is_dm:
    tab_names += ["🧠 Cognitive Warfare", "⚖ Arbitration Track", "📚 Governance Lab"]
tabs = st.tabs(tab_names)

tab_scenario, tab_actors, tab_concession, tab_capgap, tab_dgt, tab_osint = tabs[0], tabs[1], tabs[2], tabs[3], tabs[4], tabs[5]
if not is_dm:
    tab_cogwar = tabs[6]
    tab_arbitration = tabs[7]
    tab_govlab = tabs[8]

with tab_scenario:
    st.markdown("<div class='ws-section-label'>Scenario & Doctrine Configuration</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='ws-section-label'>Actor Readiness & Strategic Seam Analysis</div>", unsafe_allow_html=True)
    st.write("Arctic theatre baselines across governance capacity, institutional indicators, exposure, concession status, and each actor's primary strategic seam. Reference data; expert-panel validation is invited.")
    st.dataframe(styled_actor_table(), use_container_width=True, hide_index=True, height=320)

with tab_capgap:
    st.markdown("<div class='ws-section-label'>Collective Capability-Gap Monitor</div>", unsafe_allow_html=True)
    st.write(f"**Composite gap: {state['cap_gap']}% · Posture: {posture}** — calculated from five operational-governance domains, then adjusted by concession effects and adversarial narrative pressure. Lower is stronger.")
    st.progress(state["cap_gap"] / 100, text=f"{state['cap_gap']}% capability gap")
    domain_df = pd.DataFrame(state["domains"]).rename(columns={"name": "Capability Domain", "gap": "Gap %"})
    st.dataframe(domain_df.style.bar(subset=["Gap %"], vmin=0, vmax=100), use_container_width=True, hide_index=True, height=245)

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

with tab_dgt:
    st.markdown("<div class='ws-section-label'>Dynamic Governance Tracking</div>", unsafe_allow_html=True)
    st.write("Live-updating status view of the session's governance state — mirrors the HTML build's \"Live Tracking\" tab. "
             "Bayesian/Kalman-style continuous tracking is the framing; the values themselves are computed directly from live session data, not fitted models.")

    started = state.get("started_at")
    if started:
        elapsed = datetime.now() - datetime.strptime(started, "%Y-%m-%d %H:%M:%S")
        hh, rem = divmod(int(elapsed.total_seconds()), 3600)
        mm = rem // 60
        clock_str = f"T+{hh:02d}:{mm:02d}"
    else:
        clock_str = "T+00:00"

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.markdown("**Scenario Clock**")
        st.markdown(f"<div style='font-family:Rajdhani,sans-serif;font-size:3rem;font-weight:700;color:#55e5de;'>{clock_str}</div>", unsafe_allow_html=True)
        st.caption(f"Session started {started or 'unknown'} · Turn {state['turn']}")
    with dcol2:
        st.markdown("**Live Governance State**")
        iic_composite = round(sum(a["iic"] for a in ACTOR_BASELINES) / len(ACTOR_BASELINES))
        cd_composite = round(sum(a["cd"] for a in ACTOR_BASELINES) / len(ACTOR_BASELINES))
        st.write(f"IIC — Nordic Composite: **{iic_composite}/100**")
        st.progress(iic_composite / 100)
        st.write(f"CD — Cognitive Domain: **{cd_composite}/100**")
        st.progress(cd_composite / 100)
        st.write(f"NATO Cap Gap: **{state['cap_gap']}%**")
        st.progress(state["cap_gap"] / 100)

    st.divider()
    st.markdown("**Degradation / Event Log**")
    st.caption("Same underlying data as the Shared Move Feed, filtered to actions that moved the Cap Gap.")
    log_df = load_log()
    if not log_df.empty and "cap_gap_delta" in log_df.columns:
        moved = log_df[log_df["cap_gap_delta"] != 0]
        if moved.empty:
            st.info("No Cap-Gap-moving events yet.")
        else:
            st.dataframe(moved, use_container_width=True, hide_index=True)
    else:
        st.info("No events logged yet.")

with tab_osint:
    st.markdown("<div class='ws-section-label'>Open-Source Event Ingestion & Calibration</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='ws-section-label'>Concession Engine</div>", unsafe_allow_html=True)
    st.write("Model how access, resource, and narrative-legal concessions shift collective resilience. Every action is immediately written to the shared move log.")
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
    with tab_cogwar:
        st.markdown("<div class='ws-section-label'>Cognitive Warfare Assessment</div>", unsafe_allow_html=True)
        st.write("Doctrine-based assessment — no live LLM call, consistent with the security constraint on this deployment. "
                 "Running an analysis sets the session's active adversary doctrine and advances the turn.")
        cw_doctrine = st.selectbox("Doctrine to assess under", options=list(DOCTRINE_LABELS.keys()),
                                    format_func=lambda k: DOCTRINE_LABELS[k], key="cw_doctrine")
        narrative_text = st.text_area("Narrative or activity to assess", key="cw_narrative")
        if st.button("Run Cognitive Warfare Analysis"):
            state, assessment = run_cogwar_analysis(cw_doctrine, narrative_text or "No narrative provided", callsign)
            mcols = st.columns(4)
            mcols[0].metric("Intent", f"{assessment['intent']}/100")
            mcols[1].metric("Autonomy", f"{assessment['autonomy']}/100")
            mcols[2].metric("Interaction", f"{assessment['interaction']}/100")
            mcols[3].metric("Governance Pressure", f"{assessment['governance']}/100")
            st.info(f"**IAIG Assessment:** {assessment['analysis']}")
            st.success(f"**Blue Team Response:** {assessment['blue_response']}")
            st.caption(f"Turn advanced to {state['turn']} — Cap Gap now {state['cap_gap']}%.")

    with tab_arbitration:
        st.markdown("<div class='ws-section-label'>Arbitration & Strategic Continuity Track</div>", unsafe_allow_html=True)
        st.write("A standing procedural escalation ladder adapted from Boundary Waters, Columbia River, and Canterbury-type mechanisms — not a one-time trigger.")
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

    with tab_govlab:
        st.markdown("<div class='ws-section-label'>Governance Lab — Document Scoring Workspace</div>", unsafe_allow_html=True)
        st.write("Upload or paste a treaty, policy, or legal agreement (e.g. the Washington Naval Treaty) for assessment against NATO doctrine "
                 "and this session's own generated evidence. Scoring is rules-based lexical overlap — labeled indicative, not a legal or AI judgment.")
        st.warning("**SCOPE** — This is heuristic keyword/overlap scoring (an E-AGPO-HT-style indicative score), not a generative-AI legal analysis "
                   "or a substitute for expert review. No document text is sent anywhere — scoring runs locally against the reference tables below.")

        upload_mode = st.radio("Input method", ["Paste text", "Upload .txt file"], horizontal=True, key="govlab_input_mode")
        doc_title = st.text_input("Document title", placeholder="e.g. Washington Naval Treaty (1922)")
        doc_text = ""
        if upload_mode == "Paste text":
            doc_text = st.text_area("Paste document text", height=200, key="govlab_paste")
        else:
            uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
            if uploaded is not None:
                doc_text = uploaded.read().decode("utf-8", errors="ignore")
                st.caption(f"Loaded {len(doc_text)} characters from {uploaded.name}.")

        if st.button("Score Document"):
            if not doc_text.strip():
                st.error("Provide document text first — paste it in or upload a .txt file.")
            else:
                result = score_document(doc_text, doc_title or "Untitled document", callsign)
                st.success(f"Scored and logged — Governance Fit Score: {result['fit_score']}/100")
                st.rerun()

        st.divider()
        st.markdown("**Scored Documents**")
        docs = load_govlab_docs()
        if not docs:
            st.info("No documents scored yet.")
        else:
            for d in docs:
                with st.container(border=True):
                    st.markdown(f"**{d['title']}** — Fit Score: **{d['fit_score']}/100**  \n*Scored by {d['uploaded_by']} at {d['ts']}*")
                    st.caption(f"Excerpt: {d['excerpt']}…")
                    mcols = st.columns(3)
                    mcols[0].metric("Treaty Article Matches", len(d["article_matches"]))
                    mcols[1].metric("Violation Categories Covered", len(d["covered_violations"]))
                    mcols[2].metric("Session Evidence Overlap", d["session_hits"])
                    if d["article_matches"]:
                        st.caption("Top Washington Treaty article matches: " + ", ".join(f"{a['article']} ({a['keyword_hits']})" for a in d["article_matches"]))
                    if d["covered_violations"]:
                        st.caption("Grey-zone categories referenced: " + ", ".join(d["covered_violations"]))
                    if d["precedent_matches"]:
                        st.caption("Precedent library alignment: " + ", ".join(f"{p['treaty']} ({p['hits']})" for p in d["precedent_matches"]))

        st.divider()
        st.markdown("<div class='ws-section-label'>Reference Library</div>", unsafe_allow_html=True)
        st.caption("Static reference material the scoring above checks documents against — not live game state.")
        with st.expander("North Atlantic Treaty (the \"Washington Treaty,\" signed April 4, 1949) — all 14 Articles"):
            st.caption("Commonly called the Washington Treaty because it was signed in Washington, D.C. — same document that contains Articles 4 and 5, not a separate treaty.")
            st.dataframe(pd.DataFrame(WASHINGTON_TREATY_ARTICLES), use_container_width=True, hide_index=True)
        with st.expander("Precedent Library — grey-zone infrastructure & boundary dispute analogues"):
            for p in PRECEDENT_LIBRARY:
                st.markdown(f"**{p['treaty']}**")
                st.markdown(f"Infrastructure focus: {p['focus']}")
                st.markdown(f"Why it's a useful analogue: {p['why']}")
                st.markdown("---")
