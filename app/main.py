# app/main.py
import streamlit as st
from ui import sidebar_inputs        # our sidebar module

# ----- page setup -----
st.set_page_config(page_title="SkyDoc AI", layout="wide")
st.title("🛰️ SkyDoc AI – Satellite-Guided Telemedicine")

# ----- sidebar -----
location, symptoms, run_button = sidebar_inputs()

# ----- main area -----
if run_button:
    # everything inside this block is indented 4 spaces
    st.subheader("📊 NDVI Analysis")
    st.write("Mean NDVI: loading…")
    st.write("Vegetation stress: loading…")

    st.subheader("🧠 AI Medical Advice")
    st.info("LLM advice will appear here…")
