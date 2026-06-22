import streamlit as st
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Energy Predictor", page_icon="⚡")

st.title("⚡ Energy Consumption Predictor")

st.write("Estimate your monthly electricity usage and receive AI-based recommendations.")

members = st.number_input(
    "👨‍👩‍👧 Number of Family Members",
    min_value=1,
    value=4
)

units = st.number_input(
    "⚡ Monthly Electricity Consumption (kWh)",
    min_value=1,
    value=250
)

appliance = st.selectbox(
    "Most Used Appliance",
    [
        "Air Conditioner",
        "Refrigerator",
        "Washing Machine",
        "Television",
        "Computer",
        "Fans & Lights"
    ]
)

if st.button("Analyze Energy Usage"):

    bill = units * 8
    conn = sqlite3.connect("database/ecobuddy.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO energy_data
    (members,units,appliance,bill)

    VALUES(?,?,?,?)
    """,
    (
    members,
    units,
    appliance,
    bill
    ))

    conn.commit()

    conn.close()
    st.header("⚡ Energy Report")

    st.metric("Monthly Units", f"{units} kWh")
    st.metric("Estimated Electricity Bill", f"₹ {bill}")

    if units < 150:
        st.success("🟢 Low Energy Consumption")

    elif units < 350:
        st.warning("🟡 Moderate Energy Consumption")

    else:
        st.error("🔴 High Energy Consumption")

    eco_score = max(0, 100 - units / 5)

    st.metric("🌱 Eco Score", f"{eco_score:.0f}/100")

    fig = px.bar(
        x=["Electricity Units"],
        y=[units],
        title="Monthly Electricity Consumption"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💡 EcoBuddy AI Recommendations")

    if appliance == "Air Conditioner":
        st.warning("Use AC at 24–26°C and clean filters regularly.")

    elif appliance == "Refrigerator":
        st.info("Avoid opening the refrigerator door frequently.")

    elif appliance == "Washing Machine":
        st.info("Run only full loads to save electricity.")

    elif appliance == "Television":
        st.info("Turn off the TV completely instead of leaving it on standby.")

    elif appliance == "Computer":
        st.info("Enable power-saving mode and shut down when not in use.")

    else:
        st.info("Replace old bulbs with LED bulbs.")

    if units > 350:
        st.error("Your electricity usage is high. Consider switching to energy-efficient appliances.")

    elif units > 150:
        st.warning("You can reduce electricity usage by unplugging unused devices.")

    else:
        st.success("Excellent! Your electricity consumption is efficient.")