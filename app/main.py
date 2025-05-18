import streamlit as st
from ui import sidebar_inputs  # Assuming ui.py is in the same 'app' folder
from logic import compute_scene_metrics          # ← new
from LLM   import mina_LLM 
from sentence_transformers import SentenceTransformer
from chromadb import Client
from LLM import METRIC_INFO, SYSTEM_PROMPT
import ollama, json
import re, json, streamlit as st

def safe_json(text: str):
    """
    Remove common LLM wrappers (markdown fences, prefaces),
    then json-decode.
    """
    # 1) take everything between the first "[" and the last "]"
    m = re.search(r"\[.*\]", text, flags=re.S)
    if not m:
        raise ValueError("No JSON array found")
    cleaned = m.group(0)

    # 2) try to decode
    return json.loads(cleaned)

@st.cache_resource(show_spinner=False)
def init_rag():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    vecdb    = Client().create_collection("session_store")
    return embedder, vecdb

print('Stop 1')
embedder, vecdb = init_rag()
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
print('Stop 2')
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

print('Stop 3')
if run_button:
    with st.spinner("SkyDoc AI is thinking..."):
        # Placeholder for actual LLM call
        st.info("LLM response will appear here once backend is connected.")
        metrics = compute_scene_metrics()

    # vecdb.clear()                                      # start fresh each click
    # vecdb.clear()   ← remove this

    # vecdb.delete(where={})          # ← add this

    context_chunks = [
        f"Average NDVI for tile {metrics['tile_id']} on {metrics['acq_date']} is {metrics['avg_ndvi']:.2f}.",
        f"{metrics['stress_pct']:.1f}% of pixels indicate vegetation stress.",
        f"GNSS location: {metrics['lat']:.4f}°, {metrics['lon']:.4f}°, height {metrics['height']:.1f} m."
    ]
    for i, chunk in enumerate(context_chunks):
        vecdb.add(f"chunk_{i}",
                  embeddings=[embedder.encode(chunk)],
                  documents=[chunk])

    # 3) formulate the user question
    user_prompt = (
        "Using ONLY the context above, propose **three** concrete "
        "SMART-Emergency-Healthcare solutions (tele-medicine, "
        "medical-logistics, or SAR-support) most relevant to this "
        "location and date."
    )

    st.subheader("🌿 NDVI analysis")
    st.metric("Mean NDVI",     f"{metrics['avg_ndvi']:.2f}")
    st.metric("Stress pixels", f"{metrics['stress_pct']:.1f}%")
    # 4) retrieve the most relevant chunks
    top_docs = vecdb.query(
        query_embeddings=[embedder.encode(user_prompt)],
        n_results=3
    )["documents"][0]
    ctx = "\n".join(top_docs)

    # 5) build the final prompt & call Gemma-3
    final_prompt = (
        f"Here is some information for you:\n{METRIC_INFO}\n\n"
        f"Context:\n{ctx}\n\n"
        f"User question:\n{user_prompt}"
    )
    with st.spinner("Gemma-3 is thinking …"):
        response = ollama.chat(
            model="gemma3:12b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": final_prompt}
            ]
        )
    reply_json = response["message"]["content"]
    print(reply_json)
    # 6) display results
    

    st.subheader("🧠 AI medical advice")
    # st.json(json.loads(reply_json))  
    # st.text(reply_json)      # ← temp debugging
    try:
        st.json(safe_json(reply_json))
    except Exception as e:
        # st.error(f"❌ Couldn’t parse model output: {e}")
        st.write(reply_json) 


else:
    st.write("Click 'Analyze' in the sidebar to get advice.")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 SkyDoc AI — CASSINI Hackathon Project")