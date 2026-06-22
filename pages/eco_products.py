import streamlit as st

st.set_page_config(page_title="Eco Product Advisor", page_icon="🛍️")

st.title("🛍️ Eco-Friendly Product Recommendation")

st.write("Find sustainable alternatives to everyday products.")

products = {

    "Plastic Bottle":{
        "Alternative":"Steel Bottle",
        "Eco Score":95,
        "Impact":"Reduces plastic waste and is reusable.",
        "Carbon":"Low",
        "Recycle":"Yes"
    },

    "Plastic Bag":{
        "Alternative":"Cloth Bag",
        "Eco Score":98,
        "Impact":"Reusable and biodegradable.",
        "Carbon":"Very Low",
        "Recycle":"Yes"
    },

    "Incandescent Bulb":{
        "Alternative":"LED Bulb",
        "Eco Score":96,
        "Impact":"Consumes 80% less electricity.",
        "Carbon":"Low",
        "Recycle":"Yes"
    },

    "Disposable Cup":{
        "Alternative":"Reusable Mug",
        "Eco Score":94,
        "Impact":"Reduces single-use waste.",
        "Carbon":"Low",
        "Recycle":"Yes"
    },

    "Plastic Toothbrush":{
        "Alternative":"Bamboo Toothbrush",
        "Eco Score":93,
        "Impact":"Biodegradable handle.",
        "Carbon":"Low",
        "Recycle":"Partially"
    },

    "Paper Napkin":{
        "Alternative":"Cloth Napkin",
        "Eco Score":91,
        "Impact":"Reusable for years.",
        "Carbon":"Very Low",
        "Recycle":"Yes"
    }

}

item = st.selectbox(
    "Select a Product",
    list(products.keys())
)

if st.button("Recommend Eco Product"):

    p = products[item]

    st.success(f"🌱 Recommended Alternative: {p['Alternative']}")

    st.metric("Eco Score", f"{p['Eco Score']}/100")

    st.write(f"🌍 Carbon Impact : {p['Carbon']}")

    st.write(f"♻️ Recyclable : {p['Recycle']}")

    st.info(p["Impact"])

    st.subheader("🤖 EcoBuddy AI Recommendation")

    st.write(
        f"Instead of using **{item}**, switch to **{p['Alternative']}**. "
        "This reduces waste, lowers carbon emissions, and supports sustainable living."
    )