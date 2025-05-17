# app/ui.py
import streamlit as st

def sidebar_inputs():
    st.sidebar.header("🧍 Patient Information")

    location = st.sidebar.text_input(
        "📍 Location",
        value="Florence"
    )

    symptoms = st.sidebar.text_area(
        "📝 Describe Symptoms",
        height=150,
        placeholder="Example: fever, headache, rash..."
    )

    run_button = st.sidebar.button("🚀 Analyze")

    return location, symptoms, run_button
