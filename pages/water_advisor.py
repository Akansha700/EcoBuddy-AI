import streamlit as st
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Water Advisor", page_icon="💧")

st.title("💧 Water Conservation Advisor")

st.write("Estimate your water usage and receive personalized conservation tips.")

family = st.number_input(
    "👨‍👩‍👧‍👦 Number of Family Members",
    min_value=1,
    value=4
)

daily = st.number_input(
    "🚰 Daily Water Usage (Litres)",
    min_value=1,
    value=500
)

source = st.selectbox(
    "Water Source",
    [
        "Municipal Supply",
        "Borewell",
        "Rainwater Harvesting",
        "Mixed"
    ]
)

if st.button("Analyze Water Usage"):

    monthly = daily * 30

    bill = monthly * 0.05

    conn = sqlite3.connect("database/ecobuddy.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO water_data
    (family,daily,source,monthly,bill)

    VALUES(?,?,?,?,?)
    """,
    (
    family,
    daily,
    source,
    monthly,
    bill
    ))

    conn.commit()

    conn.close()

    st.header("💧 Results")

    st.metric("Monthly Consumption", f"{monthly:,} Litres")

    st.metric("Estimated Bill", f"₹ {bill:.2f}")

    if daily < 300:
        st.success("🟢 Low Water Usage")

    elif daily < 700:
        st.warning("🟡 Moderate Water Usage")

    else:
        st.error("🔴 High Water Usage")

    score = max(0, 100 - (daily / 10))

    st.metric("🌱 Water Sustainability Score", f"{score:.0f}/100")

    fig = px.bar(
        x=["Daily", "Monthly"],
        y=[daily, monthly],
        labels={"x": "Usage", "y": "Litres"},
        title="Water Consumption"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💡 EcoBuddy AI Recommendations")

    if daily > 700:
        st.warning("• Fix leaking taps immediately.")
        st.warning("• Use low-flow shower heads.")
        st.warning("• Reuse RO wastewater.")
        st.warning("• Harvest rainwater.")

    elif daily > 300:
        st.info("• Turn off taps while brushing.")
        st.info("• Wash vehicles using a bucket.")
        st.info("• Run washing machines with full loads.")

    else:
        st.success("Excellent! Your water usage is sustainable.")

    if source == "Rainwater Harvesting":
        st.success("Great! Rainwater harvesting helps conserve groundwater.")

    elif source == "Borewell":
        st.warning("Avoid excessive groundwater extraction.")

    elif source == "Municipal Supply":
        st.info("Use municipal water responsibly.")