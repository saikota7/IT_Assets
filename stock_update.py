import streamlit as st
from data_handler import load_data, update_status

st.set_page_config(layout="wide")

st.title("📦 Stock Update")

df = load_data()

asset_tag = st.selectbox(
    "Select Asset Tag",
    df["Laptop Asset Tag"].dropna().unique()
)

column = st.selectbox(
    "Select Asset Type",
    ["Laptop Status", "Keyboard Status", "Headset Status", "Monitor Status"]
)

new_status = st.selectbox(
    "New Status",
    ["Assigned", "In Stock", "Scrap", "Not Working"]
)

if st.button("Update"):
    update_status(asset_tag, column, new_status)
    st.success("✅ Updated Successfully")