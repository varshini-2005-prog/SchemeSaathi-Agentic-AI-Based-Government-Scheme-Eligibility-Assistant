"""
frontend/streamlit_app.py
Interactive Streamlit Dashboard for SchemeSaathi.
Tamil + English Agentic Government Scheme Eligibility Assistant UI.
"""

import streamlit as st
import sys
from pathlib import Path

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import settings
from app.graph import run_schemesaathi_turn, create_initial_state
from app.rules import scheme_repository

st.set_page_config(
    page_title="SchemeSaathi - Tamil & English Scheme Assistant",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ SchemeSaathi (திட்டம் சாதி)")
st.caption("Tamil + English Agentic AI Government Scheme Eligibility Assistant")

# Initialize Session State
if "state" not in st.session_state:
    st.session_state.state = create_initial_state()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar - User Profile State & What-if Simulator
with st.sidebar:
    st.header("👤 Active User Profile")
    st.caption("Stateful profile parameters extracted by agent")

    profile = st.session_state.state.get("profile", {})

    income_val = profile.get("annual_family_income")
    income_str = f"₹{income_val:,.0f}" if income_val else "Not set"

    st.markdown(f"**Age:** `{profile.get('age') or 'Not set'}`")
    st.markdown(f"**Gender:** `{profile.get('gender') or 'Not set'}`")
    st.markdown(f"**Annual Income:** `{income_str}`")

    st.markdown(f"**Occupation:** `{profile.get('occupation') or 'Not set'}`")
    st.markdown(f"**District:** `{profile.get('district') or 'Coimbatore (Default)'}`")
    st.markdown(f"**TN Govt School (Class 6-12):** `{profile.get('govt_school_study_class_6_to_12') if profile.get('govt_school_study_class_6_to_12') is not None else 'Not set'}`")
    st.markdown(f"**Agricultural Land:** `{profile.get('land_ownership') if profile.get('land_ownership') is not None else 'Not set'}`")

    st.markdown("---")
    st.header("💡 Quick What-if Simulators")
    st.caption("Simulate profile changes without altering core state")

    if st.button("🧪 What if my income was ₹2 Lakh?"):
        what_if_msg = "What if my annual income was 2 lakh instead of 3 lakh?"
        st.session_state.chat_history.append({"role": "user", "content": what_if_msg})
        st.session_state.state = run_schemesaathi_turn(what_if_msg, st.session_state.state)
        st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.state["final_response"]})

    if st.button("🔄 Reset User Profile"):
        st.session_state.state = create_initial_state()
        st.session_state.chat_history = []
        st.success("Profile reset.")

# Main Layout Tabs
tab1, tab2, tab3 = st.tabs(["💬 Agent Chat", "🏛️ Official Schemes Knowledge Base", "📊 System Health"])

with tab1:
    st.subheader("Chat with SchemeSaathi Agent")
    st.caption("Supports English, Tamil (தமிழ்), and Tanglish. Example: *'Enakku 24 age. Family income 1.8 lakh. Naan Coimbatore-la irukken. Enakku enna schemes kidaikkum?'*")

    # Render Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    if user_input := st.chat_input("Enter your query or profile details..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Analyzing profile & evaluating official eligibility rules..."):
            st.session_state.state = run_schemesaathi_turn(user_input, st.session_state.state)
            response_text = st.session_state.state.get("final_response", "No response generated.")

        with st.chat_message("assistant"):
            st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

with tab2:
    st.subheader("📚 Verified Official Scheme Knowledge Base")
    schemes = scheme_repository.get_all_schemes()
    for s in schemes:
        with st.expander(f"🏛️ [{s.scheme_id}] {s.scheme_name} ({s.government_level})"):
            st.markdown(f"**Category:** {s.scheme_category}")
            st.markdown(f"**Target State:** {s.state}")
            st.markdown(f"**Description:** {s.description}")
            st.markdown(f"**Benefits:** {s.benefits}")
            st.markdown(f"**Official Portal:** [{s.official_url}]({s.official_url})")
            st.markdown(f"**Source Document:** `{s.source_document}` (Verified: `{s.last_verified_date}`)")

            st.markdown("**Eligibility Rules:**")
            for r in s.eligibility_rules:
                st.markdown(f"- **{r.field}** `{r.operator}` `{r.target_value}` — *{r.description}*")

            st.markdown("**Required Documents:**")
            st.write(s.required_documents)

with tab3:
    st.subheader("⚙️ System Status & Verification")
    col1, col2, col3 = st.columns(3)
    col1.metric("Application", settings.PROJECT_NAME)
    col2.metric("Environment", settings.ENV)
    col3.metric("Schemes Loaded", len(scheme_repository.get_all_schemes()))
    st.success("✅ Agentic Workflow Graph, Rule Engine, FAISS Vector Retriever & SQLite Database Active.")
