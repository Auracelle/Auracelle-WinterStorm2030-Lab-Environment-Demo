# winterstorm_game_ui.py
# A complete game-mode UI for WinterStorm2030
# Drop-in replacement for the current UI structure - uses same backend logic

import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

# ============================================
# GAME STATE ENHANCEMENTS
# ============================================

# Extended game state with win/loss tracking
GAME_OBJECTIVES = {
    "primary": {
        "name": "Prevent NATO Article 4 Invocation",
        "description": "Keep the Cap Gap below 75% for 10 turns",
        "success_condition": "cap_gap_below_75_for_10_turns",
        "failure_condition": "cap_gap_above_75",
        "progress": 0,
        "max_progress": 10
    },
    "secondary": [
        {
            "name": "Maintain Nordic Solidarity",
            "description": "Keep Iceland, Finland, and Norway in alignment",
            "success_condition": "alliance_cohesion_above_60",
            "current": 0,
            "target": 60
        },
        {
            "name": "Secure the GIUK Gap",
            "description": "Reduce Undersea Surveillance gap below 50%",
            "success_condition": "undersea_gap_below_50",
            "current": 0,
            "target": 50
        }
    ]
}

# AI Opponent personality with adaptive behavior
AI_PERSONALITY = {
    "rus": {
        "name": "KOMANDOR",
        "title": "Russian Northern Fleet Commander",
        "emoji": "⚓",
        "tactics": ["narrative", "probe", "escalate", "deniable"],
        "responses": {
            "narrative": "Your words are as thin as the Arctic ice, Minister.",
            "probe": "We are merely exercising our rights in international waters.",
            "escalate": "You force our hand. This is on you.",
            "defensive": "You've countered this move. But the next one...",
            "victory": "The Arctic belongs to those who dare.",
            "defeat": "You've won this round. But winter always returns."
        }
    },
    "prc": {
        "name": "WEI LANG",
        "title": "China's Arctic Envoy",
        "emoji": "🐉",
        "tactics": ["infrastructure", "economic", "legal", "hybrid"],
        "responses": {
            "infrastructure": "Our cables connect nations. Yours divide them.",
            "economic": "Capital finds its own path. Always.",
            "legal": "The law is written by those who show up.",
            "hybrid": "You see chaos. We see opportunity.",
            "victory": "The future of the Arctic is Asian.",
            "defeat": "A temporary setback. We are patient."
        }
    }
}

# Narrative arc events that trigger based on game state
NARRATIVE_BEATS = [
    {
        "trigger": "turn_3",
        "title": "The Svalbard Incident",
        "description": "A Norwegian fishing vessel reports a submersible near its nets. Russia denies involvement.",
        "choice": [
            {"label": "🔍 Investigate quietly", "effect": "narrative_modifier_-2", "text": "You order a discreet intelligence review."},
            {"label": "📢 Public condemnation", "effect": "narrative_modifier_+4", "text": "Norway issues a formal diplomatic protest."},
            {"label": "🤝 Offer joint inspection", "effect": "concession_modifier_-3", "text": "You propose a bilateral inspection mechanism."}
        ]
    },
    {
        "trigger": "turn_6",
        "title": "The Cable Cut",
        "description": "A fiber optic cable in the GIUK gap goes offline. Unconfirmed reports suggest sabotage.",
        "choice": [
            {"label": "🛡️ NATO emergency protocol", "effect": "cap_gap_-5", "text": "You activate NATO's critical infrastructure response."},
            {"label": "🔬 Technical investigation", "effect": "narrative_modifier_-3", "text": "You treat it as a commercial incident."},
            {"label": "⚖️ Open arbitration case", "effect": "arbitration_status_open", "text": "You file a formal dispute."}
        ]
    },
    {
        "trigger": "turn_9",
        "title": "The Summit",
        "description": "NATO allies demand a clear response. The clock is running out.",
        "choice": [
            {"label": "🏛️ Push for Article 4 consultation", "effect": "article_4_invocation", "text": "You escalate to formal consultation."},
            {"label": "🤝 Brokered deal with Russia", "effect": "concession_modifier_-8", "text": "You offer significant concessions for stability."},
            {"label": "⏳ Buy more time", "effect": "narrative_modifier_-4", "text": "You delay for more intelligence."}
        ]
    }
]

# Special abilities that unlock as the game progresses
UNLOCKABLES = {
    "turn_4": {
        "name": "Emergency NATO Summit",
        "description": "Call an emergency NATO meeting to coordinate response",
        "effect": "alliance_cohesion_+10"
    },
    "turn_6": {
        "name": "Arctic Patrol Escalation",
        "description": "Increase Nordic patrols in the GIUK gap",
        "effect": "undersea_gap_-8"
    },
    "turn_8": {
        "name": "Diplomatic Offensive",
        "description": "Launch a coordinated diplomatic campaign",
        "effect": "narrative_modifier_-6"
    }
}

# ============================================
# GAME UI COMPONENTS
# ============================================

def init_game_state():
    """Initialize extended game state if not present"""
    if "game" not in st.session_state:
        st.session_state.game = {
            "turn": 1,
            "phase": "setup",  # setup | active | crisis | resolution
            "alliance_cohesion": 72,
            "nordic_solidarity": 68,
            "public_support": 55,
            "consecutive_wins": 0,
            "consecutive_losses": 0,
            "narrative_events_triggered": [],
            "unlocked_abilities": [],
            "used_abilities": [],
            "ai_used_tactics": [],
            "ai_current_mood": "neutral",
            "victory_countdown": 10,
            "crisis_events": [],
            "story_log": []
        }

def game_css():
    """Game-themed CSS overlay"""
    return """
    <style>
    /* Game-specific overrides */
    .game-header {
        background: linear-gradient(135deg, #0a1a2a 0%, #1a3a4a 100%);
        border-bottom: 3px solid #4fc3f7;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .game-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #e3f2fd;
        text-shadow: 0 0 20px rgba(79, 195, 247, 0.3);
    }
    
    .game-status-bar {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .game-status-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(255,255,255,0.05);
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        border: 1px solid rgba(79,195,247,0.2);
        min-width: 80px;
    }
    
    .game-status-item .label {
        font-size: 0.6rem;
        text-transform: uppercase;
        color: #90a4ae;
        letter-spacing: 0.1em;
    }
    
    .game-status-item .value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .game-status-item .value.danger { color: #ef5350; }
    .game-status-item .value.warning { color: #ffb74d; }
    .game-status-item .value.success { color: #66bb6a; }
    
    .game-opponent-banner {
        background: linear-gradient(135deg, rgba(239,83,80,0.15), rgba(239,83,80,0.05));
        border: 2px solid #ef5350;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .game-opponent-banner .emoji {
        font-size: 2.5rem;
        line-height: 1;
    }
    
    .game-opponent-banner .title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ef5350;
    }
    
    .game-opponent-banner .subtitle {
        font-size: 0.8rem;
        color: #90a4ae;
    }
    
    .game-opponent-banner .quote {
        font-style: italic;
        color: #b0bec5;
        border-left: 3px solid #ef5350;
        padding-left: 1rem;
        margin-left: 0.5rem;
    }
    
    .game-choice-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin: 0.5rem 0 1rem 0;
    }
    
    .game-choice-card {
        background: rgba(10, 30, 45, 0.9);
        border: 1px solid rgba(79,195,247,0.2);
        border-radius: 12px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .game-choice-card:hover {
        border-color: #4fc3f7;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79,195,247,0.15);
    }
    
    .game-choice-card .emoji { font-size: 1.8rem; }
    .game-choice-card .label { font-weight: 600; color: #e3f2fd; margin: 0.3rem 0; }
    .game-choice-card .desc { font-size: 0.8rem; color: #90a4ae; }
    .game-choice-card .cost { 
        font-size: 0.7rem; 
        color: #ffb74d; 
        margin-top: 0.3rem;
        padding: 0.2rem 0.5rem;
        background: rgba(255,183,77,0.1);
        border-radius: 4px;
        display: inline-block;
    }
    
    .game-choice-card.selected {
        border-color: #4fc3f7;
        background: rgba(79,195,247,0.1);
        box-shadow: 0 0 30px rgba(79,195,247,0.1);
    }
    
    .game-choice-card.disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    .game-news-ticker {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(79,195,247,0.1);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        overflow: hidden;
    }
    
    .game-news-ticker .icon { font-size: 1.2rem; }
    .game-news-ticker .text { 
        color: #b0bec5; 
        font-size: 0.9rem;
        white-space: nowrap;
        animation: ticker-scroll 20s linear infinite;
    }
    
    @keyframes ticker-scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .game-objective-tracker {
        background: rgba(10, 30, 45, 0.6);
        border: 1px solid rgba(79,195,247,0.1);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
    }
    
    .game-objective-tracker .title {
        font-size: 0.7rem;
        text-transform: uppercase;
        color: #90a4ae;
        letter-spacing: 0.1em;
    }
    
    .game-objective-tracker .progress-bar {
        height: 6px;
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
        margin-top: 0.3rem;
        overflow: hidden;
    }
    
    .game-objective-tracker .progress-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    .game-objective-tracker .progress-fill.success { background: #66bb6a; }
    .game-objective-tracker .progress-fill.warning { background: #ffb74d; }
    .game-objective-tracker .progress-fill.danger { background: #ef5350; }
    
    .game-story-log {
        max-height: 200px;
        overflow-y: auto;
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    
    .game-story-log .entry {
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 0.3rem 0;
        display: flex;
        gap: 0.5rem;
    }
    
    .game-story-log .entry .time {
        color: #90a4ae;
        font-size: 0.7rem;
        min-width: 60px;
    }
    
    .game-story-log .entry .text { color: #e3f2fd; }
    .game-story-log .entry .text .highlight { color: #4fc3f7; font-weight: 600; }
    .game-story-log .entry .text .danger { color: #ef5350; }
    .game-story-log .entry .text .success { color: #66bb6a; }
    
    @media (max-width: 768px) {
        .game-choice-grid { grid-template-columns: 1fr; }
        .game-status-bar { gap: 0.5rem; }
        .game-status-item { min-width: 60px; padding: 0.2rem 0.5rem; }
        .game-status-item .value { font-size: 1rem; }
    }
    </style>
    """

def render_game_header():
    """Render the game header with status bar"""
    game = st.session_state.game
    state = load_state()
    
    # Determine status colors
    cap_gap = state.get("cap_gap", 50)
    if cap_gap < 35:
        gap_color = "success"
        gap_status = "STABLE"
    elif cap_gap < 55:
        gap_color = "warning"
        gap_status = "TENSE"
    else:
        gap_color = "danger"
        gap_status = "CRITICAL"
    
    # Alliance cohesion
    cohesion = game.get("alliance_cohesion", 70)
    if cohesion > 70:
        cohesion_color = "success"
    elif cohesion > 50:
        cohesion_color = "warning"
    else:
        cohesion_color = "danger"
    
    st.markdown(f"""
    <div class="game-header">
        <div class="game-title">🧊 WINTERSTORM 2030</div>
        <div class="game-status-bar">
            <div class="game-status-item">
                <span class="label">Turn</span>
                <span class="value" style="color:#4fc3f7;">{game['turn']}</span>
            </div>
            <div class="game-status-item">
                <span class="label">Cap Gap</span>
                <span class="value {gap_color}">{cap_gap}%</span>
            </div>
            <div class="game-status-item">
                <span class="label">Alliance</span>
                <span class="value {cohesion_color}">{cohesion}%</span>
            </div>
            <div class="game-status-item">
                <span class="label">Objective</span>
                <span class="value" style="color:#ffb74d;">{game.get('victory_countdown', 10)} turns</span>
            </div>
            <div class="game-status-item">
                <span class="label">Status</span>
                <span class="value {gap_color}">{gap_status}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_opponent_banner():
    """Render the AI opponent with personality"""
    game = st.session_state.game
    state = load_state()
    
    doctrine = state.get("doctrine", "rus")
    ai = AI_PERSONALITY.get(doctrine, AI_PERSONALITY["rus"])
    
    # Get appropriate quote based on game state
    cap_gap = state.get("cap_gap", 50)
    if cap_gap > 65:
        quote = ai["responses"].get("victory", "The Arctic belongs to those who dare.")
    elif cap_gap < 40:
        quote = ai["responses"].get("defeat", "A temporary setback. We are patient.")
    elif game.get("consecutive_wins", 0) >= 2:
        quote = ai["responses"].get("defensive", "You've countered this move. But the next one...")
    else:
        # Get random quote from available tactics
        tactic = random.choice(ai["tactics"])
        quote = ai["responses"].get(tactic, "We are merely exercising our rights.")
    
    st.markdown(f"""
    <div class="game-opponent-banner">
        <div class="emoji">{ai["emoji"]}</div>
        <div>
            <div class="title">{ai["name"]}</div>
            <div class="subtitle">{ai["title"]}</div>
        </div>
        <div class="quote">"{quote}"</div>
    </div>
    """, unsafe_allow_html=True)

def render_objectives():
    """Render the player's objectives with progress"""
    game = st.session_state.game
    state = load_state()
    
    # Primary objective
    cap_gap = state.get("cap_gap", 50)
    turns_remaining = game.get("victory_countdown", 10)
    primary_progress = min(100, (10 - turns_remaining) * 10)
    primary_color = "success" if cap_gap < 55 else "warning" if cap_gap < 65 else "danger"
    
    # Secondary objectives
    cohesion = game.get("alliance_cohesion", 70)
    cohesion_progress = min(100, (cohesion / 60) * 100)  # Target is 60%
    cohesion_color = "success" if cohesion > 60 else "warning" if cohesion > 40 else "danger"
    
    st.markdown(f"""
    <div class="game-objective-tracker">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div class="title">🎯 Primary Objective</div>
                <div style="font-weight:600;color:#e3f2fd;">Prevent NATO Article 4 Invocation</div>
                <div style="font-size:0.8rem;color:#90a4ae;">Keep Cap Gap below 75% for {turns_remaining} more turns</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.8rem;color:#90a4ae;">Progress</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;font-weight:700;color:#4fc3f7;">{primary_progress}%</div>
            </div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill {primary_color}" style="width:{primary_progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_game_choices():
    """Render the player's choices for the current turn"""
    game = st.session_state.game
    state = load_state()
    
    st.markdown("### 📋 Your Move")
    
    # Check if this is a narrative beat turn
    narrative_event = None
    for beat in NARRATIVE_BEATS:
        if f"turn_{game['turn']}" == beat["trigger"] and beat["trigger"] not in game.get("narrative_events_triggered", []):
            narrative_event = beat
            break
    
    if narrative_event:
        render_narrative_event(narrative_event)
        return
    
    # Regular turn choices
    choices = get_regular_choices(state, game)
    
    # Display choices in grid
    cols = st.columns(3)
    selected = None
    
    for i, choice in enumerate(choices):
        with cols[i % 3]:
            disabled = choice.get("disabled", False)
            st.markdown(f"""
            <div class="game-choice-card {'selected' if choice.get('selected') else ''} {'disabled' if disabled else ''}"
                 onclick="document.getElementById('choice_{i}').click()">
                <div class="emoji">{choice['emoji']}</div>
                <div class="label">{choice['label']}</div>
                <div class="desc">{choice['desc']}</div>
                <div class="cost">{choice.get('cost', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select", key=f"choice_{i}", use_container_width=True):
                selected = choice
                break
    
    return selected

def render_narrative_event(event):
    """Render a narrative event with choices"""
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(79,195,247,0.1),rgba(79,195,247,0.02));
                border:2px solid #4fc3f7;
                border-radius:12px;
                padding:1.5rem;
                margin:0.5rem 0 1rem 0;">
        <div style="font-size:0.7rem;text-transform:uppercase;color:#4fc3f7;letter-spacing:0.1em;">⚡ Narrative Event</div>
        <div style="font-size:1.3rem;font-weight:700;color:#e3f2fd;margin:0.3rem 0;">{event['title']}</div>
        <div style="color:#b0bec5;margin-bottom:1rem;">{event['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show choices for the event
    cols = st.columns(3)
    for i, choice in enumerate(event.get("choice", [])):
        with cols[i]:
            if st.button(f"{choice['label']}", key=f"narrative_{i}", use_container_width=True):
                return choice
    
    return None

def get_regular_choices(state, game):
    """Generate regular turn choices based on current game state"""
    cap_gap = state.get("cap_gap", 50)
    doctrine = state.get("doctrine", "rus")
    turn = game["turn"]
    
    choices = [
        {
            "emoji": "🛡️",
            "label": "Increase Patrols",
            "desc": "Authorize additional NATO patrols in the GIUK gap",
            "cost": "Cost: +2% tension",
            "action": "patrol",
            "effect": {"cap_gap": -5, "tension": 2}
        },
        {
            "emoji": "🤝",
            "label": "Offer Concession",
            "desc": "Offer access or resource concessions to de-escalate",
            "cost": "Cost: Alliance cohesion -3%",
            "action": "concession",
            "effect": {"cap_gap": -8, "cohesion": -3}
        },
        {
            "emoji": "📢",
            "label": "Public Statement",
            "desc": "Issue a public statement condemning provocative actions",
            "cost": "Cost: +4% narrative pressure",
            "action": "statement",
            "effect": {"cap_gap": -3, "narrative": 4}
        }
    ]
    
    # Add doctrine-specific choices
    if doctrine == "rus":
        choices.append({
            "emoji": "🔍",
            "label": "Intel Op",
            "desc": "Deploy intelligence assets to monitor Russian movements",
            "cost": "Cost: 1 turn of reduced response",
            "action": "intel",
            "effect": {"cap_gap": -4, "next_turn_boost": 3}
        })
    else:
        choices.append({
            "emoji": "⚖️",
            "label": "Legal Challenge",
            "desc": "File a formal legal challenge to China's Arctic claims",
            "cost": "Cost: +6% diplomatic friction",
            "action": "legal",
            "effect": {"cap_gap": -6, "diplomatic": 6}
        })
    
    # Add unlocked abilities if available
    for unlock_turn, ability in UNLOCKABLES.items():
        if int(unlock_turn.split("_")[1]) <= turn:
            if ability["name"] not in game.get("used_abilities", []):
                choices.append({
                    "emoji": "🌟",
                    "label": ability["name"],
                    "desc": ability["description"],
                    "cost": "⭐ Unlocked!",
                    "action": "ability",
                    "effect": {"ability": ability["name"]},
                    "is_ability": True
                })
    
    # Limit choices to 4-5 for readability
    return choices[:5]

def process_player_move(state, game, choice):
    """Process the player's choice and update game state"""
    if not choice:
        return
    
    effect = choice.get("effect", {})
    
    # Apply cap gap changes
    if "cap_gap" in effect:
        # Update domains
        domains = state["domains"]
        for d in domains:
            d["gap"] = max(0, min(100, d["gap"] + effect["cap_gap"]))
        state = recompute_cap_gap(state)
    
    # Apply narrative modifier
    if "narrative" in effect:
        state["narrative_modifier"] = max(-15, min(15, state.get("narrative_modifier", 0) + effect["narrative"]))
        state = recompute_cap_gap(state)
    
    # Apply alliance cohesion changes
    if "cohesion" in effect:
        game["alliance_cohesion"] = max(0, min(100, game["alliance_cohesion"] + effect["cohesion"]))
    
    # Apply diplomatic friction
    if "diplomatic" in effect:
        game["diplomatic_friction"] = game.get("diplomatic_friction", 0) + effect["diplomatic"]
    
    # Handle ability usage
    if choice.get("is_ability"):
        game["used_abilities"].append(choice["label"])
    
    # Track AI response
    game["consecutive_wins"] = 0
    game["consecutive_losses"] = 0
    
    # Log the action
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": f"<span class='highlight'>{choice['label']}</span> — {choice['desc']}"
    }
    game["story_log"].insert(0, log_entry)
    
    # Save state
    save_state(state)
    st.session_state.game = game

def process_ai_move(state, game):
    """Process the AI's response with personality"""
    doctrine = state.get("doctrine", "rus")
    ai = AI_PERSONALITY.get(doctrine, AI_PERSONALITY["rus"])
    
    # Determine AI's tactical choice based on game state
    cap_gap = state.get("cap_gap", 50)
    cohesion = game.get("alliance_cohesion", 70)
    
    # Adaptive AI behavior
    if cap_gap < 40:
        # AI is losing - escalate aggressively
        tactic = random.choice(["escalate", "hybrid"])
        delta = random.randint(6, 10)
        game["ai_current_mood"] = "aggressive"
    elif cap_gap > 65:
        # AI is winning - press advantage
        tactic = random.choice(ai["tactics"][:2])
        delta = random.randint(3, 6)
        game["ai_current_mood"] = "confident"
    else:
        # Balanced - mixed approach
        tactic = random.choice(ai["tactics"])
        delta = random.randint(2, 5)
        game["ai_current_mood"] = "neutral"
    
    # Apply AI move effect
    domains = state["domains"]
    affected_domain = random.choice(domains)
    affected_domain["gap"] = max(0, min(100, affected_domain["gap"] + delta))
    state = recompute_cap_gap(state)
    
    # Track AI tactic
    game["ai_used_tactics"].append(tactic)
    
    # Generate AI response text
    response = ai["responses"].get(tactic, "We are merely exercising our rights.")
    
    # Log AI move
    log_entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": f"<span class='danger'>⚡ {ai['name']}: {response}</span>"
    }
    game["story_log"].insert(0, log_entry)
    
    # Check for narrative events
    check_narrative_events(state, game)
    
    # Update victory countdown
    game["victory_countdown"] = max(0, game["victory_countdown"] - 1)
    
    # Save state
    save_state(state)
    st.session_state.game = game
    
    return state, game

def check_narrative_events(state, game):
    """Check if any narrative events should trigger"""
    turn = game["turn"]
    
    for beat in NARRATIVE_BEATS:
        trigger = beat["trigger"]
        if trigger.startswith("turn_") and int(trigger.split("_")[1]) == turn:
            if beat["trigger"] not in game.get("narrative_events_triggered", []):
                # Store the event for display
                game["pending_narrative_event"] = beat
                game["narrative_events_triggered"].append(beat["trigger"])
                st.session_state.game = game
                return True
    
    return False

def render_game_result():
    """Render victory or defeat screen"""
    game = st.session_state.game
    state = load_state()
    
    cap_gap = state.get("cap_gap", 50)
    turns_remaining = game.get("victory_countdown", 10)
    
    # Check win/loss conditions
    if cap_gap >= 75:
        defeat_reason = "NATO Cap Gap exceeded 75%"
        result = "defeat"
    elif turns_remaining <= 0 and cap_gap < 75:
        result = "victory"
    else:
        return None
    
    # Render result
    if result == "victory":
        st.balloons()
        st.markdown("""
        <div style="text-align:center;padding:3rem;background:linear-gradient(135deg,rgba(102,187,106,0.1),rgba(102,187,106,0.02));
                    border:3px solid #66bb6a;border-radius:16px;margin:1rem 0;">
            <div style="font-size:4rem;">🏆</div>
            <div style="font-size:2rem;font-weight:700;color:#66bb6a;">VICTORY</div>
            <div style="font-size:1.2rem;color:#e3f2fd;margin:1rem 0;">
                You successfully prevented NATO Article 4 invocation in the High North.
            </div>
            <div style="color:#90a4ae;">
                Alliance Cohesion: {game['alliance_cohesion']}%<br>
                Turns Survived: {game['turn']}<br>
                Arctic Stability: SECURE
            </div>
        </div>
        """.format(game=game), unsafe_allow_html=True)
    else:
        st.snow()
        st.markdown("""
        <div style="text-align:center;padding:3rem;background:linear-gradient(135deg,rgba(239,83,80,0.1),rgba(239,83,80,0.02));
                    border:3px solid #ef5350;border-radius:16px;margin:1rem 0;">
            <div style="font-size:4rem;">💀</div>
            <div style="font-size:2rem;font-weight:700;color:#ef5350;">DEFEAT</div>
            <div style="font-size:1.2rem;color:#e3f2fd;margin:1rem 0;">
                {defeat_reason}
            </div>
            <div style="color:#90a4ae;">
                Alliance Cohesion: {game['alliance_cohesion']}%<br>
                Turns Survived: {game['turn']}<br>
                Arctic Stability: COLLAPSED
            </div>
        </div>
        """.format(game=game, defeat_reason=defeat_reason), unsafe_allow_html=True)
    
    if st.button("🔄 Play Again", type="primary"):
        reset_game()
        st.rerun()
    
    return result

def render_story_log():
    """Render the story log with recent events"""
    game = st.session_state.game
    log = game.get("story_log", [])
    
    if not log:
        return
    
    st.markdown("### 📜 Story Log")
    st.markdown('<div class="game-story-log">', unsafe_allow_html=True)
    
    for entry in log[:10]:  # Show last 10 entries
        st.markdown(f"""
        <div class="entry">
            <div class="time">{entry['time']}</div>
            <div class="text">{entry['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_game_controls():
    """Render the game control buttons"""
    game = st.session_state.game
    state = load_state()
    
    # Check if player has moved this turn
    has_moved = game.get("turn_action_taken", False)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.caption("💡 Tip: Your choices affect the Cap Gap and alliance cohesion.")
    
    with col2:
        if not has_moved:
            if st.button("⏳ End Turn", type="primary", use_container_width=True):
                # Process AI move
                process_ai_move(state, game)
                game["turn"] = game["turn"] + 1
                st.session_state.game = game
                st.rerun()
        else:
            st.button("⏳ Turn Complete", disabled=True, use_container_width=True)
    
    with col3:
        if st.button("💾 Save & Exit", use_container_width=True):
            st.success("Game saved!")

def reset_game():
    """Reset the game state"""
    if "game" in st.session_state:
        del st.session_state.game
    init_game_state()

# ============================================
# MAIN GAME UI
# ============================================

def game_ui():
    """Main game UI renderer"""
    
    # Apply game CSS
    st.markdown(game_css(), unsafe_allow_html=True)
    
    # Initialize game state
    init_game_state()
    game = st.session_state.game
    
    # Load current state
    state = load_state()
    
    # Check for game result
    result = render_game_result()
    if result:
        return
    
    # Render header
    render_game_header()
    
    # Render opponent banner
    render_opponent_banner()
    
    # Render objectives
    render_objectives()
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Player choices
        choice = render_game_choices()
        
        if choice:
            process_player_move(state, game, choice)
            game["turn_action_taken"] = True
            st.session_state.game = game
            st.rerun()
        
        # Game controls
        render_game_controls()
    
    with col2:
        # Story log
        render_story_log()
    
    # Show game stats in an expandable section
    with st.expander("📊 Game Statistics"):
        st.markdown(f"""
        **Turn:** {game['turn']}  
        **Cap Gap:** {state.get('cap_gap', 50)}%  
        **Alliance Cohesion:** {game.get('alliance_cohesion', 70)}%  
        **AI Mood:** {game.get('ai_current_mood', 'neutral').title()}  
        **Victory Countdown:** {game.get('victory_countdown', 10)} turns  
        **AI Tactics Used:** {', '.join(game.get('ai_used_tactics', [])[:5]) or 'None yet'}  
        **Abilities Unlocked:** {len(game.get('unlocked_abilities', []))}  
        **Abilities Used:** {len(game.get('used_abilities', []))}  
        """)

# ============================================
# BACKEND INTEGRATION
# ============================================

# These functions are from the original app - kept for compatibility
def load_state():
    """Load the current game state from JSONBin"""
    # Same as original load_state() function
    from app import load_state as original_load
    return original_load()

def save_state(state):
    """Save the current game state to JSONBin"""
    from app import save_state as original_save
    return original_save(state)

def recompute_cap_gap(state):
    """Recompute the Cap Gap from domain scores"""
    from app import recompute_cap_gap as original_recompute
    return original_recompute(state)

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    # Check authentication first
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please log in to play WinterStorm2030.")
        st.stop()
    
    # Show game mode toggle
    mode = st.sidebar.radio(
        "Mode",
        ["🎮 Game Mode", "📊 Analyst Mode"],
        index=0
    )
    
    if mode == "🎮 Game Mode":
        game_ui()
    else:
        # Original analyst mode
        st.info("Switching to Analyst Mode...")
        # The original app's UI would go here
        st.warning("Analyst Mode content goes here.")
