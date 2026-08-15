import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Energy Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 EcoBuddy Energy Analytics")
st.write("Analyze your energy consumption, bills and efficiency trends.")

# Load history
conn = sqlite3.connect("database/ecobuddy.db")

df = pd.read_sql_query("""
    SELECT
        date,
        city,
        consumption_kwh,
        bill,
        eco_score,
        biggest_consumer
    FROM prediction_history
    ORDER BY id
""", conn)

conn.close()

if df.empty:
    st.warning("No prediction data available yet.")
    st.info("Go to ⚡ Energy Predictor and create a prediction first.")
    st.stop()

# -----------------------------
# SUMMARY
# -----------------------------
st.subheader("📌 Overall Energy Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Predictions",
        len(df)
    )

with c2:
    st.metric(
        "Average Consumption",
        f"{df['consumption_kwh'].mean():.0f} kWh"
    )

with c3:
    st.metric(
        "Average Bill",
        f"₹{df['bill'].mean():,.0f}"
    )

with c4:
    st.metric(
        "Average Eco Score",
        f"{df['eco_score'].mean():.0f}/100"
    )

# -----------------------------
# LATEST PROFILE
# -----------------------------
latest = df.iloc[-1]

st.divider()
st.subheader("🔎 Latest Energy Profile")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Latest Consumption",
        f"{latest['consumption_kwh']:.0f} kWh"
    )

with c2:
    st.metric(
        "Latest Bill",
        f"₹{latest['bill']:,.0f}"
    )

with c3:
    st.metric(
        "Biggest Consumer",
        latest["biggest_consumer"]
    )

# -----------------------------
# CONSUMPTION TREND
# -----------------------------
st.divider()
st.subheader("⚡ Consumption Trend")

chart_df = df.copy()
chart_df["date"] = pd.to_datetime(chart_df["date"])

st.line_chart(
    chart_df.set_index("date")["consumption_kwh"]
)

# -----------------------------
# BILL TREND
# -----------------------------
st.subheader("💰 Electricity Bill Trend")

st.line_chart(
    chart_df.set_index("date")["bill"]
)

# -----------------------------
# ECO SCORE TREND
# -----------------------------
st.subheader("🌱 Eco Score Trend")

st.line_chart(
    chart_df.set_index("date")["eco_score"]
)

# -----------------------------
# BIGGEST CONSUMERS
# -----------------------------
st.divider()
st.subheader("🎯 Biggest Energy Consumers")

consumer_count = (
    df["biggest_consumer"]
    .value_counts()
)

st.bar_chart(consumer_count)

# -----------------------------
# INSIGHT
# -----------------------------
st.subheader("🧠 Analytics Insight")

most_common = consumer_count.index[0]

if len(df) >= 2:

    first = df.iloc[0]["consumption_kwh"]
    last = df.iloc[-1]["consumption_kwh"]

    change = last - first

    if change > 0:
        st.warning(
            f"Your latest predicted consumption is "
            f"**{change:.0f} kWh higher** than your first recorded prediction."
        )

    elif change < 0:
        st.success(
            f"Your latest predicted consumption is "
            f"**{abs(change):.0f} kWh lower** than your first recorded prediction."
        )

    else:
        st.info(
            "Your recorded consumption has remained approximately stable."
        )

else:
    st.info(
        "Create more predictions to generate meaningful consumption trends."
    )

st.info(
    f"Across your recorded predictions, **{most_common}** "
    f"has most frequently been identified as the biggest energy consumer."
)
