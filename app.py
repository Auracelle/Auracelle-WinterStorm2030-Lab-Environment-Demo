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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@500;600;700&display=swap');
:root{
  --navy:#04111c;--navy2:#082033;--navy3:#0b2e43;--ice:#dffbff;--cyan:#7ae7f4;--cyan2:#bbfbff;
  --teal:#4fd0de;--amber:#ffd279;--red:#ff808d;--green:#8ce8b1;--muted:#9fb8c7;--steel:#6e8ea1;
  --line:rgba(122,231,244,.18);--line2:rgba(122,231,244,.45);--panel:rgba(6,24,36,.86);--panel2:rgba(10,34,50,.78);
}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{
  color:var(--ice);
  background:
    radial-gradient(circle at 12% 18%, rgba(80,170,210,.18), transparent 24%),
    radial-gradient(circle at 85% 12%, rgba(96,232,255,.15), transparent 23%),
    radial-gradient(circle at 72% 66%, rgba(42,94,148,.16), transparent 30%),
    linear-gradient(145deg,#01070d 0%, #03131f 42%, #082234 78%, #0d2f46 100%);
}
.stApp:before{
  content:"";position:fixed;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(160,232,244,.028) 1px, transparent 1px),
    linear-gradient(90deg, rgba(160,232,244,.028) 1px, transparent 1px);
  background-size:44px 44px;
}
.stApp:after{
  content:"";position:fixed;left:0;right:0;bottom:0;height:180px;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(196,241,255,.05) 46%,rgba(196,241,255,.08));
  clip-path:polygon(0 100%,12% 76%,20% 88%,33% 68%,45% 84%,58% 70%,70% 86%,82% 65%,92% 80%,100% 61%,100% 100%);
}
.block-container{max-width:1560px;padding-top:1.15rem;padding-bottom:3rem;position:relative}
header[data-testid="stHeader"]{background:transparent}#MainMenu,footer{visibility:hidden}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,rgba(5,18,29,.96),rgba(8,24,38,.96));border-right:1px solid var(--line)}
section[data-testid="stSidebar"] .block-container{padding-top:1rem}
h1,h2,h3,h4{font-family:'Rajdhani',sans-serif;color:var(--ice);letter-spacing:.01em}

.ws-hero,.ws-panel,.ws-callout-panel,.ws-brief,.ws-domain-card,.ws-mini-card,.ws-mode-note{
  position:relative;overflow:hidden;border:1px solid var(--line);border-radius:20px;background:linear-gradient(150deg,rgba(8,29,44,.94),rgba(5,20,32,.88));
  box-shadow:0 20px 48px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.04);
}
.ws-hero{padding:1.35rem 1.5rem 1.3rem;border-color:var(--line2);margin:.15rem 0 1rem}
.ws-hero:before,.ws-panel:before,.ws-brief:before,.ws-domain-card:before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(120deg,rgba(255,255,255,.035),transparent 26%,transparent 70%,rgba(122,231,244,.04));
}
.ws-hero:after{
  content:"";position:absolute;width:360px;height:360px;right:-90px;top:-190px;border-radius:50%;
  border:1px solid rgba(122,231,244,.22);box-shadow:0 0 95px rgba(122,231,244,.10), inset 0 0 60px rgba(122,231,244,.05);
}
.ws-kicker{color:var(--cyan);font-size:.74rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase}
.ws-title{font-family:'Rajdhani',sans-serif;font-size:clamp(2.2rem,4vw,3.85rem);line-height:.94;font-weight:700;margin:.24rem 0 .42rem}
.ws-subtitle{color:var(--muted);font-size:.97rem;max-width:960px;line-height:1.45}
.ws-badges{display:flex;gap:.48rem;flex-wrap:wrap;margin-top:.85rem}.ws-badge{padding:.34rem .68rem;border:1px solid rgba(122,231,244,.24);border-radius:999px;background:rgba(122,231,244,.085);color:#e2feff;font-size:.72rem;font-weight:700;letter-spacing:.05em}
.ws-section-label{margin:.35rem 0 .72rem;color:var(--cyan);font-size:.75rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase}
.ws-status{display:inline-flex;align-items:center;gap:.42rem;flex-wrap:wrap;font-size:.74rem;color:var(--muted)}
.ws-dot{width:8px;height:8px;border-radius:50%;display:inline-block;background:var(--green);box-shadow:0 0 12px var(--green)}
.ws-risk-low{color:var(--green)}.ws-risk-med{color:var(--amber)}.ws-risk-high{color:var(--red)}
.ws-callout-panel{padding:1rem 1.05rem;border-left:3px solid var(--cyan);background:linear-gradient(145deg,rgba(6,28,42,.82),rgba(8,31,47,.66));color:var(--muted)}
.ws-panel{padding:1rem 1.05rem}
.ws-brief{padding:1.15rem 1.1rem;height:100%}
.ws-brief-title{font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;margin-bottom:.35rem}
.ws-brief-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem;margin-top:.75rem}
.ws-mini-card{padding:.78rem .82rem;border-radius:14px;background:linear-gradient(145deg,rgba(10,38,56,.92),rgba(8,26,39,.76));border:1px solid rgba(122,231,244,.14)}
.ws-mini-card small{display:block;color:var(--muted);font-size:.68rem;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.2rem}
.ws-mini-card strong{display:block;color:var(--cyan2);font-size:1.05rem;font-weight:700;line-height:1.2}
.ws-feature-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:.72rem 0 .2rem}
.ws-feature{padding:.84rem .82rem;border:1px solid var(--line);border-radius:14px;background:linear-gradient(145deg,rgba(11,38,53,.70),rgba(8,28,42,.52));color:var(--muted);font-size:.82rem}.ws-feature strong{color:var(--ice);display:block;margin-bottom:.24rem;font-weight:700}
.ws-domain-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.72rem;margin:.8rem 0 1rem}
.ws-domain-card{padding:.82rem .86rem;border-radius:16px;background:linear-gradient(145deg,rgba(9,34,49,.88),rgba(5,21,34,.88))}
.ws-domain-card .name{display:block;font-size:.78rem;color:var(--muted);min-height:2.35rem;line-height:1.3}
.ws-domain-card .gap{display:block;font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;color:var(--cyan2);line-height:1.05;margin:.2rem 0}
.ws-domain-card .tag{display:inline-block;padding:.24rem .48rem;border-radius:999px;font-size:.66rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.ws-domain-card.low .tag{background:rgba(140,232,177,.14);color:var(--green);border:1px solid rgba(140,232,177,.25)}
.ws-domain-card.med .tag{background:rgba(255,210,121,.14);color:var(--amber);border:1px solid rgba(255,210,121,.25)}
.ws-domain-card.high .tag{background:rgba(255,128,141,.14);color:var(--red);border:1px solid rgba(255,128,141,.25)}
.ws-chip-row{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.7rem}.ws-chip{padding:.32rem .56rem;border-radius:999px;border:1px solid var(--line);background:rgba(122,231,244,.07);color:var(--ice);font-size:.72rem;font-weight:700}
.ws-mode-note{padding:.85rem .95rem;border-radius:14px;background:linear-gradient(145deg,rgba(8,28,40,.76),rgba(5,19,29,.70));margin-bottom:.85rem}

/* Native Streamlit components */
div[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(11,37,54,.94),rgba(6,24,37,.88));border:1px solid var(--line);border-radius:18px;padding:1rem 1.05rem;min-height:120px;box-shadow:0 12px 26px rgba(0,0,0,.2),inset 0 1px 0 rgba(255,255,255,.03)}
div[data-testid="stMetricLabel"]{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.11em;font-weight:800}
div[data-testid="stMetricValue"]{color:var(--cyan2);font-family:'Rajdhani',sans-serif;font-weight:700;font-size:2rem}
.stButton>button,.stFormSubmitButton>button{min-height:2.75rem;background:linear-gradient(135deg,#82f0fb,#40bfd0)!important;color:#031d2a!important;font-weight:800!important;border:1px solid rgba(220,255,255,.74)!important;border-radius:11px!important;padding:.68rem 1rem!important;box-shadow:0 9px 22px rgba(12,174,165,.20),inset 0 1px 0 rgba(255,255,255,.45)!important;transition:.16s ease!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);filter:brightness(1.06);box-shadow:0 14px 30px rgba(12,174,165,.27)!important}
.stButton>button:active,.stFormSubmitButton>button:active{transform:translateY(1px)}
div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{background:rgba(5,23,35,.90)!important;border-color:rgba(109,199,216,.28)!important;border-radius:11px!important}input,textarea{color:var(--ice)!important}.stTextInput label,.stTextArea label,.stSelectbox label,.stRadio label,.stToggle label{color:var(--muted)!important;font-weight:700!important}
.stTabs [data-baseweb="tab-list"]{gap:.34rem;padding:.38rem;border:1px solid var(--line);border-radius:14px;background:rgba(4,18,29,.76);overflow-x:auto}.stTabs [data-baseweb="tab"]{height:2.8rem;border-radius:10px;padding:0 .95rem;color:var(--muted);font-weight:700}.stTabs [aria-selected="true"]{background:rgba(122,231,244,.12)!important;color:var(--cyan2)!important}.stTabs [data-baseweb="tab-highlight"]{background-color:var(--cyan)}
div[data-testid="stSegmentedControl"]{gap:.5rem;flex-wrap:wrap}
div[data-testid="stSegmentedControl"] label{border:1px solid var(--line)!important;border-radius:12px!important;background:rgba(9,33,49,.55)!important;padding:.65rem .9rem!important;min-height:2.6rem;transition:box-shadow .15s ease,border-color .15s ease,background .15s ease!important}
div[data-testid="stSegmentedControl"] label:hover{border-color:var(--cyan)!important}
div[data-testid="stSegmentedControl"] label[aria-checked="true"],div[data-testid="stSegmentedControl"] label[data-checked="true"]{border-color:var(--cyan)!important;background:rgba(122,231,244,.16)!important;box-shadow:0 0 0 1px var(--cyan),0 0 18px rgba(122,231,244,.55)!important}
div[data-testid="stSegmentedControl"] label[aria-checked="true"] p,div[data-testid="stSegmentedControl"] label[data-checked="true"] p{color:var(--cyan2)!important;font-weight:700!important}
.st-key-vector_box_wrap div[data-testid="stSegmentedControl"]{gap:.7rem}
.st-key-vector_box_wrap div[data-testid="stSegmentedControl"] label{min-height:4.4rem;min-width:9.5rem;padding:1rem .9rem!important;font-size:1.02rem!important;border-radius:16px!important;border-width:1.5px!important}
.st-key-vector_box_wrap div[data-testid="stSegmentedControl"] label[aria-checked="true"],.st-key-vector_box_wrap div[data-testid="stSegmentedControl"] label[data-checked="true"]{box-shadow:0 0 0 2px var(--cyan),0 0 12px rgba(122,231,244,.65),0 0 40px rgba(122,231,244,.35)!important;background:radial-gradient(circle at 30% 20%,rgba(122,231,244,.28),rgba(122,231,244,.1))!important}
.st-key-vector_box_wrap div[data-testid="stSegmentedControl"] label p{font-size:1.02rem!important}
.st-key-blue_actor_box [data-baseweb="tag"]{background-color:#5fb8e8!important;border-color:#5fb8e8!important;color:#04202e!important}
.st-key-blue_actor_box [data-baseweb="tag"] span{color:#04202e!important}
.st-key-red_actor_box [data-baseweb="tag"]{background-color:var(--red)!important;border-color:var(--red)!important;color:#2a0508!important}
.st-key-red_actor_box [data-baseweb="tag"] span{color:#2a0508!important}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;border-radius:16px!important;background:rgba(7,27,41,.56)}div[data-testid="stExpander"]{border:1px solid var(--line);border-radius:14px;background:rgba(7,26,39,.58)}div[data-testid="stAlert"]{border-radius:14px;border-width:1px}[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:14px;overflow:hidden}[data-testid="stDataFrame"] *{font-size:.88rem}
hr{border-color:rgba(95,179,196,.18)!important}.stProgress>div>div>div>div{background:linear-gradient(90deg,#5ee8f0,#ffd279,#ff808d)}.stProgress>div>div{background:rgba(138,199,211,.13)}

@media(max-width:1100px){.ws-feature-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ws-domain-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ws-brief-grid{grid-template-columns:1fr 1fr}}
@media(max-width:900px){.block-container{padding-left:.9rem;padding-right:.9rem}.ws-feature-grid,.ws-domain-grid,.ws-brief-grid{grid-template-columns:1fr}.ws-title{font-size:2.55rem}}
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
        "adversarial_vector": None, "intensity": "medium",
        "blue_actors": ["Norway", "Denmark/Greenland", "Finland", "Iceland"], "red_actors": ["Russia"],
        "scenario_active": False,
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
    "govlab_docs": [],
    "contested_table": {"status": "CLOSED", "artifact": None, "trades": {}, "escalation_text": "", "escalation_run": False, "opened_by": ""}
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



def modifier_text(value):
    return f"{int(value):+d}"


def domain_card_style(gap):
    if gap < 40:
        return "low", "Resilient"
    if gap < 60:
        return "med", "Contested"
    return "high", "Exposed"


def render_domain_cards(domains):
    cards = []
    for domain in domains:
        gap = int(domain["gap"])
        card_class, label = domain_card_style(gap)
        cards.append(
            f"<div class='ws-domain-card {card_class}'><span class='name'>{domain['name']}</span><span class='gap'>{gap}%</span><span class='tag'>{label}</span></div>"
        )
    st.markdown(f"<div class='ws-domain-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def render_briefing_panel(state, callsign, posture, posture_class):
    try:
        log_df = load_log()
        latest_move = log_df.iloc[0]["move_type"] if not log_df.empty else "Awaiting first logged action"
    except Exception:
        latest_move = "Activity feed unavailable"
    try:
        arb_df = load_arbitration()
        open_cases = int((arb_df["status"] == "OPEN").sum()) if not arb_df.empty else 0
    except Exception:
        open_cases = 0

    treaty_state = "Active" if state.get("treaty_flag") else "Inactive"
    win_state = "Available" if state.get("win_win_active") else "Contested"
    st.markdown(
        f"""
        <div class="ws-brief">
          <div class="ws-kicker">High North Theatre Brief</div>
          <div class="ws-brief-title">NATO Arctic Situation Snapshot</div>
          <div class="ws-subtitle">Operational picture for <strong style='color:#edf7fa'>{callsign.upper()}</strong> across grey-zone competition, concession pressure, arbitration posture, and collective readiness.</div>
          <div class="ws-brief-grid">
            <div class="ws-mini-card"><small>Capability Posture</small><strong class="{posture_class}">{posture}</strong></div>
            <div class="ws-mini-card"><small>Active Doctrine</small><strong>{DOCTRINE_LABELS.get(state.get('doctrine','rus'),'—')}</strong></div>
            <div class="ws-mini-card"><small>Open Arbitration Cases</small><strong>{open_cases}</strong></div>
            <div class="ws-mini-card"><small>Treaty / Legal Mechanism</small><strong>{treaty_state}</strong></div>
            <div class="ws-mini-card"><small>Latest Activity</small><strong>{latest_move}</strong></div>
            <div class="ws-mini-card"><small>Stability Window</small><strong>{win_state}</strong></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

def compute_actor_thresholds():
    """Live per-actor threshold status -- baseline concession status escalated by how many
    times that actor has actually been the subject of a concession this session."""
    log = load_all()["log"]
    counts = {}
    for e in log:
        a = e.get("actor", "")
        counts[a] = counts.get(a, 0) + 1
    rows = []
    for a in ACTOR_BASELINES:
        c = counts.get(a["actor"], 0)
        live_status = a["concession"]
        if c >= 3 and live_status == "STABLE":
            live_status = "WATCH"
        elif c >= 5 and live_status in {"STABLE", "WATCH"}:
            live_status = "CRITICAL"
        rows.append({"Actor": a["actor"], "Baseline": a["concession"], "Concessions This Session": c,
                     "Live Status": live_status, "Primary Seam": a["seam"]})
    return rows

# ══════════════════════════════════════════════════════════
# JSONBIN.IO — shared, persistent state (this is what makes async multiplayer work)
# One JSON document, one API key. No SQL, no schema, no service-account file.
# ══════════════════════════════════════════════════════════
def _bin_url():
    return f"https://api.jsonbin.io/v3/b/{st.secrets['jsonbin']['bin_id']}"

def _headers():
    return {"X-Master-Key": st.secrets["jsonbin"]["master_key"], "Content-Type": "application/json"}

def _fetch_bin():
    resp = requests.get(f"{_bin_url()}/latest", headers=_headers(), timeout=10)
    resp.raise_for_status()
    return resp.json()["record"]

@st.cache_data(ttl=3, show_spinner=False)
def _load_all_cached():
    return _fetch_bin()

def load_all():
    """Every helper in this app calls load_all() independently -- without caching, a single
    page load can fire 10+ GET requests to JSONBin, which burns through the free tier's rate
    limit fast (worse with several participants and/or Live Mode's auto-refresh running).
    A short 3-second cache collapses those into one real request per rerun, and save_all()
    below clears it immediately so writes are never stale."""
    try:
        data = _load_all_cached()
    except requests.exceptions.RequestException as e:
        st.error(
            "⚠️ Couldn't reach the shared session store (JSONBin) right now. This is almost "
            "always a temporary rate limit or network hiccup, not a bug in the game logic. "
            f"\n\nDetails: {e}"
        )
        if st.button("🔄 Retry"):
            _load_all_cached.clear()
            st.rerun()
        st.stop()
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
    _load_all_cached.clear()  # invalidate the cache immediately so the next read isn't stale

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
    source_colors = {"REAL": "#7ae7f4", "SIMULATED": "#ff808d", "ANALYST": "#ffd279", "ARBITRATION": "#b9c9ff"}
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
        <div style="border:1px solid var(--line);border-left:3px solid {color};border-radius:10px;padding:.6rem .7rem;margin-bottom:.5rem;background:rgba(8,30,46,.52);">
          <div style="font-size:.68rem;color:var(--muted);letter-spacing:.03em;">Turn {entry.get('turn','?')} · {entry.get('ts','')} · {callsign_e}</div>
          <div style="margin:.2rem 0;"><span style="color:{color};font-weight:700;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;">{src}</span><br>
            <strong style="color:var(--ice);">{actor}</strong>
            <span style="color:var(--muted);"> — {move_type}</span></div>
          <div style="color:var(--muted);font-size:.82rem;">{detail}</div>
          <div style="font-size:.72rem;color:{'#ff727f' if delta>0 else '#7ee2a8' if delta<0 else 'var(--muted)'};margin-top:.2rem;">Cap Gap impact: {delta_str}</div>
        </div>"""
    st.markdown(f'<div style="max-height:78vh;overflow-y:auto;padding-right:.3rem;">{items_html}</div>', unsafe_allow_html=True)

def get_ai_moves():
    """Agentic AI Red Team moves only -- end_turn() logs these with callsign 'Agentic AI',
    distinguishing them from Cognitive Warfare/Narrative Analysis/Contested Table entries
    which also carry source=SIMULATED but under the human participant's own callsign."""
    raw_log = load_all()["log"]
    return [e for e in raw_log if e.get("callsign") == "Agentic AI"]

def get_last_ai_move():
    moves = get_ai_moves()
    return moves[-1] if moves else None

def render_ai_move_panel():
    ai_moves = get_ai_moves()
    st.markdown(f"<div class='ws-section-label'>⚡ Agentic AI — Turn-by-Turn Red Team Moves</div>", unsafe_allow_html=True)
    st.caption(f"{len(ai_moves)} Red Team move{'s' if len(ai_moves)!=1 else ''} generated this session via End Turn — separate from the general Shared Move Feed.")
    if not ai_moves:
        st.info("No AI moves yet. Click \"End Turn\" above to generate Turn 2.")
        return
    tag_colors = {"PROBE": "var(--amber)", "EXPLOIT": "var(--red)", "ESCALATE": "var(--red)", "WITHDRAW": "var(--green)"}
    items_html = ""
    for m in reversed(ai_moves):
        move_type = m.get("move_type", "")
        tag = move_type.split(" — ")[0] if " — " in move_type else "MOVE"
        title = move_type.split(" — ", 1)[1] if " — " in move_type else move_type
        color = tag_colors.get(tag, "var(--muted)")
        items_html += f"""
        <div style="border:1px solid var(--line);border-left:3px solid {color};border-radius:10px;padding:.65rem .8rem;margin-bottom:.5rem;background:rgba(8,30,46,.5);">
          <div style="font-size:.68rem;color:var(--muted);">Turn {m.get('turn','?')} · {m.get('ts','')} · {html.escape(str(m.get('actor','')))}</div>
          <div style="margin:.2rem 0;"><span style="color:{color};font-weight:700;font-size:.72rem;text-transform:uppercase;">{tag}</span>
            <strong style="color:var(--ice);margin-left:.4rem;">{html.escape(title)}</strong></div>
          <div style="color:var(--muted);font-size:.85rem;">{html.escape(str(m.get('detail','')))}</div>
        </div>"""
    st.markdown(f'<div style="max-height:340px;overflow-y:auto;">{items_html}</div>', unsafe_allow_html=True)

def render_winwin_banner(state):
    is_active = bool(state.get("win_win_active"))
    if "winwin_prev" not in st.session_state:
        st.session_state["winwin_prev"] = False
    if is_active and not st.session_state["winwin_prev"]:
        st.session_state["winwin_dismissed"] = False
    st.session_state["winwin_prev"] = is_active

    if is_active and not st.session_state.get("winwin_dismissed"):
        bcol1, bcol2 = st.columns([12, 1])
        with bcol1:
            st.markdown(
                "<div style='border:1px solid var(--green);border-left:4px solid var(--green);border-radius:12px;"
                "padding:.75rem 1rem;background:rgba(140,232,177,.08);color:var(--ice);margin-bottom:.8rem;'>"
                "<strong style='color:var(--green);'>🌟 WIN-WIN CONDITION DETECTED</strong> — Composite Cap Gap has fallen below 45% "
                "and a treaty/legal concession has been logged. A cooperative resolution is available at the Contested Table."
                "</div>", unsafe_allow_html=True)
        with bcol2:
            if st.button("✕", key="dismiss_winwin"):
                st.session_state["winwin_dismissed"] = True
                st.rerun()

def load_arbitration():
    arb = load_all()["arbitration"]
    if not arb:
        return pd.DataFrame(columns=["id", "case_id", "status", "violation", "asset", "stage", "opened_by", "opened_at"])
    return pd.DataFrame(arb)

def load_contested_table():
    data = load_all()
    return data.get("contested_table", {"status": "CLOSED", "artifact": None, "trades": {}, "escalation_text": "", "escalation_run": False, "opened_by": ""})

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
def score_document(doc_text, doc_title, callsign, live_query="", live_timespan="7d"):
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

    # 5. Live OSINT pull -- this is what was missing: score_document previously never fetched
    # current events at all, only checked already-tagged session history. Now it pulls fresh.
    live_events = []
    live_events_were_live = False
    if live_query.strip():
        live_events, live_events_were_live = fetch_osint(live_query.strip(), live_timespan)

    # 6. Gap findings -- generated sentences connecting matched Articles to live events, not just counts
    gap_findings = []
    for art in article_matches[:4]:
        art_terms = [w.strip(".,()").lower() for w in art["summary"].split() if len(w) > 5]
        matched_events = [e for e in live_events if any(t in e.get("title", "").lower() for t in art_terms)]
        if matched_events:
            titles = "; ".join(f'"{e["title"]}"' for e in matched_events[:2])
            gap_findings.append(
                f"**{art['article']}** ({art['summary']}) — {len(matched_events)} live event(s) touch this Article's territory: {titles}. "
                f"Current treaty language does not specify a consultation timeline or evidentiary threshold for this scenario class."
            )
        else:
            gap_findings.append(f"**{art['article']}** ({art['summary']}) — no live event in this pull matched this Article's language directly; document relevance is based on text overlap only.")

    # 7. Recommendations -- template-based, explicitly not AI-generated
    recommendations = []
    if covered_violations:
        recommendations.append(
            f"Consider an addendum clarifying consultation triggers for: {', '.join(covered_violations[:3])} — "
            f"categories referenced in this document but not explicitly defined as consultation-worthy under current Article 4 language."
        )
    if live_events:
        recommendations.append(
            f"{len(live_events)} live event(s) were pulled for \"{live_query}\" ({'live GDELT data' if live_events_were_live else 'cached sample — GDELT unavailable in this environment'}). "
            f"Cross-reference this document's provisions against those events before treating any Article match above as settled — treaty language should be tested against current activity, not historical precedent alone."
        )
    else:
        recommendations.append("No live event context was pulled for this scoring — findings above reflect only the document's text against static reference tables. Add search terms to ground this against today's activity.")

    # 8. Composite indicative score (0-100) -- NOT a legal or AI judgment, purely lexical overlap
    fit_score = min(100, len(article_matches) * 6 + len(covered_violations) * 8 + len(precedent_matches) * 5 + min(session_hits, 10) * 2 + min(len(live_events), 5) * 2)

    result = {
        "title": doc_title, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "uploaded_by": callsign,
        "excerpt": doc_text[:220], "fit_score": fit_score,
        "article_matches": article_matches[:5], "covered_violations": covered_violations,
        "precedent_matches": precedent_matches[:3], "session_hits": session_hits,
        "live_query": live_query, "live_event_count": len(live_events),
        "gap_findings": gap_findings, "recommendations": recommendations,
    }
    append_govlab_doc(result)
    return result

ADVERSARIAL_VECTORS = {
    "infra": {"icon": "⊙", "label": "Critical Infrastructure", "sub": "Polar Connect Cable // Arctic LNG Pipeline // GPS-PNT",
              "help": "The Polar Connect subsea cable, an Arctic LNG/oil pipeline, or GPS/PNT (positioning/navigation/timing) systems are interfered with or sabotaged."},
    "disinfo": {"icon": "≈", "label": "Disinformation Op", "sub": "Sovereignty Narrative // IIC Vector",
                "help": "Coordinated narrative campaign targeting Arctic sovereignty claims or alliance cohesion (IIC — Information Integrity Composite)."},
    "auto": {"icon": "▣", "label": "Autonomous Systems", "sub": "Icebreaker UxV // Arctic Seabed ASI",
             "help": "Unmanned icebreaker-class vessels (UxV) or autonomous seabed sensing infrastructure (ASI) probe or contest a boundary/asset."},
    "energy": {"icon": "⚡", "label": "Energy Coercion", "sub": "Arctic LNG // Nordic Grid // Barents Oil",
               "help": "Arctic LNG, Nordic grid interconnection, or Barents Sea oil leverage used as pressure against a Blue Team actor's energy dependence."},
    "hybrid": {"icon": "⬡", "label": "Compound Hybrid", "sub": "Multi-Domain Arctic Pressure",
               "help": "Two or more vectors occur together (e.g. cable interference + sovereignty narrative), designed to saturate Blue Team attention across the High North."},
    "legal": {"icon": "⚖", "label": "Legal / Sovereignty", "sub": "Svalbard Article 9 // EEZ Boundary",
              "help": "A grey-zone move that exploits treaty or legal ambiguity — e.g. Svalbard Treaty Article 9 demilitarization, or an Arctic EEZ boundary dispute — rather than a physical or cyber act."},
}
INTENSITY_LEVELS = {
    "low": {"label": "LOW", "sub": "Deniable", "help": "Deniable activity, easily disputed attribution, minimal Cap Gap movement."},
    "medium": {"label": "MEDIUM", "sub": "Below Art.4", "help": "Activity clearly below Article 4's plain threshold, but real and attributable."},
    "high": {"label": "HIGH", "sub": "Approaching Art.4", "help": "Activity approaching what Article 4 language would plainly cover; consultation-worthy."},
    "critical": {"label": "CRITICAL", "sub": "Cohesion Threat", "help": "Direct threat to alliance cohesion; the scenario most likely to force a Contested Table deadlock."},
}
ALL_BLUE_ACTORS = ["Norway", "Denmark/Greenland", "Finland", "Sweden", "Iceland", "Canada"]
ALL_RED_ACTORS = ["Russia", "China"]

DISPUTED_ARTIFACTS = {
    "svalbard": {"label": "Svalbard Treaty — Article 9 Demilitarisation",
                 "escalation": "RED TEAM — RUSSIA: Article 9 ambiguity cannot be resolved bilaterally. Counter-move: GRU-linked icebreaker enters disputed EEZ. NATO Capability Gap +5%. Mainsail (CMRE) flags anomalous trajectory — attribution MEDIUM. Blue Team window: T+4hrs.",
                 "delta": 5},
    "article5": {"label": "NATO Article 5 — Activation Threshold",
                 "escalation": "RED TEAM — RUSSIA+CHINA: Article 5 threshold exploited. AI-generated content questioning Finnish commitment. IIC degradation: −8pts. Verdict: EXPLOIT. Cap Gap +7%.",
                 "delta": 7},
    "caofa": {"label": "CAOFA — Moratorium Extension",
              "escalation": "RED TEAM — CHINA: CAOFA moratorium exploited as leverage. Conditional support for Polar Connect data sovereignty recognition. Warning: narrow scoping being weaponized.",
              "delta": 5},
    "minerals": {"label": "Greenland Critical Mineral Access",
                 "escalation": "RED TEAM — CHINA: Greenland mineral access contested three-way. Chinese infrastructure investment offer. Cap Gap +9% NATO. Verdict: ESCALATE.",
                 "delta": 9},
}
TRADE_ACTORS = ["Norway", "Denmark/Greenland", "Finland", "Iceland", "Canada", "United States"]
TRADE_TYPES = ["Access", "Resource", "Narrative/Legal"]

NARRATIVE_ASSESSMENTS = [
    {"intent": "HIGH", "autonomy": "HIGH", "interaction": "MEDIUM", "governance": "HIGH",
     "analysis": "Adversarial objective: fracture Nordic alliance solidarity via legal ambiguity. Primary seam: IIC gap between Iceland (42) and Norway (65).",
     "foresight": "Joint Nordic attribution statement within T+4hrs."},
    {"intent": "MEDIUM", "autonomy": "HIGH", "interaction": "HIGH", "governance": "MEDIUM",
     "analysis": "Adversarial objective: normalize infrastructure access through economic framing rather than security framing, reducing Blue Team's ability to invoke Article 4 consultation.",
     "foresight": "Pre-empt with a joint infrastructure-access transparency statement before the narrative gains traction."},
    {"intent": "HIGH", "autonomy": "MEDIUM", "interaction": "MEDIUM", "governance": "HIGH",
     "analysis": "Adversarial objective: exploit US–Greenland friction to widen the Denmark/Greenland seam already flagged as the theatre's most exposed concession point.",
     "foresight": "Coordinate a US–Denmark joint statement reaffirming the existing sovereignty arrangement."},
]

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

def run_narrative_analysis(narrative_text, callsign):
    """IAIG Narrative Analysis Engine — doctrine-independent, HIGH/MEDIUM/LOW output.
    Rules-based (no live LLM call), same security posture as everything else here.
    Picks a template using a simple keyword heuristic on the input, for texture rather
    than always returning the identical canned line."""
    text_lower = narrative_text.lower()
    if "greenland" in text_lower or "denmark" in text_lower:
        assessment = NARRATIVE_ASSESSMENTS[2]
    elif "infrastructure" in text_lower or "invest" in text_lower or "economic" in text_lower:
        assessment = NARRATIVE_ASSESSMENTS[1]
    else:
        assessment = NARRATIVE_ASSESSMENTS[0]

    state = load_state()
    label_delta = {"HIGH": 4, "MEDIUM": 1, "LOW": -3}
    mod = int(state.get("narrative_modifier", 0)) + label_delta.get(assessment["governance"], 2)
    state["narrative_modifier"] = max(-15, min(15, mod))
    state = recompute_cap_gap(state)
    save_state(state)
    append_log(state["turn"], callsign, "IAIG Narrative Analysis Engine",
               "NARRATIVE ANALYSIS", "SIMULATED",
               f"Narrative: \"{narrative_text[:120]}\" — {assessment['analysis']}", 0)
    return state, assessment

# ══════════════════════════════════════════════════════════
# CONTESTED NEGOTIATION TABLE — a separate resolution path from the Arbitration Track.
# Single shared table (one dispute at a time, matching the HTML build), with a
# Deadlock Protocol that flags when a Denmark/Greenland Access concession fires.
# ══════════════════════════════════════════════════════════
def generate_scenario(name, desc, doctrine, vector, intensity, blue_actors, red_actors):
    state = load_state()
    state["scenario_name"] = name
    state["scenario_desc"] = desc
    state["doctrine"] = doctrine
    state["adversarial_vector"] = vector
    state["intensity"] = intensity
    state["blue_actors"] = blue_actors
    state["red_actors"] = red_actors
    state["scenario_active"] = True
    save_state(state)
    return state

def open_contested_table(artifact_key, callsign):
    data = load_all()
    data["contested_table"] = {"status": "OPEN", "artifact": artifact_key, "trades": {}, "escalation_text": "", "escalation_run": False, "opened_by": callsign}
    save_all(data)
    append_log(data["state"]["turn"], callsign, "Negotiation Table",
               "TABLE OPENED", "ANALYST", f"Dispute opened: {DISPUTED_ARTIFACTS[artifact_key]['label']}", 0)

def set_trade(actor, ttype):
    data = load_all()
    data["contested_table"]["trades"][actor] = ttype
    save_all(data)

def run_table_escalation(callsign):
    data = load_all()
    ct = data["contested_table"]
    art = DISPUTED_ARTIFACTS.get(ct["artifact"], {"escalation": "RED TEAM — COMPOUND: Concession asymmetry detected. Cap Gap +6%.", "delta": 6})
    ct["escalation_text"] = art["escalation"]
    ct["escalation_run"] = True
    data["contested_table"] = ct
    state = data["state"]
    state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) + art["delta"]))
    state = recompute_cap_gap(state)
    data["state"] = state
    save_all(data)
    append_log(state["turn"], callsign, "Negotiation Table",
               "RED ESCALATION", "SIMULATED", art["escalation"], art["delta"])
    return state

def log_table_resolution(callsign):
    data = load_all()
    ct = data["contested_table"]
    trades = ct.get("trades", {})
    state = data["state"]
    if any(t == "Narrative/Legal" for t in trades.values()):
        state["treaty_flag"] = True
    state["concession_modifier"] = max(-20, min(20, int(state.get("concession_modifier", 0)) - 2))
    state = recompute_cap_gap(state)
    trade_summary = ", ".join(f"{a}:{t}" for a, t in trades.items()) or "No trades selected"
    artifact_label = DISPUTED_ARTIFACTS.get(ct["artifact"], {}).get("label", ct.get("artifact") or "Unknown")
    data["state"] = state
    data["contested_table"] = {"status": "CLOSED", "artifact": None, "trades": {}, "escalation_text": "", "escalation_run": False, "opened_by": ""}
    save_all(data)
    append_log(state["turn"], callsign, "Negotiation Table",
               "RESOLUTION", "ANALYST", f"Resolution — {artifact_label}. Trades: {trade_summary}", -2)
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
    st.markdown("""
    <div class="ws-hero">
      <div class="ws-kicker">Auracelle AI Governance Labs · NATO Arctic High North Decision Environment</div>
      <div class="ws-title">WINTERSTORM<span style="color:#7ae7f4">2030</span></div>
      <div class="ws-subtitle">WinterStorm2030 measures the gap between grey-zone activity and NATO's Article 4/5 thresholds — scoring how urgent a decision is, and stress-testing where existing NATO policy has no clear answer. It draws on real-time OSINT event data and historical treaty precedent (including the 1949 North Atlantic Treaty and comparative grey-zone/infrastructure-dispute analogues) to build an evidence-grounded case for a NATO Treaty addendum or revision recommendation by 2030, in support of NATO STO SAS-219's full range of workstreams — not a combat simulator.</div>
      <div class="ws-badges">
        <span class="ws-badge">NATO ARCTIC HIGH NORTH</span>
        <span class="ws-badge">ARTICLE 4/5 GAP SCORING</span>
        <span class="ws-badge">AGENTIC AI RED TEAM</span>
        <span class="ws-badge">CONTESTED NEGOTIATION TABLE</span>
        <span class="ws-badge">ASYNCHRONOUS MULTIPLAYER</span>
      </div>
    </div>
    <div class="ws-feature-grid">
      <div class="ws-feature"><strong>Strategic Purpose</strong>Score the urgency of a decision at the seam between grey-zone activity and NATO's Article 4/5 consultation threshold.</div>
      <div class="ws-feature"><strong>Evidence Base</strong>Real-time OSINT event data plus historical treaty precedent, feeding a written case for where NATO policy needs an addendum or revision.</div>
      <div class="ws-feature"><strong>Operational Logic</strong>Trade concessions, counter narratives, calibrate domain gaps, and work disputes before they cascade into strategic failure.</div>
      <div class="ws-feature"><strong>Shared Environment</strong>Persistent state, shared move history, and asynchronous access support distributed participation over time.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        callsign_input = st.text_input("Callsign")
        access_code = st.text_input("Access Code", type="password")

        st.markdown("<div class='ws-section-label'>Secure Participant Access</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='ws-callout'><strong>Governance capacity instrument</strong> — not a combat simulator. "
            "WinterStorm2030 measures how policy, institutional capacity, alliance cohesion, concessions, "
            "narratives, and grey-zone actions alter the live NATO Capability Gap, and where that gap exposes "
            "shortfalls in current NATO treaty language that a 2030 addendum could address.</div>",
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
last_ai_move = get_last_ai_move()
last_move_str = f"{last_ai_move['move_type']}" if last_ai_move else "No AI moves yet"

with st.sidebar:
    render_move_feed()

st.markdown("<div class='ws-section-label'>High North Command Overview</div>", unsafe_allow_html=True)
hero_left, hero_right = st.columns([1.65, 1.05], gap="large")
with hero_left:
    st.markdown(f"""
    <div class="ws-hero">
      <div class="ws-kicker">NATO STO SAS-219 · High North Scenarios for Wargaming & Analysis</div>
      <div class="ws-title" style="font-size:2.85rem">WINTERSTORM<span style="color:#7ae7f4">2030</span></div>
      <div class="ws-subtitle"><strong style="color:#edf7fa">{scenario_label}</strong><br>Governance capacity · grey-zone competition · strategic concession analysis · alliance resilience decision-testing across the Arctic High North.</div>
      <div class="ws-badges">
        <span class="ws-badge">CALLSIGN: {callsign.upper()}</span>
        <span class="ws-badge">TURN {state['turn']}</span>
        <span class="ws-badge">SHARED STATE ACTIVE</span>
        <span class="ws-badge">POSTURE: <span class="{posture_class}">{posture}</span></span>
        <span class="ws-badge">NATO / NORDIC THEATRE</span>
      </div>
      <div class="ws-chip-row" style="margin-top:1rem">
        <span class="ws-chip">Grey-Zone Competition</span>
        <span class="ws-chip">Alliance Governance</span>
        <span class="ws-chip">Strategic Concession Analysis</span>
        <span class="ws-chip">Arctic Infrastructure Continuity</span>
      </div>
      <div style="margin-top:.8rem;font-size:.78rem;color:var(--muted);">
        <strong style="color:var(--cyan2);">{DOCTRINE_LABELS.get(state.get('doctrine','rus'),'—')}</strong>
        &nbsp;·&nbsp; Last AI move: <span style="color:var(--ice);">{html.escape(last_move_str)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
with hero_right:
    render_briefing_panel(state, callsign, posture, posture_class)

render_winwin_banner(state)

st.markdown("<div class='ws-section-label'>Operational Status</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Turn", state["turn"], help="Shared simulation turn visible to all participants.")
c2.metric("NATO Capability Gap", f"{state['cap_gap']}%", help="Lower scores indicate a smaller capability gap and stronger collective resilience.")
c3.metric("Adversary Doctrine", DOCTRINE_LABELS.get(state.get("doctrine", "rus"), "—"), help="Doctrine governing Agentic AI Red Team behavior.")
c4.metric("Negotiated Stability", "ACHIEVED" if state.get("win_win_active") else "NOT YET", help="Achieved below a 45% gap with an active treaty/legal mechanism.")
st.markdown(f"<div class='ws-status'><span class='ws-dot'></span> Shared state online &nbsp;·&nbsp; Capability posture: <strong class='{posture_class}'>{posture}</strong> &nbsp;·&nbsp; Concession modifier: {state.get('concession_modifier',0):+d} &nbsp;·&nbsp; Narrative pressure: {state.get('narrative_modifier',0):+d}</div>", unsafe_allow_html=True)

ai_col, nav_col = st.columns([1.5, 1])
with ai_col:
    render_ai_move_panel()
with nav_col:
    with st.expander("ℹ️ Architecture & Navigation Guide", expanded=False):
        st.markdown("""
**Architecture highlights**
- **Concession Engine** — Access / Resource / Narrative-Legal, per-actor thresholds, Deadlock Protocol
- **Contested Negotiation Table** — a separate trade-based resolution path from the Arbitration Track
- **Cognitive Warfare & Narrative Analysis** — two distinct doctrine-based assessment engines (Decision-Support only)
- **NATO Cap Gap** — five-domain composite, every tab writes to the same shared number
- **OSINT Feed** — real GDELT event data, no LLM call, with a Strait of Hormuz calibration baseline
- **Governance Lab** — upload/paste a treaty or policy for rules-based scoring against NATO doctrine

**Navigation guide**
| Tab | Use it for |
|---|---|
| Scenario Setup | Configure vector, intensity, actors, doctrine — start here |
| Actor Analysis | Static baseline reference across all six Blue actors |
| Concession Engine | Trigger concessions; live per-actor threshold status |
| NATO Cap Gap | Composite score + five-domain breakdown |
| Dynamic Governance Tracking | Scenario clock + live IIC/CD/Cap Gap state |
| OSINT Feed | Real event data, tag into Concession Engine or Article 4 log |
| Cognitive Warfare | Numeric doctrine-based narrative scoring |
| Narrative Analysis | HIGH/MEDIUM/LOW categorical narrative read |
| Arbitration Track | 5-stage standing escalation ladder |
| Governance Lab | Upload a document for treaty/precedent scoring |
        """)

st.divider()

st.markdown("<div class='ws-section-label'>Decision Environment</div>", unsafe_allow_html=True)
mode = st.segmented_control(
    "Mode",
    ["◆ Decision-Maker (breadth — act on it)", "◇ Decision-Support (full depth — including Arbitration Track)"],
    default="◇ Decision-Support (full depth — including Arbitration Track)",
    key="dm_ds_mode",
)
if mode is None:
    mode = "◇ Decision-Support (full depth — including Arbitration Track)"
is_dm = mode.startswith("◆")
if is_dm:
    st.caption("Decision-Maker mode: the Arbitration Track (a procedural escalation ladder), Cognitive Warfare, Narrative Analysis, and Governance Lab are hidden. "
               "Scenario Setup is editable in both modes. Switch to Decision-Support for the full depth toolkit.")

st.markdown(f"""
<div class='ws-mode-note'>
  <div class='ws-status'><span class='ws-dot'></span> <strong style='color:#edf7fa'>Active mode:</strong> {mode} &nbsp;·&nbsp; <strong style='color:#edf7fa'>Current posture:</strong> <span class='{posture_class}'>{posture}</span> &nbsp;·&nbsp; <strong style='color:#edf7fa'>Concession modifier:</strong> {modifier_text(state.get('concession_modifier',0))} &nbsp;·&nbsp; <strong style='color:#edf7fa'>Narrative pressure:</strong> {modifier_text(state.get('narrative_modifier',0))}</div>
</div>
""", unsafe_allow_html=True)

tab_names = ["📋 Scenario Setup", "🧑‍🤝‍🧑 Actor Analysis", "🤝 Concession Engine", "📡 NATO Cap Gap",
             "📈 Dynamic Governance Tracking", "🛰️ OSINT Feed"]
if not is_dm:
    tab_names += ["🧠 Cognitive Warfare", "🗞️ Narrative Analysis", "⚖ Arbitration Track", "📚 Governance Lab"]
tabs = st.tabs(tab_names)

tab_scenario, tab_actors, tab_concession, tab_capgap, tab_dgt, tab_osint = tabs[0], tabs[1], tabs[2], tabs[3], tabs[4], tabs[5]
if not is_dm:
    tab_cogwar = tabs[6]
    tab_narrative = tabs[7]
    tab_arbitration = tabs[8]
    tab_govlab = tabs[9]

with tab_scenario:
    st.markdown("<div class='ws-section-label'>Scenario & Doctrine Configuration</div>", unsafe_allow_html=True)
    st.markdown("**Step 01 — Scenario Identity**")
    st.write("Set once, visible to every participant on refresh. Editable in both Decision-Maker and Decision-Support mode.")
    name = st.text_input("Scenario Name", value=state.get("scenario_name", ""))
    desc = st.text_area("Scenario Description", value=state.get("scenario_desc", ""))
    doctrine = st.selectbox("Active Adversary Doctrine", options=list(DOCTRINE_LABELS.keys()),
                             format_func=lambda k: DOCTRINE_LABELS[k],
                             index=list(DOCTRINE_LABELS.keys()).index(state.get("doctrine", "rus")))

    st.markdown("---")
    st.markdown("**Step 02 — Adversarial Vector**")
    st.write("Click a box below to select the primary adversarial action this scenario centers on.")
    vec_keys = list(ADVERSARIAL_VECTORS.keys())
    default_vec = state.get("adversarial_vector") if state.get("adversarial_vector") in vec_keys else vec_keys[0]
    with st.container(key="vector_box_wrap"):
        selected_vector = st.segmented_control(
            "Adversarial vector",
            options=vec_keys,
            format_func=lambda k: f"{ADVERSARIAL_VECTORS[k]['icon']}  {ADVERSARIAL_VECTORS[k]['label']}",
            default=default_vec,
            key="vector_control",
            label_visibility="collapsed",
        )
    if selected_vector is None:
        selected_vector = default_vec
    st.caption(f"**{ADVERSARIAL_VECTORS[selected_vector]['sub']}** — {ADVERSARIAL_VECTORS[selected_vector]['help']}")

    st.markdown("---")
    st.markdown("**Step 03 — Intensity**")
    int_keys = list(INTENSITY_LEVELS.keys())
    selected_intensity = st.radio("Intensity level", options=int_keys,
                                   format_func=lambda k: f"{INTENSITY_LEVELS[k]['label']} — {INTENSITY_LEVELS[k]['sub']}",
                                   index=int_keys.index(state.get("intensity", "medium")), horizontal=True)
    st.caption(INTENSITY_LEVELS[selected_intensity]["help"])

    st.markdown("---")
    st.markdown("**Step 04 — Actor Selection**")
    acols = st.columns(2)
    with acols[0]:
        with st.container(key="blue_actor_box"):
            blue_sel = st.multiselect("Blue Team actors", options=ALL_BLUE_ACTORS, default=state.get("blue_actors", ALL_BLUE_ACTORS[:4]))
    with acols[1]:
        with st.container(key="red_actor_box"):
            red_sel = st.multiselect("Red Team actors", options=ALL_RED_ACTORS, default=state.get("red_actors", ["Russia"]))

    st.markdown("---")
    if state.get("scenario_active"):
        st.success("✓ SCENARIO ACTIVE — all analytical panels are contextualised to this configuration.")
    if st.button("🚀 Generate Analysis", type="primary"):
        state = generate_scenario(name, desc, doctrine, selected_vector, selected_intensity, blue_sel, red_sel)
        st.success("✓ SCENARIO ACTIVE. All analytical panels are live — the Concession Engine, Cognitive Warfare, Narrative Analysis, and NATO Cap Gap tracker are now contextualised to this configuration.")
        st.rerun()

with tab_actors:
    st.markdown("<div class='ws-section-label'>Actor Readiness & Strategic Seam Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='ws-chip-row'><span class='ws-chip'>Alliance Baselines</span><span class='ws-chip'>Exposure & Vulnerability</span><span class='ws-chip'>Primary Strategic Seams</span><span class='ws-chip'>Panel Validation Invited</span></div>", unsafe_allow_html=True)
    st.write("Arctic theatre baselines across governance capacity, institutional indicators, exposure, concession status, and each actor's primary strategic seam. This table grounds the NATO High North readiness picture and helps identify where policy or adversarial pressure is most likely to bite.")
    st.dataframe(styled_actor_table(), use_container_width=True, hide_index=True, height=320)

with tab_capgap:
    st.markdown("<div class='ws-section-label'>Collective Capability-Gap Monitor</div>", unsafe_allow_html=True)
    st.write(f"**Composite gap: {state['cap_gap']}% · Posture: {posture}** — calculated from five operational-governance domains, then adjusted by concession effects and adversarial narrative pressure. Lower scores indicate stronger collective resilience.")
    render_domain_cards(state["domains"])
    st.progress(state["cap_gap"] / 100, text=f"{state['cap_gap']}% capability gap")
    domain_df = pd.DataFrame(state["domains"]).rename(columns={"name": "Capability Domain", "gap": "Gap %"})
    st.dataframe(domain_df.style.bar(subset=["Gap %"], vmin=0, vmax=100), use_container_width=True, hide_index=True, height=245)

    if is_dm:
        st.caption("Domain-level adjustment is Decision-Support depth tooling. Switch to Decision-Support to see or change what's behind this number.")
    else:
        st.markdown("<div class='ws-callout-panel'><strong style='color:#edf7fa'>Capability management controls</strong> — adjust an individual domain to model Blue Team closure or Red Team widening pressure against the shared NATO capability picture.</div>", unsafe_allow_html=True)
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
    st.write("Model how access, resource, and narrative-legal concessions shift collective resilience. Every action is immediately written to the shared move log and reflected in the NATO capability picture.")
    st.markdown("<div class='ws-feature-grid' style='grid-template-columns:repeat(3,minmax(0,1fr));margin-top:.2rem'><div class='ws-feature'><strong>Access</strong>Transit, basing, corridor, or inspection access concessions.</div><div class='ws-feature'><strong>Resource</strong>Material, financing, extraction, or infrastructure concessions.</div><div class='ws-feature'><strong>Narrative-Legal</strong>Recognition, sovereignty framing, legal position, or messaging concessions.</div></div>", unsafe_allow_html=True)
    actor = st.selectbox("Triggering Actor", ["Norway", "Denmark/Greenland", "Finland", "Iceland", "Canada",
                                               "United States", "Russia (Red)", "China (Red)"])
    ctype = st.selectbox("Concession Type", ["Access", "Resource", "Narrative-Legal"])
    desc = st.text_area("Description")
    if st.button("Trigger Concession"):
        is_red = "Red" in actor
        state = trigger_concession(actor, ctype, desc or "No description provided", callsign, is_red)
        st.success(f"Logged — Cap Gap now {state['cap_gap']}%")
        if actor == "Denmark/Greenland" and ctype == "Access":
            st.session_state["deadlock_flag"] = True
        st.rerun()

    st.divider()
    st.markdown("<div class='ws-section-label'>Per-Actor Threshold Status</div>", unsafe_allow_html=True)
    st.caption("Live view, separate from the static Actor Analysis baseline table — escalates when an actor is repeatedly the subject of concessions this session.")
    threshold_rows = compute_actor_thresholds()
    tdf = pd.DataFrame(threshold_rows)
    st.dataframe(
        tdf.style.map(
            lambda v: "color:#ff808d;font-weight:700" if v in {"CRITICAL", "VULNERABLE"}
            else ("color:#ffd279;font-weight:700" if v == "WATCH" else "color:#8ce8b1;font-weight:700"),
            subset=["Baseline", "Live Status"]
        ),
        use_container_width=True, hide_index=True
    )

    if st.session_state.get("deadlock_flag"):
        st.warning("**Deadlock Protocol** — Denmark/Greenland Access concession detected with the US adversarial flag active. "
                   "Open the Contested Table to resolve this through trades rather than letting it sit unresolved.")
        dcols = st.columns([2, 1])
        deadlock_artifact = dcols[0].selectbox("Dispute to open", options=list(DISPUTED_ARTIFACTS.keys()),
                                                format_func=lambda k: DISPUTED_ARTIFACTS[k]["label"],
                                                index=list(DISPUTED_ARTIFACTS.keys()).index("minerals"), key="deadlock_artifact")
        if dcols[1].button("Open Contested Table"):
            open_contested_table(deadlock_artifact, callsign)
            st.session_state["deadlock_flag"] = False
            st.rerun()
        if st.button("Dismiss"):
            st.session_state["deadlock_flag"] = False
            st.rerun()

    st.divider()
    st.markdown("<div class='ws-section-label'>Contested Negotiation Table</div>", unsafe_allow_html=True)
    st.caption("A separate resolution path from the Arbitration Track — one active dispute at a time, resolved by trading concession types across all six actors rather than a procedural ladder.")

    ct = load_contested_table()
    if ct["status"] != "OPEN":
        ocols = st.columns([2, 1])
        open_artifact = ocols[0].selectbox("Disputed artifact", options=list(DISPUTED_ARTIFACTS.keys()),
                                            format_func=lambda k: DISPUTED_ARTIFACTS[k]["label"], key="manual_artifact")
        if ocols[1].button("Open Negotiation Table"):
            open_contested_table(open_artifact, callsign)
            st.rerun()
    else:
        st.markdown(f"**Open dispute:** {DISPUTED_ARTIFACTS[ct['artifact']]['label']}  \n*Opened by {ct['opened_by']}*")
        st.markdown("**Concession Trade Declaration** — assign a trade type per actor (or leave unset):")
        trades = ct.get("trades", {})
        for a in TRADE_ACTORS:
            tcols = st.columns([1, 2])
            tcols[0].markdown(f"**{a}**")
            current = trades.get(a, "— none —")
            options = ["— none —"] + TRADE_TYPES
            choice = tcols[1].selectbox(f"trade_{a}", options=options, index=options.index(current) if current in options else 0,
                                         key=f"trade_select_{a}", label_visibility="collapsed")
            if choice != current:
                set_trade(a, None if choice == "— none —" else choice)
                st.rerun()

        st.markdown("---")
        bcols = st.columns(2)
        if bcols[0].button("⚡ Run Escalation"):
            run_table_escalation(callsign)
            st.rerun()
        if bcols[1].button("✅ Log Resolution & Close Table"):
            log_table_resolution(callsign)
            st.success("Resolution logged — table closed.")
            st.rerun()

        if ct.get("escalation_run"):
            st.markdown(
                f"<div class='ws-callout-panel' style='border-left-color:var(--red);'><strong style='color:var(--red);'>Agentic AI Assessment — Red Team Response</strong><br>{html.escape(ct['escalation_text'])}</div>",
                unsafe_allow_html=True)

if not is_dm:
    with tab_cogwar:
        st.markdown("<div class='ws-section-label'>Cognitive Warfare Assessment</div>", unsafe_allow_html=True)
        st.markdown("<div class='ws-chip-row'><span class='ws-chip'>Narrative Pressure</span><span class='ws-chip'>Doctrine Inference</span><span class='ws-chip'>No Live LLM Call</span><span class='ws-chip'>Blue Team Response Prompting</span></div>", unsafe_allow_html=True)
        st.write("Doctrine-based assessment — no live LLM call, consistent with the security constraint on this deployment. Running an analysis sets the session's active adversary doctrine and advances the turn.")
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

    with tab_narrative:
        st.markdown("<div class='ws-section-label'>IAIG Narrative Analysis Engine</div>", unsafe_allow_html=True)
        st.markdown("<div class='ws-chip-row'><span class='ws-chip'>HIGH / MEDIUM / LOW Output</span><span class='ws-chip'>Doctrine-Independent</span><span class='ws-chip'>No Live LLM Call</span><span class='ws-chip'>Foresight Recommendation</span></div>", unsafe_allow_html=True)
        st.write("Distinct from Cognitive Warfare's numeric doctrine scoring — this engine reads a narrative on its own terms and returns categorical "
                 "Intent/Autonomy/Interaction/Governance labels plus a foresight recommendation. Rules-based (no live LLM call), same security posture as the rest of this deployment.")
        narr_input = st.text_area("Narrative to analyze", key="narr_input", placeholder="Paste or describe the narrative/activity...")
        if st.button("Run Narrative Analysis"):
            if not narr_input.strip():
                st.error("Enter a narrative first.")
            else:
                state, assessment = run_narrative_analysis(narr_input, callsign)
                ncols = st.columns(4)
                label_color = {"HIGH": "var(--red)", "MEDIUM": "var(--amber)", "LOW": "var(--green)"}
                for col, key, label in zip(ncols, ["intent", "autonomy", "interaction", "governance"],
                                            ["Intent", "Autonomy", "Interaction", "Governance"]):
                    col.markdown(f"<div class='ws-mini-card'><small>{label}</small><strong style='color:{label_color.get(assessment[key],'var(--ice)')}'>{assessment[key]}</strong></div>", unsafe_allow_html=True)
                st.info(f"**Analysis:** {assessment['analysis']}")
                st.success(f"**Foresight:** {assessment['foresight']}")
                st.caption(f"Cap Gap now {state['cap_gap']}% — narrative pressure modifier updated, session turn unchanged (unlike Cognitive Warfare, this does not advance the turn).")

    with tab_arbitration:
        st.markdown("<div class='ws-section-label'>Arbitration & Strategic Continuity Track</div>", unsafe_allow_html=True)
        st.markdown("<div class='ws-chip-row'><span class='ws-chip'>Notification</span><span class='ws-chip'>Joint Verification</span><span class='ws-chip'>Interim Continuity</span><span class='ws-chip'>Conciliation</span><span class='ws-chip'>Binding Arbitration</span></div>", unsafe_allow_html=True)
        st.write("A standing procedural escalation ladder adapted from Boundary Waters, Columbia River, and Canterbury-type mechanisms — designed for the Arctic High North as a continuity-preserving dispute architecture rather than a one-time trigger.")
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
        st.markdown("<div class='ws-callout-panel'><strong style='color:#edf7fa'>Reference workspace</strong> — upload or paste a treaty, policy, or legal agreement for indicative assessment against NATO doctrine, live current events, and this session's evidence.</div>", unsafe_allow_html=True)
        st.write("Upload or paste a treaty, policy, or legal agreement (e.g. the 1949 North Atlantic Treaty) for assessment against NATO doctrine, a live OSINT pull, and this session's own generated evidence. Scoring is rules-based lexical overlap plus templated findings — labeled indicative, not a legal or AI judgment.")
        st.warning("**SCOPE** — This is heuristic keyword/overlap scoring (an E-AGPO-HT-style indicative score) with templated gap findings, not a generative-AI legal analysis "
                   "or a substitute for expert review. No document text is sent anywhere — scoring runs locally against the reference tables below, plus a live GDELT pull if you provide search terms.")

        upload_mode = st.radio("Input method", ["Paste text", "Upload .txt file"], horizontal=True, key="govlab_input_mode")
        doc_title = st.text_input("Document title", placeholder="e.g. North Atlantic Treaty (1949)")
        doc_text = ""
        if upload_mode == "Paste text":
            doc_text = st.text_area("Paste document text", height=200, key="govlab_paste")
        else:
            uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
            if uploaded is not None:
                doc_text = uploaded.read().decode("utf-8", errors="ignore")
                st.caption(f"Loaded {len(doc_text)} characters from {uploaded.name}.")

        st.markdown("**Live event context** — pulls a fresh OSINT query at scoring time and cross-references it against the document's Article matches below.")
        gcols = st.columns([2, 1])
        live_query = gcols[0].text_input("Search terms", placeholder="e.g. Iran Israel United States", key="govlab_live_query")
        live_timespan = gcols[1].selectbox("Window", ["1d", "3d", "7d", "30d"], index=2, key="govlab_live_span",
                                            format_func=lambda t: {"1d": "Last 24h", "3d": "Last 3 days", "7d": "Last 7 days", "30d": "Last 30 days"}[t])

        if st.button("Score Document"):
            if not doc_text.strip():
                st.error("Provide document text first — paste it in or upload a .txt file.")
            else:
                result = score_document(doc_text, doc_title or "Untitled document", callsign, live_query, live_timespan)
                st.success(f"Scored and logged — Governance Fit Score: {result['fit_score']}/100 · {result['live_event_count']} live event(s) factored in")
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
                    mcols = st.columns(4)
                    mcols[0].metric("Treaty Article Matches", len(d["article_matches"]))
                    mcols[1].metric("Violation Categories", len(d["covered_violations"]))
                    mcols[2].metric("Session Evidence Overlap", d["session_hits"])
                    mcols[3].metric("Live Events Pulled", d.get("live_event_count", 0))
                    if d["covered_violations"]:
                        st.caption("Grey-zone categories referenced: " + ", ".join(d["covered_violations"]))
                    if d.get("precedent_matches"):
                        st.caption("Precedent library alignment: " + ", ".join(f"{p['treaty']} ({p['hits']})" for p in d["precedent_matches"]))

                    if d.get("gap_findings"):
                        st.markdown("**Gap Findings**")
                        for f in d["gap_findings"]:
                            st.markdown(f"- {f}")
                    if d.get("recommendations"):
                        st.markdown("**Recommendations**")
                        for r in d["recommendations"]:
                            st.markdown(f"- {r}")

        st.divider()
        st.markdown("<div class='ws-section-label'>Reference Library</div>", unsafe_allow_html=True)
        st.caption("Static reference material the scoring above checks documents against — not live game state.")
        with st.expander("North Atlantic Treaty (signed in Washington, D.C., April 4, 1949) — all 14 Articles"):
            st.caption("Commonly referred to by the city where it was signed — the same document that contains Articles 4 and 5, not a separate treaty.")
            st.dataframe(pd.DataFrame(WASHINGTON_TREATY_ARTICLES), use_container_width=True, hide_index=True)
        with st.expander("Precedent Library — grey-zone infrastructure & boundary dispute analogues"):
            for p in PRECEDENT_LIBRARY:
                st.markdown(f"**{p['treaty']}**")
                st.markdown(f"Infrastructure focus: {p['focus']}")
                st.markdown(f"Why it's a useful analogue: {p['why']}")
                st.markdown("---")

st.divider()
st.markdown("<div class='ws-section-label'>Session Controls</div>", unsafe_allow_html=True)
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
