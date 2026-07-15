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

## Async and synchronous play
The same shared backend supports both — the only difference is whether the page refreshes
itself:
- **Async (default):** participants take turns on their own schedule, clicking "🔄 Refresh
  Shared State" to see others' activity when they return.
- **Live Mode (toggle at the top of the app):** the page auto-refreshes every 15 seconds,
  for a facilitated session where a room is watching moves land in near-real-time. Turn
  this off for solo/async play — see the rate-limit trade-off below.

## How the async multiplayer works
No live push/websocket — even in Live Mode, this is polling (checking every 15s), not a
true real-time push. Sufficient for a facilitated session; if two people submit an action
in the exact same instant, see "Known trade-offs" below.

## Known trade-offs of this backend
- **Free-tier rate limits** — JSONBin's free tier caps requests per minute. Fine for a small
  pilot group taking turns; would need a paid tier for a larger/faster-moving session.
  **This matters more in Live Mode**: every participant's browser auto-polls every 15
  seconds, so a room of several people in Live Mode generates meaningfully more requests
  than async play. If you're running a live facilitated session on the 21st and hit rate
  limits, either raise the interval in `app.py` (`st_autorefresh(interval=15000, ...)` —
  try 30000 or higher) or upgrade the JSONBin tier for that day.
- **Whole-document overwrite** — every write replaces the entire JSON document. If two people
  submit an action in the same instant, one write can be lost. Low risk for genuinely
  asynchronous, turn-based play; a real risk if several people click simultaneously — which
  is more likely in Live Mode than async.
- **No schema/validation** — unlike Supabase, nothing enforces the JSON's shape. A malformed
  manual edit to the bin could break the app; don't hand-edit the bin content directly.

## Decision-Maker / Decision-Support mode
A radio toggle near the top switches between:
- **Decision-Maker (breadth):** read-only Scenario Setup; Actor Analysis, Concession Engine,
  NATO Cap Gap (composite + domain table, no manual adjustment), OSINT Feed, and Shared Move
  Log all visible and usable.
- **Decision-Support (full depth):** adds editable Scenario Setup, manual per-domain Cap Gap
  adjustment, and the Arbitration Track (the multi-stage escalation ladder).

This is an adapted mapping, not a full port of the HTML build's DM/DS split — the HTML
version also differentiates Cognitive Warfare and Narrative Analysis, which this build
doesn't have yet (see Scope note below).

## Scope note
This build now includes: Concession Engine, Agentic AI Red Team moves (doctrine-based move
library, no live LLM call), the Arbitration Track, an Actor Analysis reference table, a
5-domain NATO Capability Gap breakdown, and an OSINT Feed (real GDELT event data, no API
key, no LLM call) with a Strait of Hormuz calibration baseline kept structurally separate
from the live Arctic Cap Gap. It does not include the Cognitive Warfare Module, Narrative
Analysis, the Governance Lab's treaty-structuring content, or the visual effects (tilt,
glow, 3D map, scanline) from the standalone HTML build — those still require either a
cleared LLM channel or are visual-only and don't affect the async-multiplayer goal.
