import streamlit as st

st.set_page_config(page_title="WinterStorm2030 | Login", layout="wide")

st.markdown('''
<style>
.stApp {
    background: linear-gradient(135deg, #0a1822 0%, #16303f 100%);
}
/* 3D Shadow Bevel Buttons — matches Auracelle Bach styling */
.stButton > button {
    background: #0ed7c4 !important;
    color: #0a1822 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    box-shadow:
        0 4px 0 #0ba894,
        0 4px 8px rgba(0, 0, 0, 0.35) !important;
    transition: all 0.1s ease !important;
    position: relative !important;
    top: 0 !important;
}
.stButton > button:hover {
    background: #15e8d4 !important;
    box-shadow:
        0 4px 0 #0ba894,
        0 4px 10px rgba(0, 0, 0, 0.4) !important;
}
.stButton > button:active {
    top: 4px !important;
    box-shadow:
        0 0 0 #0ba894,
        0 2px 4px rgba(0, 0, 0, 0.35) !important;
}
</style>
''', unsafe_allow_html=True)

st.title("🧊 WinterStorm2030")
st.subheader("NATO STO SAS-219 — High North Scenarios for Wargaming & Analysis")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    with st.form("login_form"):
        callsign = st.text_input("Callsign")
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
            st.session_state["callsign"] = callsign or "PARTICIPANT"
            st.success("✅ Authentication successful!")
            st.rerun()
        else:
            st.error("❌ Access Denied — Credentials Not Recognized")
            st.stop()
else:
    st.switch_page("pages/simulation.py")
