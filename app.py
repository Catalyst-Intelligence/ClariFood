import streamlit as st
import cv2
import numpy as np
from google import genai
from PIL import Image

# Initialize Gemini Client
client = genai.Client()

# Force full viewport usage to widen the camera layout frame
st.set_page_config(page_title="NutriScan AI Pro", page_icon="🛡️", layout="wide")

st.title("🛡️ NutriScan AI: Conversational Diet Intelligence")
st.write("A production-hardened hybrid edge/cloud system with dynamic session memory.")

st.markdown("---")

# --- STEP 1: CONTEXT INJECTION DECK (SIDEBAR) ---
st.sidebar.header("👤 Dynamic Health Profile")

goal_options = ["Weight Loss", "Muscle Gain / Clean Bulk", "Diabetes Management", "Hypertension Control", "Gluten-Free Induction"]
selected_goals = st.sidebar.multiselect("Primary Objectives", options=goal_options)

# Custom Goal Input Gate
custom_goal_active = st.sidebar.checkbox("Inject custom targets?")
custom_goal_text = ""
if custom_goal_active:
    custom_goal_text = st.sidebar.text_input("Type custom health profile constraints:")

allergy_options = ["Dairy", "Nuts", "Gluten", "Soy", "Artificial Sweeteners", "Preservatives"]
selected_allergies = st.sidebar.multiselect("STRICT Avoidances / Allergies", options=allergy_options)

additional_notes = st.sidebar.text_area("Narrative Clinical Notes (e.g., medical conditions):")

# Construct the master string block
final_goals = selected_goals + ([custom_goal_text] if custom_goal_text else [])
user_profile_context = f"""
USER HEALTH PROFILE DOSSIER:
- Objectives: {', '.join(final_goals) if final_goals else 'General Fitness Check'}
- Strict Allergens to Flag: {', '.join(selected_allergies) if selected_allergies else 'None specified'}
- Medical/Narrative Notes: {additional_notes if additional_notes else 'None provided'}
"""

# --- STEP 2: CONVERSATIONAL MEMORY INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vault_images" not in st.session_state:
    st.session_state.vault_images = []

# --- STEP 3: MULTI-IMAGE ACQUISITION CANVAS ---
st.subheader("📸 Frame Capture Pipeline")
col_cam, col_vault = st.columns([2, 3])

with col_cam:
    captured_file = st.camera_input("Position product packaging in center view")
    if captured_file is not None:
        img = Image.open(captured_file)
        
        # Guard against duplicates inside the active frame cycle
        if len(st.session_state.vault_images) == 0 or captured_file.name != st.session_state.get("last_uploaded_name", ""):
            st.session_state.vault_images.append(img)
            st.session_state.last_uploaded_name = captured_file.name
            st.success(f"Frame buffered into system memory! Canvas Count: {len(st.session_state.vault_images)}")

with col_vault:
    if st.session_state.vault_images:
        st.write("⚡ **Buffered Frame Stack Active:**")
        # Render thumbnails of all taken photos side-by-side
        thumb_cols = st.columns(min(len(st.session_state.vault_images), 4))
        for idx, thumb_img in enumerate(st.session_state.vault_images):
            with thumb_cols[idx % 4]:
                st.image(thumb_img, caption=f"Scan #{idx+1}", width=120)
        
        if st.button("🗑️ Clear Image Stack"):
            st.session_state.vault_images = []
            st.rerun()

st.markdown("---")

# --- STEP 4: INTERACTIVE CHAT ENGINE LAYOUT ---
st.subheader("💬 AI Clinical Consultation Stream")

# Render previous conversational statements
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System Execution Prompter
if user_message := st.chat_input("Ask a question about your scanned items..."):
    
    # 1. Display User Message Instantly
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)
        
    # 2. Build Multi-modal Prompt Strategy
    # Construct systemic ground truth logic framework
    system_logic_prompt = f"""
    You are an expert digital dietitian. You are analyzing an interactive product scan loop.
    
    CRITICAL OPERATION PROTOCOLS:
    1. Cross-reference all inputs against this profile context: {user_profile_context}
    2. Analyze the attached sequence of product photos sequentially. 
    3. If the user's query requires finer granular data that you cannot see in the current image stack, or if a photo is unclear, DO NOT guess. State your initial observation and explicitly request the user to take an additional focused scan.
    
    CURRENT CHAT HISTORY DIALOGUE FOR TRACKING CONTEXT:
    """
    
    # Pack background context strings, active image arrays, and current input together
    payload = [system_logic_prompt]
    
    # Compile chat history text strings into payload
    for msg in st.session_state.chat_history[:-1]:
        payload.append(f"{msg['role'].upper()}: {msg['content']}\n")
        
    # Inject our list of images directly into the multimodal generation array
    payload.extend(st.session_state.vault_images)
    
    # Inject current fresh query prompt
    payload.append(f"CURRENT USER INQUIRY: {user_message}\nASSISTANT SYSTEM OUTPUT:")
    
    # 3. Call Cloud Model Infrastructure
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data streams..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=payload
                )
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Execution Error: {e}")
