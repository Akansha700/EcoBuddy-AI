import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EcoBuddy AI",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# NAVIGATION
# -----------------------------
pages = {
    "🏠 Main": [
        st.Page(
            "app_home.py",
            title="Home",
            icon="🏠"
        ),
        st.Page(
            "pages/about.py",
            title="About EcoBuddy",
            icon="ℹ️"
        ),
    ],

    "⚡ Energy": [
        st.Page(
            "pages/energy_predictor.py",
            title="Energy Predictor",
            icon="⚡"
        ),
        st.Page(
            "pages/ai_advisor.py",
            title="AI Energy Advisor",
            icon="🤖"
        ),
        st.Page(
            "pages/energy_analytics.py",
            title="Energy Analytics",
            icon="📊"
        ),
    ],

    "🌱 Sustainability": [
        st.Page(
            "pages/carbon_calculator.py",
            title="Carbon Footprint",
            icon="🌍"
        ),
        st.Page(
            "pages/waste_assistant.py",
            title="Waste Assistant",
            icon="♻️"
        ),
        st.Page(
            "pages/water_advisor.py",
            title="Water Advisor",
            icon="💧"
        ),
        st.Page(
            "pages/eco_products.py",
            title="Eco Products",
            icon="🛍️"
        ),
    ],

    "🤖 AI Assistant": [
        st.Page(
            "pages/chatbot.py",
            title="EcoBuddy Chatbot",
            icon="💬"
        ),
    ],
}

# -----------------------------
# RUN NAVIGATION
# -----------------------------
pg = st.navigation(pages)

pg.run()