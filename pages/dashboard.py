import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from utils.pdf_report import generate_report

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="EcoBuddy AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.metric-card{
background:#E8F5E9;
padding:20px;
border-radius:15px;
border-left:8px solid #2E7D32;
box-shadow:0px 3px 10px rgba(0,0,0,0.15);
text-align:center;
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 EcoBuddy AI Dashboard")

# ---------------- DATABASE ---------------- #

try:

    conn = sqlite3.connect("database/ecobuddy.db")

    carbon_df = pd.read_sql_query(
        "SELECT * FROM carbon_data",
        conn
    )

    water_df = pd.read_sql_query(
        "SELECT * FROM water_data",
        conn
    )

    energy_df = pd.read_sql_query(
        "SELECT * FROM energy_data",
        conn
    )

    conn.close()

except Exception as e:

    st.error(f"Database Error : {e}")
    st.stop()

# ---------------- CALCULATIONS ---------------- #

total_records = len(carbon_df)

average_emission = (
    carbon_df["emission"].mean()
    if not carbon_df.empty
    else 0
)

highest = (
    carbon_df["emission"].max()
    if not carbon_df.empty
    else 0
)

lowest = (
    carbon_df["emission"].min()
    if not carbon_df.empty
    else 0
)

avg_water = (
    water_df["monthly"].mean()
    if not water_df.empty
    else 0
)

avg_energy = (
    energy_df["units"].mean()
    if not energy_df.empty
    else 0
)

eco_score = max(0, min(100, 100 - average_emission))

# ---------------- TOP METRICS ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📄 Total Reports", total_records)

with c2:
    st.metric("🌍 Avg Carbon", f"{average_emission:.2f} kg")

with c3:
    st.metric("💧 Avg Water", f"{avg_water:.0f} L")

with c4:
    st.metric("⚡ Avg Energy", f"{avg_energy:.0f} kWh")

st.divider()

# ---------------- DASHBOARD CARDS ---------------- #

card1, card2, card3, card4 = st.columns(4)

with card1:

    st.markdown(f"""
    <div class="metric-card">

    <h3>🌍 Carbon</h3>

    <h2>{average_emission:.2f} kg</h2>

    </div>
    """, unsafe_allow_html=True)

with card2:

    st.markdown(f"""
    <div class="metric-card">

    <h3>💧 Water</h3>

    <h2>{avg_water:.0f} L</h2>

    </div>
    """, unsafe_allow_html=True)

with card3:

    st.markdown(f"""
    <div class="metric-card">

    <h3>⚡ Energy</h3>

    <h2>{avg_energy:.0f} kWh</h2>

    </div>
    """, unsafe_allow_html=True)

with card4:

    st.markdown(f"""
    <div class="metric-card">

    <h3>🌱 Eco Score</h3>

    <h2>{eco_score:.0f}/100</h2>

    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- EXTRA METRICS ---------------- #

left, right = st.columns(2)

with left:

    st.metric(
        "Highest Carbon Emission",
        f"{highest:.2f} kg"
    )

with right:

    st.metric(
        "Lowest Carbon Emission",
        f"{lowest:.2f} kg"
    )

st.divider()

# ---------------- PIE CHART ---------------- #

if not carbon_df.empty:

    st.subheader("🚗 Transport Usage")

    fig = px.pie(
        carbon_df,
        names="transport",
        title="Most Used Transport"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- LINE CHART ---------------- #

if not carbon_df.empty:

    st.subheader("📈 Carbon Footprint Trend")

    fig2 = px.line(
        carbon_df,
        x="id",
        y="emission",
        markers=True,
        title="Carbon Emission History"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------- WATER GRAPH ---------------- #

if not water_df.empty:

    st.subheader("💧 Water Consumption")

    water_chart = px.bar(
        water_df,
        x="id",
        y="monthly",
        title="Monthly Water Usage"
    )

    st.plotly_chart(
        water_chart,
        use_container_width=True
    )

# ---------------- ENERGY GRAPH ---------------- #

if not energy_df.empty:

    st.subheader("⚡ Energy Consumption")

    energy_chart = px.bar(
        energy_df,
        x="id",
        y="units",
        title="Energy Usage"
    )

    st.plotly_chart(
        energy_chart,
        use_container_width=True
    )

st.success("✅ Dashboard updated from SQLite Database")

# ---------------- PDF REPORT ---------------- #

st.divider()

st.subheader("📄 Download Sustainability Report")

if st.button("Generate PDF Report"):

    filename = generate_report(
        carbon=round(average_emission, 2),
        water=round(avg_water, 2),
        energy=round(avg_energy, 2),
        score=round(eco_score)
    )

    if os.path.exists(filename):

        st.success("✅ PDF Generated Successfully!")

        with open(filename, "rb") as pdf:

            st.download_button(
                label="⬇ Download Report",
                data=pdf,
                file_name="EcoBuddy_Report.pdf",
                mime="application/pdf"
            )

    else:

        st.error("Unable to generate PDF.")

# ---------------- SUSTAINABILITY TIPS ---------------- #

st.divider()

st.subheader("🌿 Today's Sustainability Tips")

tips = [
    "🚶 Walk or cycle for short distances.",
    "💧 Turn off taps while brushing.",
    "⚡ Switch off unused electrical appliances.",
    "♻ Segregate wet and dry waste.",
    "🌳 Plant at least one tree every year."
]

for tip in tips:
    st.success(tip)