import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Energy History",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Energy Prediction History")
st.write("View your previous EcoBuddy energy predictions.")

conn = sqlite3.connect("database/ecobuddy.db")

df = pd.read_sql_query("""
    SELECT
        date AS Date,
        family_members AS "Family Members",
        city AS City,
        consumption_kwh AS "Consumption (kWh)",
        bill AS "Bill (₹)",
        eco_score AS "Eco Score",
        biggest_consumer AS "Biggest Consumer"
    FROM prediction_history
    ORDER BY id DESC
""", conn)

conn.close()

if df.empty:

    st.info(
        "No prediction history yet. "
        "Go to Energy Predictor and make your first prediction."
    )

else:

    # Summary
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Predictions",
            len(df)
        )

    with c2:
        st.metric(
            "Average Consumption",
            f"{df['Consumption (kWh)'].mean():.0f} kWh"
        )

    with c3:
        st.metric(
            "Average Bill",
            f"₹{df['Bill (₹)'].mean():,.0f}"
        )

    st.divider()

    # History table
    st.subheader("📋 Prediction History")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Consumption chart
    st.subheader("⚡ Consumption Trend")

    chart_data = df.sort_values("Date")

    st.line_chart(
        chart_data.set_index("Date")[
            "Consumption (kWh)"
        ]
    )

    # Bill chart
    st.subheader("💰 Electricity Bill Trend")

    st.line_chart(
        chart_data.set_index("Date")[
            "Bill (₹)"
        ]
    )

    # Biggest consumer
    st.subheader("🎯 Most Common Biggest Consumer")

    biggest = df["Biggest Consumer"].value_counts()

    st.bar_chart(biggest)