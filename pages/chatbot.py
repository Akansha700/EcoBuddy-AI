import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoBuddy AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# CHECK API KEY
# ============================================================

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY is missing.")
    st.info(
        "Create a .env file in the main EcoBuddy project folder "
        "and add: GROQ_API_KEY=your_api_key"
    )
    st.stop()

# ============================================================
# GROQ CLIENT
# ============================================================

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"❌ Could not initialize Groq: {e}")
    st.stop()

# ============================================================
# ECOBUDDY SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are EcoBuddy AI, an intelligent and friendly environmental
assistant.

Your main areas of expertise are:

1. Waste management
2. Waste segregation
3. Recycling
4. Composting
5. Plastic pollution
6. E-waste
7. Sustainable living
8. Climate change
9. Carbon footprint
10. Renewable energy
11. Water conservation
12. Energy conservation
13. Environmental awareness

You can also answer general questions from the user.

Rules:

- Give accurate and understandable answers.
- Explain technical concepts in simple language when appropriate.
- For environmental questions, provide practical real-world suggestions.
- If the user asks a general question, answer it normally.
- Do not pretend to have information that you do not have.
- Do not claim that an action was performed if it was not.
- Be concise but useful.
- Use bullet points when they improve readability.
- Maintain a friendly and educational personality.
"""

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# ============================================================
# HEADER
# ============================================================

st.title("🤖 EcoBuddy AI")
st.subheader("Your Intelligent Environmental Assistant")

st.write(
    "Ask me about waste management, recycling, sustainability, "
    "carbon footprint, climate change, or even general questions!"
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🌱 EcoBuddy")

    st.write(
        "EcoBuddy AI helps you learn about environmental issues "
        "and sustainable living."
    )

    st.divider()

    st.subheader("💡 Try asking")

    st.write("♻️ How should I segregate waste?")
    st.write("🌱 What is composting?")
    st.write("🌍 How can I reduce my carbon footprint?")
    st.write("🔋 How does solar energy work?")
    st.write("🗑️ What goes into a dry waste bin?")
    st.write("💻 How should I dispose of e-waste?")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()

# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask EcoBuddy anything..."
)

# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=st.session_state.messages,

                temperature=0.7,

                max_tokens=1024,

                top_p=0.9
            )

            assistant_response = response.choices[0].message.content

            response_placeholder.markdown(
                assistant_response
            )

            # Save response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response
                }
            )

        except Exception as e:

            error_message = f"""
❌ **Unable to generate a response.**

Error:

`{str(e)}`

Please check your Groq API key and internet connection.
"""

            response_placeholder.markdown(error_message)        
