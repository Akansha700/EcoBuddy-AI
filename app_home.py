import streamlit as st

st.title("🌱 EcoBuddy AI")

st.subheader("Your Intelligent Sustainability Assistant")

st.write(
    "EcoBuddy AI helps you understand and improve your "
    "environmental impact through energy, carbon, water, "
    "waste and sustainable lifestyle insights."
)

st.divider()

st.subheader("🌍 What EcoBuddy AI Can Do")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### ⚡ Energy")
    st.write(
        "Predict household energy consumption "
        "and understand usage patterns."
    )

with c2:
    st.markdown("### 🌍 Carbon")
    st.write(
        "Estimate your personal carbon footprint "
        "from everyday activities."
    )

with c3:
    st.markdown("### 🌱 Sustainability")
    st.write(
        "Get guidance for water, waste and "
        "eco-friendly choices."
    )

st.divider()

st.success(
    "💡 Choose a module from the sidebar to get started."
)

st.caption(
    "EcoBuddy AI — Smart Energy, Better Sustainability."
)