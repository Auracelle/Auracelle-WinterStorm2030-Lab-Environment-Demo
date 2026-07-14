# WinterStorm2030

NATO STO SAS-219 — High North Scenarios for Wargaming & Analysis. A governance capacity
instrument for asynchronous grey-zone wargaming: participants trade concessions, trigger
Agentic AI Red Team moves, and run cases through an Arbitration Track, with every action
visible to every participant through a shared move log.

## Repository structure
```
.
├── app.py                          # everything — login gate + instrument, one file
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example        # template — copy to secrets.toml locally, never commit the real one
```

## Why JSONBin.io
This went through two earlier backends: Google Sheets (blocked by an org policy against
service-account key creation) and Supabase (works, but needs a SQL Editor step to create
tables). JSONBin.io needs neither — it's one JSON document behind one API key. Simplest
setup path of the three, at the cost of being a less "serious" database (fine for a
turn-based async demo; would not be the choice for high-concurrency or long-term use).

## 1. Create your JSONBin.io account and bin
1. Go to jsonbin.io → sign up (free tier is enough for this).
2. Dashboard → "Create Bin".
3. Paste this exact starter JSON as the bin's content:
```json
{
  "state": {"turn": 1, "cap_gap": 64, "concession_modifier": 0, "narrative_modifier": 0, "doctrine": "rus", "scenario_name": "", "scenario_desc": "", "treaty_flag": false, "win_win_active": false},
  "log": [],
  "arbitration": []
}
```
4. Save. Copy the **Bin ID** shown (also visible in the URL when viewing the bin).
5. Go to "API Keys" in the left sidebar → copy your **X-Master-Key**.

## 2. Add credentials
**Local:**
```
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Fill in `bin_id` and `master_key` with the values from step 1. This file is gitignored.

**Streamlit Community Cloud:** app dashboard → Settings → Secrets → paste the same TOML
content (with real values) there instead.

## 3. Run
```
pip install -r requirements.txt
streamlit run app.py
```
Login: callsign `SAS219`, access code `WinterStorm2030!`

## How the async multiplayer works
No live push/websocket — each participant's page reads the shared JSONBin document on load
and after every action. Sufficient for asynchronous play (take a turn, log off; next person
opens the link, hits Refresh, sees it) but not simultaneous real-time viewing.

## Known trade-offs of this backend
- **Free-tier rate limits** — JSONBin's free tier caps requests per minute. Fine for a small
  pilot group taking turns; would need a paid tier for a larger/faster-moving session.
- **Whole-document overwrite** — every write replaces the entire JSON document. If two people
  submit an action in the same instant, one write can be lost. Low risk for genuinely
  asynchronous, turn-based play; a real risk if several people click simultaneously.
- **No schema/validation** — unlike Supabase, nothing enforces the JSON's shape. A malformed
  manual edit to the bin could break the app; don't hand-edit the bin content directly.

## Scope note
This build ports the core loop — Concession Engine, Agentic AI Red Team moves (doctrine-based
move library, no live LLM call), and the Arbitration Track. It does not include the DM/DS mode
split, OSINT/Hormuz calibration, the 5-domain Cap Gap breakdown, or the visual effects from the
standalone HTML build — those were out of scope for the async-visibility goal and would need a
second pass.
