import streamlit as st

st.set_page_config(
    page_title="EcoBuddy AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Custom CSS
# -----------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:55px;
    color:#2E8B57;
    font-weight:bold;
}

.sub-title{
    text-align:center;
    font-size:24px;
    color:#555;
}

.feature-card{
    background:#F0FFF4;
    padding:18px;
    border-radius:15px;
    margin-bottom:15px;
    border-left:6px solid #2E8B57;
}

</style>
""", unsafe_allow_html=True)

# -----------------------

st.markdown(
    "<h1 class='main-title'>🌍 EcoBuddy AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Your Intelligent Sustainability Assistant</p>",
    unsafe_allow_html=True
)

st.divider()

st.markdown("""
<div class='feature-card'>

### 🌱 What EcoBuddy AI Can Do

✅ Carbon Footprint Calculator

✅ Waste Segregation Assistant

✅ Water Conservation Advisor

✅ Energy Consumption Predictor

✅ Eco-Friendly Product Recommendation

✅ AI Sustainability Chatbot

</div>
""", unsafe_allow_html=True)

st.success("👈 Select any module from the left sidebar.")

