import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="EcoBuddy Energy Predictor",
    page_icon="⚡",
    layout="wide"
)

# =========================
# LOAD DATA + MODEL
# =========================

df = pd.read_csv("data/electricity_energy_dataset.csv")

bundle = joblib.load(
    "models/energy_consumption_model.pkl"
)

model = bundle["model"]
features = bundle["features"]

# =========================
# HEADER
# =========================

st.title("⚡ EcoBuddy AI Energy Predictor")

st.write(
    "Predict your monthly electricity consumption "
    "and get personalized ways to reduce energy usage."
)

st.info(
    "Enter your normal appliance usage. "
    "Appliance values are measured in hours."
)

# =========================
# HOUSEHOLD DETAILS
# =========================

st.subheader("🏠 Household Details")

c1, c2, c3 = st.columns(3)

with c1:
    family = st.number_input(
        "👨‍👩‍👧 Family Members",
        min_value=1,
        max_value=15,
        value=4,
        step=1
    )

with c2:
    city = st.selectbox(
        "🏙️ City",
        sorted(df["City"].unique())
    )

with c3:

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    month_name = st.selectbox(
        "📅 Month",
        list(month_names.values())
    )

    month = list(month_names.keys())[
        list(month_names.values()).index(month_name)
    ]

# =========================
# APPLIANCE USAGE
# =========================

st.subheader("🔌 Appliance Usage")

st.caption(
    "Enter approximately how many hours each appliance is used."
)

c1, c2 = st.columns(2)

with c1:

    fan = st.number_input(
        "🌀 Fan (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=6.0,
        step=0.5
    )

    refrigerator = st.number_input(
        "🧊 Refrigerator (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=20.0,
        step=0.5
    )

    ac = st.number_input(
        "❄️ Air Conditioner (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.5
    )

    television = st.number_input(
        "📺 Television (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5
    )

with c2:

    monitor = st.number_input(
        "🖥️ Monitor (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5
    )

    washing = st.number_input(
        "🧺 Washing Machine (hours/week)",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.5
    )

    lighting = st.number_input(
        "💡 Lighting (hours/day)",
        min_value=0.0,
        max_value=24.0,
        value=6.0,
        step=0.5
    )

    tariff = st.number_input(
        "💰 Electricity Tariff (₹/kWh)",
        min_value=1.0,
        max_value=20.0,
        value=8.0,
        step=0.1
    )

# =========================
# PREDICTION
# =========================

st.divider()

if st.button(
    "⚡ Predict My Energy Usage",
    type="primary"
):

    # -------------------------
    # INPUT DATA
    # -------------------------

    input_data = pd.DataFrame([{
        "FamilyMembers": family,
        "FanHoursPerDay": fan,
        "RefrigeratorHoursPerDay": refrigerator,
        "AirConditionerHoursPerDay": ac,
        "TelevisionHoursPerDay": television,
        "MonitorHoursPerDay": monitor,
        "WashingMachineHoursPerWeek": washing,
        "LightingHoursPerDay": lighting,
        "City": city,
        "Month": month,
        "TariffRateINRPerKWh": tariff
    }])

    input_data = input_data[features]

    # -------------------------
    # ML PREDICTION
    # -------------------------

    consumption = float(
        model.predict(input_data)[0]
    )

    consumption = max(0, consumption)

    # Estimated bill
    bill = consumption * tariff

    # -------------------------
    # APPLIANCE IMPACT
    # -------------------------

    appliance_usage = {

        "Fan":
            fan * 30 * 0.075,

        "Refrigerator":
            refrigerator * 30 * 0.15,

        "Air Conditioner":
            ac * 30 * 1.5,

        "Television":
            television * 30 * 0.10,

        "Monitor":
            monitor * 30 * 0.08,

        "Washing Machine":
            washing * 4.33 * 0.50,

        "Lighting":
            lighting * 30 * 0.06
    }

    impact_df = pd.DataFrame(
        list(appliance_usage.items()),
        columns=[
            "Appliance",
            "Estimated_kWh"
        ]
    )

    impact_df = impact_df.sort_values(
        "Estimated_kWh",
        ascending=False
    )

    biggest = impact_df.iloc[0]["Appliance"]

    biggest_kwh = impact_df.iloc[0][
        "Estimated_kWh"
    ]

    # -------------------------
    # ECO SCORE
    # -------------------------

    score = 100

    if ac >= 6:
        score -= 15

    elif ac >= 4:
        score -= 8

    if fan >= 10:
        score -= 8

    if television >= 6:
        score -= 6

    if monitor >= 6:
        score -= 6

    if lighting >= 9:
        score -= 6

    if washing >= 6:
        score -= 5

    if consumption > 500:
        score -= 15

    elif consumption > 400:
        score -= 8

    score = max(
        0,
        min(100, score)
    )

    # -------------------------
    # CONSUMPTION LEVEL
    # -------------------------

    if consumption < 250:
        level = "🟢 Low"

    elif consumption < 450:
        level = "🟡 Moderate"

    else:
        level = "🔴 High"

    # =========================
    # SAVE TO DATABASE
    # =========================

    conn = sqlite3.connect(
        "database/ecobuddy.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO prediction_history
        (
            date,
            family_members,
            city,
            month,
            consumption_kwh,
            bill,
            eco_score,
            biggest_consumer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            family,
            city,
            month,
            consumption,
            bill,
            score,
            biggest
        )
    )

    conn.commit()
    conn.close()

    # =========================
    # RESULTS
    # =========================

    st.subheader(
        "📊 Your AI Energy Report"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "⚡ Monthly Consumption",
            f"{consumption:.0f} kWh"
        )

    with c2:
        st.metric(
            "💰 Estimated Monthly Bill",
            f"₹{bill:,.0f}"
        )

    with c3:
        st.metric(
            "🌱 Eco Score",
            f"{score}/100"
        )

    st.success(
        f"Your predicted consumption level is "
        f"**{level}**."
    )

    # =========================
    # BIGGEST CONSUMER
    # =========================

    st.subheader(
        "🎯 Biggest Energy Consumer"
    )

    st.warning(
        f"**{biggest}** is your biggest estimated "
        f"energy consumer at approximately "
        f"**{biggest_kwh:.1f} kWh/month**."
    )

    # =========================
    # CHART
    # =========================

    st.subheader(
        "📊 Estimated Appliance Impact"
    )

    chart_df = impact_df.set_index(
        "Appliance"
    )

    st.bar_chart(chart_df)

    st.caption(
        "Appliance impact is an estimate based on "
        "typical appliance power ratings and your "
        "entered usage."
    )

    # =========================
    # SAVING OPPORTUNITY
    # =========================

    st.subheader(
        "💰 Potential Saving Opportunity"
    )

    saving_hours = {
        "Air Conditioner": ac,
        "Fan": fan,
        "Television": television,
        "Monitor": monitor,
        "Lighting": lighting
    }

    power = {
        "Air Conditioner": 1.5,
        "Fan": 0.075,
        "Television": 0.10,
        "Monitor": 0.08,
        "Lighting": 0.06
    }

    if (
        biggest in saving_hours
        and saving_hours[biggest] > 1
    ):

        reduction = min(
            1.0,
            saving_hours[biggest] * 0.25
        )

        saving_kwh = (
            reduction *
            30 *
            power[biggest]
        )

        saving_money = (
            saving_kwh * tariff
        )

        st.info(
            f"If you reduce **{biggest}** usage "
            f"by approximately **{reduction:.1f} "
            f"hour/day**, you could save around "
            f"**{saving_kwh:.1f} kWh/month**, "
            f"worth approximately "
            f"**₹{saving_money:,.0f}/month**."
        )

    else:

        st.info(
            "Reducing the usage of your highest "
            "consuming appliances can help lower "
            "your monthly electricity bill."
        )

    # =========================
    # RECOMMENDATIONS
    # =========================

    st.subheader(
        "💡 Ways to Reduce Your Consumption"
    )

    recommendations = []

    if ac >= 6:

        recommendations.append(
            "❄️ **Air Conditioner:** Usage is high. "
            "Try reducing AC usage by 1–2 hours/day "
            "and avoid cooling empty rooms."
        )

    elif ac >= 4:

        recommendations.append(
            "❄️ **Air Conditioner:** Use AC only "
            "when required and maintain a moderate "
            "temperature."
        )

    if fan >= 10:

        recommendations.append(
            "🌀 **Fan:** Switch off fans when "
            "leaving a room and consider "
            "energy-efficient fans."
        )

    if television >= 6:

        recommendations.append(
            "📺 **Television:** Avoid leaving the TV "
            "running when nobody is watching."
        )

    if monitor >= 6:

        recommendations.append(
            "🖥️ **Monitor:** Turn off the monitor "
            "during long breaks."
        )

    if washing >= 5:

        recommendations.append(
            "🧺 **Washing Machine:** Prefer full-load "
            "cycles and avoid unnecessary small loads."
        )

    if lighting >= 8:

        recommendations.append(
            "💡 **Lighting:** Switch off unused lights "
            "and prefer LED bulbs."
        )

    if not recommendations:

        recommendations.append(
            "🌱 Your current usage looks reasonable. "
            "Continue switching off appliances when "
            "they are not required."
        )

    for recommendation in recommendations:
        st.write(recommendation)

    # =========================
    # ECO SCORE EXPLANATION
    # =========================

    with st.expander(
        f"🌱 Why is my Eco Score {score}/100?"
    ):

        st.write(
            "Your Eco Score is a project-level "
            "efficiency indicator based on appliance "
            "usage and predicted monthly consumption."
        )

        st.write(
            "Higher unnecessary appliance usage and "
            "higher predicted consumption reduce the score."
        )

    # =========================
    # MODEL EXPLANATION
    # =========================

    with st.expander(
        "🤖 How does EcoBuddy predict this?"
    ):

        st.write(
            "EcoBuddy uses a Gradient Boosting "
            "regression model trained using appliance "
            "usage, family size, city, month and "
            "electricity tariff."
        )

        st.write(
            "The model predicts monthly electricity "
            "consumption in kWh."
        )

        st.write(
            "The estimated bill is calculated by "
            "multiplying predicted consumption by "
            "the entered tariff."
        )

        st.write(
            "Model performance: R² = 0.9776, "
            "MAE = 13.67 kWh, RMSE = 18.15 kWh."
        )