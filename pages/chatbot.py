import streamlit as st
import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="EcoBuddy AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
URL = os.getenv("IBM_URL")

# =====================================================
# IBM CREDENTIALS
# =====================================================

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

parameters = {
    "decoding_method": "greedy",
    "temperature": 0.4,
    "max_new_tokens": 700,
    "min_new_tokens": 80,
    "repetition_penalty": 1.05
}

model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials=credentials,
    project_id=PROJECT_ID,
    params=parameters
)

# =====================================================
# READ DATABASE
# =====================================================

try:

    conn = sqlite3.connect("database/ecobuddy.db")

    carbon_df = pd.read_sql_query(
        "SELECT * FROM carbon_data ORDER BY id DESC LIMIT 1",
        conn
    )

    water_df = pd.read_sql_query(
        "SELECT * FROM water_data ORDER BY id DESC LIMIT 1",
        conn
    )

    energy_df = pd.read_sql_query(
        "SELECT * FROM energy_data ORDER BY id DESC LIMIT 1",
        conn
    )

    conn.close()

except:

    carbon_df = pd.DataFrame()

    water_df = pd.DataFrame()

    energy_df = pd.DataFrame()

# =====================================================
# LATEST VALUES
# =====================================================

carbon = (
    carbon_df["emission"].iloc[0]
    if not carbon_df.empty
    else 0
)

water = (
    water_df["daily"].iloc[0]
    if not water_df.empty
    else 0
)

energy = (
    energy_df["units"].iloc[0]
    if not energy_df.empty
    else 0
)

# =====================================================
# ECO SCORE
# =====================================================

eco_score = max(
    0,
    min(
        100,
        100 - (carbon / 5)
    )
)

# =====================================================
# ECO LEVEL
# =====================================================

def eco_level(score):

    if score >= 90:
        return "🌍 Planet Hero"

    elif score >= 75:
        return "🌳 Green Champion"

    elif score >= 60:
        return "🌿 Eco Friendly"

    else:
        return "🌱 Beginner"

level = eco_level(eco_score)

# =====================================================
# TITLE
# =====================================================

st.title("🤖 EcoBuddy AI")

st.caption(
    "Powered by IBM watsonx.ai"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🌱 EcoBuddy AI")

    st.success(level)

    st.metric(
        "🌍 Carbon",
        f"{carbon:.2f} kg"
    )

    st.metric(
        "💧 Water",
        f"{water:.0f} L/day"
    )

    st.metric(
        "⚡ Energy",
        f"{energy:.0f} kWh"
    )

    st.metric(
        "🌱 Eco Score",
        f"{eco_score:.0f}/100"
    )

    st.divider()

    st.info("""
Ask anything about

🌍 Climate Change

♻ Recycling

💧 Water Conservation

⚡ Energy Saving

🚗 Carbon Footprint

🌱 Sustainable Living

📖 SDGs
""")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input(
    "Ask EcoBuddy AI anything..."
)

if prompt:

    # ---------------- USER MESSAGE ---------------- #

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- AI RESPONSE ---------------- #

    with st.chat_message("assistant"):

        with st.spinner("🌱 EcoBuddy is analyzing your sustainability data..."):

            system_prompt = f"""
You are EcoBuddy AI.

You are an intelligent Sustainability Assistant.

You have access to the user's latest sustainability report.

-------------------------------------

LATEST USER DATA

Carbon Footprint:
{carbon:.2f} kg CO₂

Daily Water Usage:
{water:.0f} Litres

Monthly Energy Usage:
{energy:.2f} kWh

Eco Score:
{eco_score:.0f}/100

Eco Level:
{level}

-------------------------------------

Instructions:

1. Read the user's sustainability data.
2. Personalize every answer.
3. Mention their latest carbon, water and energy values whenever relevant.
4. If the user asks for improvement, give at least five personalized recommendations.
5. Explain concepts in simple language.
6. Use headings.
7. Use bullet points.
8. Never stop mid-sentence.
9. End every answer with an encouraging eco-friendly tip.

User Question:

{prompt}
"""

            try:

                response = model.generate_text(
                    prompt=system_prompt
                )

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                st.error(
                    f"IBM AI Error:\n\n{e}"
                )        

# =====================================================
# AI DASHBOARD
# =====================================================

st.divider()

st.header("🤖 AI Sustainability Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🌍 Carbon", f"{carbon:.2f} kg")

with c2:
    st.metric("💧 Water", f"{water:.0f} L/day")

with c3:
    st.metric("⚡ Energy", f"{energy:.0f} kWh")

with c4:
    st.metric("🌱 Eco Score", f"{eco_score:.0f}/100")

st.progress(eco_score / 100)

st.success(f"Current Eco Level: {level}")

# ---------------- AI Analysis ---------------- #

analysis = []

if carbon > 200:
    analysis.append(
        "🔴 Your carbon footprint is above the recommended level."
    )
else:
    analysis.append(
        "🟢 Your carbon footprint is within a healthy range."
    )

if water > 600:
    analysis.append(
        "💧 Water consumption is relatively high."
    )
else:
    analysis.append(
        "💧 Water consumption is efficient."
    )

if energy > 250:
    analysis.append(
        "⚡ Electricity usage can be reduced further."
    )
else:
    analysis.append(
        "⚡ Energy usage is efficient."
    )

st.subheader("📋 AI Analysis")

for item in analysis:
    st.info(item)

# ---------------- Personalized Recommendations ---------------- #

st.subheader("🌱 AI Recommendations")

recommendations = []

if carbon > 200:
    recommendations.extend([
        "🚶 Walk or cycle for short distances.",
        "🚌 Use public transport at least twice a week.",
        "💡 Replace old bulbs with LED lights."
    ])

if water > 600:
    recommendations.extend([
        "🚿 Reduce shower time.",
        "🚰 Fix leaking taps immediately.",
        "🌧 Install rainwater harvesting."
    ])

if energy > 250:
    recommendations.extend([
        "🔌 Turn off appliances when not in use.",
        "🌞 Use natural daylight whenever possible.",
        "⭐ Buy 5-star rated appliances."
    ])

if not recommendations:
    recommendations.extend([
        "🌍 Excellent! Continue your sustainable lifestyle.",
        "🌳 Plant a tree every year.",
        "♻ Continue segregating waste properly."
    ])

for rec in recommendations:
    st.success(rec)

# ---------------- Overall Rating ---------------- #

st.subheader("🏆 Sustainability Rating")

if eco_score >= 90:
    st.success("🌍 Planet Hero")

elif eco_score >= 75:
    st.success("🌳 Green Champion")

elif eco_score >= 60:
    st.warning("🌿 Eco Friendly")

else:
    st.error("🌱 Beginner")                