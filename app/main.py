import streamlit as st
from ui import sidebar_inputs  # Assuming ui.py is in the same 'app' folder

# --- Logo Path ---
# Assuming your logo is in SKYDOC-AI/skydoc_logo.png
# and you run from SKYDOC-AI/ with `streamlit run app/main.py`
logo_path = "skydoc_logo.png"

# --- Page Configuration ---
st.set_page_config(page_title="SkyDoc AI", layout="wide")

# --- Custom CSS for DARK BLUE Sidebar Text Color ---
# Replace #191970 with your specific dark blue if different.
st.markdown("""
<style>
    /* Target common text elements within the sidebar */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stHeading"] /* For st.sidebar.title and other headings */
    {
        color: #191970 !important; /* Dark Blue text - same as main background example */
    }
</style>
""", unsafe_allow_html=True)
# --- End Custom CSS ---

# --- Sidebar ---
st.sidebar.image(logo_path, width=100)
st.sidebar.title("SkyDoc AI") # Should be dark blue
st.sidebar.markdown("🚀 Smart Emergency Telemedicine Assistant") # Should be dark blue
st.sidebar.markdown("---")

# Patient Inputs (from ui.py)
# Labels for these inputs should also be dark blue due to the CSS.
location, symptoms, run_button = sidebar_inputs()

# --- Main Page Header ---
st.title("🛰️ SkyDoc AI – Satellite-Guided Medical Assistant") # Main page text color from config.toml
st.caption("A CASSINI Hackathon Prototype")

st.markdown("---")

# --- Main Content Columns ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Patient Case Summary")
    st.write(f"**Location:** {location}")
    st.write(f"**Symptoms:** {symptoms}")

with col2:
    st.subheader("🌿 NDVI Analysis")
    if run_button:
        st.write("Mean NDVI: Fetching...") # Placeholder
        st.write("Vegetation Stress: Fetching...") # Placeholder
        # Add actual NDVI logic here
    else:
        st.write("Mean NDVI: —")
        st.write("Vegetation Stress: —")

# --- AI Medical Advice Section ---
st.markdown("---")
st.subheader("🧠 AI Medical Advice")

if run_button:
    with st.spinner("SkyDoc AI is thinking..."):
        # Placeholder for actual LLM call
        st.info("LLM response will appear here once backend is connected.")
else:
    st.write("Click 'Analyze' in the sidebar to get advice.")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 SkyDoc AI — CASSINI Hackathon Project")