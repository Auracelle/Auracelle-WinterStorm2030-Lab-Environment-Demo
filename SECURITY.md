# Security Policy

## Reporting a Vulnerability
If you discover a security issue in this repository or the deployed WinterStorm2030
application, please report it privately rather than opening a public GitHub issue.
Contact Grace-Alice Evans directly (Auracelle AI Governance Labs LLC) with:
- A description of the issue
- Steps to reproduce, if applicable
- Any relevant logs or screenshots (with credentials/secrets redacted)

Please allow a reasonable window to address the issue before any public disclosure.

## Scope
This application is an unclassified research and demonstration instrument built for
NATO STO SAS-219 (High North Scenarios for Wargaming & Analysis). It is **not** intended
to process, store, or transmit classified information of any kind. Do not enter classified,
export-controlled, or otherwise sensitive real-world operational data into this application.

## Credential Handling
This app authenticates to Google Sheets via a service account credential, provided through
Streamlit secrets (`.streamlit/secrets.toml` locally, or the Secrets panel on Streamlit
Community Cloud). This credential must **never** be committed to the repository.

- `.streamlit/secrets.toml` is excluded via `.gitignore` — do not remove that entry.
- Only `.streamlit/secrets.toml.example` (a template with placeholder values) should ever
  be committed.
- If a real credential is accidentally committed at any point, treat it as compromised:
  revoke/rotate the key immediately in Google Cloud Console (IAM & Admin → Service Accounts),
  then scrub it from git history before continuing use of the repo.
- The shared application access code (`WinterStorm2030!`) is a session gate for
  participant convenience, not a security control. Do not rely on it to protect sensitive
  information — see Scope above.

## Known Limitations
- No per-user authentication — all participants share one access code and one Google Sheet.
  Anyone with the link and access code can read and write shared session state.
- The Google Sheet backing this app should be shared only with the service account and
  intended participants, and reviewed periodically for unintended access.
