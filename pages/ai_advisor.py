import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Energy Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 EcoBuddy AI Energy Advisor")
st.write(
    "EcoBuddy analyzes your latest energy prediction "
    "and provides personalized insights and actions."
)

# -----------------------------
# LOAD LATEST PREDICTION
# -----------------------------
conn = sqlite3.connect("database/ecobuddy.db")

df = pd.read_sql_query(
    """
    SELECT *
    FROM prediction_history
    ORDER BY id DESC
    LIMIT 1
    """,
    conn
)

conn.close()

# -----------------------------
# NO PREDICTION
# -----------------------------
if df.empty:

    st.warning(
        "⚠️ No energy prediction found."
    )

    st.info(
        "First go to ⚡ Energy Predictor, "
        "enter your details and generate a prediction."
    )

    st.stop()

# -----------------------------
# GET LATEST DATA
# -----------------------------
latest = df.iloc[0]

consumption = float(
    latest["consumption_kwh"]
)

bill = float(
    latest["bill"]
)

score = int(
    latest["eco_score"]
)

city = latest["city"]
month = int(latest["month"])
family = int(latest["family_members"])
biggest = latest["biggest_consumer"]

date = latest["date"]

# -----------------------------
# ENERGY LEVEL
# -----------------------------
if consumption < 250:
    level = "🟢 Low"
elif consumption < 450:
    level = "🟡 Moderate"
else:
    level = "🔴 High"

# -----------------------------
# PROFILE
# -----------------------------
st.subheader("🔎 Your Latest Energy Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "⚡ Consumption",
        f"{consumption:.0f} kWh"
    )

with c2:
    st.metric(
        "💰 Estimated Bill",
        f"₹{bill:,.0f}"
    )

with c3:
    st.metric(
        "🌱 Eco Score",
        f"{score}/100"
    )

with c4:
    st.metric(
        "Energy Level",
        level
    )

st.caption(
    f"Latest prediction: {date} • "
    f"{city} • Family members: {family}"
)

# -----------------------------
# AI INSIGHT
# -----------------------------
st.subheader("🧠 EcoBuddy's Analysis")

if biggest == "Air Conditioner":

    insight = (
        "Your Air Conditioner is the biggest estimated "
        "energy consumer. Cooling appliances can have a "
        "significant impact on household electricity usage."
    )

elif biggest == "Refrigerator":

    insight = (
        "Your Refrigerator is the biggest estimated "
        "energy consumer. Efficient operation and proper "
        "maintenance can help control its energy usage."
    )

elif biggest == "Fan":

    insight = (
        "Fans are currently your biggest estimated "
        "energy consumer. Avoid unnecessary operation "
        "when rooms are unoccupied."
    )

elif biggest == "Television":

    insight = (
        "Your Television is the biggest estimated "
        "energy consumer. Avoid leaving it running "
        "when nobody is watching."
    )

elif biggest == "Monitor":

    insight = (
        "Your Monitor is the biggest estimated "
        "energy consumer. Turn it off during long "
        "periods of inactivity."
    )

elif biggest == "Washing Machine":

    insight = (
        "Your Washing Machine is the biggest estimated "
        "energy consumer. Full-load cycles can improve "
        "energy efficiency."
    )

else:

    insight = (
        "Lighting is your biggest estimated energy "
        "consumer. Switching off unused lights and "
        "using efficient LED lighting can help."
    )

st.info(insight)

# -----------------------------
# PRIORITY ACTION
# -----------------------------
st.subheader("🎯 Priority Action")

if consumption >= 450:

    st.error(
        "Your predicted consumption is relatively high. "
        f"Start by improving the efficiency of your "
        f"highest-consuming appliance: **{biggest}**."
    )

elif consumption >= 250:

    st.warning(
        f"Your consumption is moderate. Your first "
        f"priority should be optimizing **{biggest}** usage."
    )

else:

    st.success(
        "Your predicted consumption is relatively low. "
        "Continue following efficient energy habits."
    )

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
st.subheader("💡 Personalized Recommendations")

recommendations = []

if biggest == "Air Conditioner":
    recommendations.extend([
        "❄️ Use the AC only when required.",
        "🌡️ Keep the temperature at a comfortable moderate setting.",
        "🚪 Avoid cooling rooms that are unoccupied.",
        "🧹 Keep AC filters clean for efficient operation."
    ])

elif biggest == "Refrigerator":
    recommendations.extend([
        "🧊 Avoid keeping the refrigerator door open unnecessarily.",
        "❄️ Maintain appropriate cooling settings.",
        "🧹 Keep the refrigerator coils and vents clean.",
        "📦 Avoid overloading the refrigerator."
    ])

elif biggest == "Fan":
    recommendations.extend([
        "🌀 Switch off fans when leaving a room.",
        "🌀 Use fans when AC is not necessary.",
        "⚡ Prefer energy-efficient fans when replacing old ones."
    ])

elif biggest == "Television":
    recommendations.extend([
        "📺 Switch off the TV when nobody is watching.",
        "⏱️ Use sleep mode for automatic shutdown.",
        "🔌 Avoid unnecessary standby operation."
    ])

elif biggest == "Monitor":
    recommendations.extend([
        "🖥️ Turn off the monitor during long breaks.",
        "💻 Enable automatic sleep mode.",
        "🔌 Switch off the system when it is not needed."
    ])

elif biggest == "Washing Machine":
    recommendations.extend([
        "🧺 Prefer full-load washing cycles.",
        "⚡ Use suitable eco modes when available.",
        "🚿 Avoid unnecessary repeated washing cycles."
    ])

else:
    recommendations.extend([
        "💡 Switch off lights in unoccupied rooms.",
        "💡 Prefer LED bulbs.",
        "☀️ Use natural daylight whenever practical."
    ])

for recommendation in recommendations:
    st.write(recommendation)

# -----------------------------
# PROFILE SUMMARY
# -----------------------------
st.subheader("📋 Profile Summary")

summary = pd.DataFrame({
    "Parameter": [
        "City",
        "Family Members",
        "Monthly Consumption",
        "Estimated Bill",
        "Eco Score",
        "Energy Level",
        "Biggest Consumer"
    ],
    "Value": [
        city,
        family,
        f"{consumption:.0f} kWh",
        f"₹{bill:,.0f}",
        f"{score}/100",
        level,
        biggest
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# HOW IT WORKS
# -----------------------------
with st.expander("🤖 How EcoBuddy AI Advisor works"):

    st.write(
        "The Energy Predictor first uses the trained "
        "Gradient Boosting regression model to predict "
        "monthly electricity consumption."
    )

    st.write(
        "The prediction is stored in SQLite. "
        "The AI Energy Advisor then reads the latest "
        "prediction and interprets the user's energy profile."
    )

    st.write(
        "The advisor identifies the biggest estimated "
        "energy consumer and generates relevant "
        "recommendations."
    )

# -----------------------------
# GO BACK
# -----------------------------
st.divider()

st.info(
    "💡 Want to analyze a different household profile? "
    "Go to ⚡ Energy Predictor and create a new prediction."
)