# WinterStorm2030

NATO STO SAS-219 — High North Scenarios for Wargaming & Analysis. A governance capacity
instrument for asynchronous grey-zone wargaming: participants trade concessions, trigger
Agentic AI Red Team moves, and run cases through an Arbitration Track, with every action
visible to every participant through a shared move log.

## Repository structure
```
.
├── app.py                          # login gate
├── pages/
│   └── simulation.py               # the instrument
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example        # template — copy to secrets.toml locally, never commit the real one
```

## 1. Create the shared Google Sheet
1. Go to sheets.google.com → create a new spreadsheet.
2. Rename it exactly: `WinterStorm2030_Session` (must match `SHEET_NAME` in `pages/simulation.py`).
3. Leave it empty — the app creates the `state`, `log`, and `arbitration` tabs automatically on first run.

## 2. Create a Google service account (one-time)
1. console.cloud.google.com → create or reuse a project.
2. Enable the **Google Sheets API** and **Google Drive API** for that project.
3. IAM & Admin → Service Accounts → Create Service Account (any name, e.g. `winterstorm-sheets`).
4. Open it → Keys → Add Key → Create new key → JSON. Downloads a `.json` file — keep this private.
5. Copy the `client_email` field from that JSON (looks like `...@your-project.iam.gserviceaccount.com`).
6. Open the `WinterStorm2030_Session` sheet → Share → paste that email in → give it **Editor** access.

## 3. Add credentials
**Local:**
```
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Then fill in every field from your downloaded JSON key file. `.streamlit/secrets.toml` is gitignored — it will never be committed.

**Streamlit Community Cloud:** app dashboard → Settings → Secrets → paste the same TOML content (with real values) there instead.

## 4. Run
```
pip install -r requirements.txt
streamlit run app.py
```
Login: callsign `SAS219`, access code `WinterStorm2030!`

## How the async multiplayer works
No live push/websocket — each participant's page reads the shared Google Sheet on load and
after every action. Genuinely sufficient for asynchronous play (take a turn, log off; next
person opens the link, hits Refresh, sees it) but **not** simultaneous real-time viewing.

## Scope note
This build ports the core loop — Concession Engine, Agentic AI Red Team moves (doctrine-based
move library, no live LLM call, consistent with the May security constraint), and the
Arbitration Track. It does not include the DM/DS mode split, OSINT/Hormuz calibration, the
5-domain Cap Gap breakdown, or the visual effects from the standalone HTML build — those were
out of scope for the async-visibility goal and would need a second pass.
