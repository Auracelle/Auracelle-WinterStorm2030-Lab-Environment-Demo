# WinterStorm2030

NATO STO SAS-219 — High North Scenarios for Wargaming & Analysis. A governance capacity
instrument for asynchronous grey-zone wargaming: participants trade concessions, trigger
Agentic AI Red Team moves, and run cases through an Arbitration Track, with every action
visible to every participant through a shared move log.

## Repository structure
```
.
├── app.py                          # everything — login gate + instrument, one file
├── supabase_setup.sql              # run once in Supabase's SQL Editor to create tables
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example        # template — copy to secrets.toml locally, never commit the real one
```

## Why Supabase instead of Google Sheets
This originally used Google Sheets via a service-account key. Some Google Workspace/Cloud
organizations enforce an Org Policy (`iam.disableServiceAccountKeyCreation`) that blocks
creating those keys entirely — if that's your situation, Google Sheets isn't usable without
an administrator lifting the policy. Supabase authenticates with a plain API key instead of
a downloadable service-account credential, so that specific organizational block doesn't apply.

## 1. Create a Supabase project
1. Go to supabase.com → sign up (free tier is enough for this) → "New Project".
2. Once it's provisioned, go to the **SQL Editor** (left sidebar) → "New query".
3. Paste in the entire contents of `supabase_setup.sql` from this repo → click **Run**.
   This creates the three tables (`ws_state`, `ws_log`, `ws_arbitration`) with permissive
   Row Level Security policies (see Security notes below).

## 2. Get your API credentials
1. In your Supabase project, go to **Settings → API**.
2. Copy the **Project URL**.
3. Copy the **anon public** key (NOT the `service_role` key — see security note below).

## 3. Add credentials
**Local:**
```
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Fill in the `url` and `key` fields with the values from step 2. This file is gitignored.

**Streamlit Community Cloud:** app dashboard → Settings → Secrets → paste the same TOML
content (with real values) there instead.

## 4. Run
```
pip install -r requirements.txt
streamlit run app.py
```
Login: callsign `SAS219`, access code `WinterStorm2030!`

## How the async multiplayer works
No live push/websocket — each participant's page reads the shared Supabase tables on load
and after every action. Sufficient for asynchronous play (take a turn, log off; next person
opens the link, hits Refresh, sees it) but not simultaneous real-time viewing.

## Security notes
- Use the **anon** key, not `service_role`. The anon key is scoped by Row Level Security
  policies (defined in `supabase_setup.sql`); `service_role` bypasses RLS entirely and
  should never be embedded in a client-facing app.
- This app has no per-participant authentication — everyone shares one access code and one
  Supabase project. Anyone with the link and access code can read/write shared state. See
  `SECURITY.md` for more detail.
- Unclassified use only. See `SECURITY.md` for scope.

## Scope note
This build ports the core loop — Concession Engine, Agentic AI Red Team moves (doctrine-based
move library, no live LLM call), and the Arbitration Track. It does not include the DM/DS mode
split, OSINT/Hormuz calibration, the 5-domain Cap Gap breakdown, or the visual effects from the
standalone HTML build — those were out of scope for the async-visibility goal and would need a
second pass.
