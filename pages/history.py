import streamlit as st
import sqlite3
import pandas as pd

st.title("📋 Carbon Footprint History")

conn = sqlite3.connect("database/ecobuddy.db")

df = pd.read_sql_query("SELECT * FROM carbon_data", conn)

conn.close()

st.dataframe(df, use_container_width=True)