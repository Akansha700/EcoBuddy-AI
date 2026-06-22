import streamlit as st

st.set_page_config(page_title="Waste Segregation", page_icon="♻️")

st.title("♻️ AI Waste Segregation Assistant")

st.write("Select a waste item to know how it should be disposed.")

waste_item = st.selectbox(
    "Choose Waste Item",
    [
        "Plastic Bottle",
        "Newspaper",
        "Banana Peel",
        "Glass Bottle",
        "Aluminium Can",
        "Battery",
        "Food Waste",
        "E-Waste",
        "Clothes",
        "Cardboard"
    ]
)

if st.button("Identify Waste"):

    waste_data = {

        "Plastic Bottle": {
            "Category": "Recyclable",
            "Bin": "Blue Bin",
            "Impact": "Can take hundreds of years to decompose."
        },

        "Newspaper": {
            "Category": "Recyclable",
            "Bin": "Blue Bin",
            "Impact": "Paper can be recycled multiple times."
        },

        "Banana Peel": {
            "Category": "Biodegradable",
            "Bin": "Green Bin",
            "Impact": "Turns into compost naturally."
        },

        "Glass Bottle": {
            "Category": "Recyclable",
            "Bin": "Blue Bin",
            "Impact": "Glass is 100% recyclable."
        },

        "Aluminium Can": {
            "Category": "Recyclable",
            "Bin": "Blue Bin",
            "Impact": "Recycling saves energy."
        },

        "Battery": {
            "Category": "Hazardous",
            "Bin": "Red Bin",
            "Impact": "Contains toxic chemicals."
        },

        "Food Waste": {
            "Category": "Biodegradable",
            "Bin": "Green Bin",
            "Impact": "Can be converted into compost."
        },

        "E-Waste": {
            "Category": "Hazardous",
            "Bin": "Red Bin",
            "Impact": "Contains harmful metals."
        },

        "Clothes": {
            "Category": "Reusable",
            "Bin": "Donation/Recycling",
            "Impact": "Donate or recycle textiles."
        },

        "Cardboard": {
            "Category": "Recyclable",
            "Bin": "Blue Bin",
            "Impact": "Easy to recycle into new paper products."
        }
    }

    info = waste_data[waste_item]

    st.success(f"Category: {info['Category']}")
    st.info(f"Recommended Bin: {info['Bin']}")
    st.warning(f"Environmental Impact: {info['Impact']}")

    st.subheader("💡 EcoBuddy AI Recommendation")

    if info["Category"] == "Recyclable":
        st.write("♻️ Clean the item before recycling.")

    elif info["Category"] == "Biodegradable":
        st.write("🌱 Compost this waste if possible.")

    elif info["Category"] == "Hazardous":
        st.write("⚠️ Dispose of it at an authorized collection center.")

    else:
        st.write("👕 Reuse or donate this item whenever possible.")