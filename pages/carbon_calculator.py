import streamlit as st
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Carbon Calculator", page_icon="🌍")

st.title("🌍 Carbon Footprint Calculator")

st.write("Estimate your monthly carbon footprint and receive sustainability recommendations.")

st.divider()

# ---------------------------
# User Inputs
# ---------------------------

transport = st.selectbox(
    "🚗 Select your Mode of Transport",
    ["Car", "Bike", "Bus", "Train", "Bicycle", "Walking"]
)

distance = st.number_input(
    "📏 Distance Travelled per Day (km)",
    min_value=0.0,
    value=10.0
)

electricity = st.number_input(
    "⚡ Monthly Electricity Consumption (kWh)",
    min_value=0.0,
    value=150.0
)

diet = st.selectbox(
    "🥗 Select your Diet",
    ["Vegetarian", "Mixed", "Non-Vegetarian"]
)

st.divider()

# ---------------------------
# Calculate Button
# ---------------------------

if st.button("Calculate Carbon Footprint"):

    # -----------------------
    # Transport Emission
    # -----------------------

    if transport == "Car":
        transport_emission = distance * 0.21

    elif transport == "Bike":
        transport_emission = distance * 0.10

    elif transport == "Bus":
        transport_emission = distance * 0.08

    elif transport == "Train":
        transport_emission = distance * 0.04

    else:
        transport_emission = 0

    # -----------------------
    # Electricity Emission
    # -----------------------

    electricity_emission = electricity * 0.5

    # -----------------------
    # Diet Emission
    # -----------------------

    if diet == "Vegetarian":
        diet_emission = 100

    elif diet == "Mixed":
        diet_emission = 200

    else:
        diet_emission = 350

    # -----------------------
    # Total Emission
    # -----------------------

    total = transport_emission + electricity_emission + diet_emission
    # Save to SQLite Database

    conn = sqlite3.connect("database/ecobuddy.db")

    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO carbon_data
(transport, distance, electricity, diet, emission)
VALUES (?, ?, ?, ?, ?)
""",
(
    transport,
    distance,
    electricity,
    diet,
    total
))

    conn.commit()
    conn.close()
    # -----------------------
    # Results
    # -----------------------

    st.header("🌍 Carbon Footprint Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚗 Transport",
            f"{transport_emission:.2f} kg"
        )

    with col2:
        st.metric(
            "⚡ Electricity",
            f"{electricity_emission:.2f} kg"
        )

    with col3:
        st.metric(
            "🥗 Diet",
            f"{diet_emission:.2f} kg"
        )

    st.success(
        f"### Total Estimated Carbon Emission: {total:.2f} kg CO₂ / month"
    )
    st.success("✅ Your result has been saved successfully!")
    # -----------------------
    # Carbon Status
    # -----------------------

    st.subheader("Carbon Footprint Status")

    if total < 200:
        st.success("🟢 Low Carbon Footprint")

    elif total < 400:
        st.warning("🟡 Medium Carbon Footprint")

    else:
        st.error("🔴 High Carbon Footprint")

    # -----------------------
    # Sustainability Score
    # -----------------------

    score = max(0, 100 - (total / 10))

    st.metric(
        "🌱 Sustainability Score",
        f"{score:.0f}/100"
    )

    # -----------------------
    # Pie Chart
    # -----------------------

    chart = px.pie(
        names=["Transport", "Electricity", "Diet"],
        values=[
            transport_emission,
            electricity_emission,
            diet_emission
        ],
        title="Carbon Emission Distribution"
    )

    st.plotly_chart(chart, use_container_width=True)

    # -----------------------
    # AI Recommendations
    # -----------------------

    st.subheader("💡 Personalized Sustainability Tips")

    if transport == "Car":
        st.info("🚍 Try using public transport or carpooling 2–3 days a week.")

    elif transport == "Bike":
        st.info("🏍️ Maintain your bike regularly to improve fuel efficiency.")

    elif transport == "Bus":
        st.info("🚌 Great choice! Public transport reduces emissions.")

    elif transport == "Train":
        st.info("🚆 Trains are one of the most eco-friendly transport options.")

    elif transport == "Bicycle":
        st.info("🚴 Excellent! Cycling produces almost zero emissions.")

    elif transport == "Walking":
        st.info("🚶 Fantastic! Walking is the healthiest and greenest option.")

    if electricity > 250:
        st.warning("💡 Your electricity consumption is high. Consider using LED bulbs and energy-efficient appliances.")

    elif electricity > 150:
        st.info("⚡ Reduce unnecessary appliance usage to save energy.")

    else:
        st.success("🌱 Your electricity usage is efficient.")

    if diet == "Non-Vegetarian":
        st.warning("🥩 Reducing meat consumption even one day per week can lower your carbon footprint.")

    elif diet == "Mixed":
        st.info("🥗 Increasing plant-based meals can reduce emissions.")

    else:
        st.success("🌿 A vegetarian diet generally has a lower carbon footprint.")

    # -----------------------
    # Overall Suggestion
    # -----------------------

    st.subheader("🌍 Overall Assessment")

    if total < 200:
        st.success(
            "Excellent! Your lifestyle is environmentally friendly. Keep following sustainable practices."
        )

    elif total < 400:
        st.warning(
            "Your carbon footprint is moderate. Small lifestyle changes can significantly reduce emissions."
        )

    else:
        st.error(
            "Your carbon footprint is relatively high. Consider improving transportation habits, reducing electricity usage, and adopting a more sustainable diet."
        )

    st.divider()

    st.caption("EcoBuddy AI • AI for Sustainability Project")