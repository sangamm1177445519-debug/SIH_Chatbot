import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IP-SAKTI Sahayak", page_icon="🌿", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    .stApp header {background-color: transparent;}
    .main {background-color: #f8fafc;}
    .css-1d391kg {background-color: #0f172a;}
    .stChatFloatingInputContainer {padding-bottom: 20px;}
    .finding-box {background-color: #f1f5f9; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #10b981;}
    .source-box {background-color: #e0e7ff; padding: 15px; border-radius: 10px; border: 1px solid #c7d2fe; margin-bottom: 10px;}
    .trace-box {background-color: #1e293b; color: white; padding: 15px; border-radius: 10px; margin-top: 15px;}
</style>
""", unsafe_allow_html=True)

# --- MOCK DATA ---
SUGGESTED_PROMPTS = {
    "en": [
        "What are the IP considerations for an Ayurveda formulation?",
        "Compare IP rules for polyherbal formulations in India and USA.",
        "What regulatory requirements apply to herbal extracts?"
    ],
    "hi": [
        "आयुर्वेद आधारित हर्बल फॉर्मूलेशन के लिए बौद्धिक संपदा (IP) नियम क्या हैं?",
        "भारत और अमेरिका में आयुर्वेदिक फॉर्मूलेशन के आईपी प्रावधानों की तुलना करें।",
        "हर्बल अर्क के लिए कौन सी नियामक आवश्यकताएं लागू होती हैं?"
    ]
}

MOCK_RESPONSE = {
    "en": {
        "answer": "For an Ayurveda-based herbal formulation, key IP considerations involve avoiding patent eligibility rejections under traditional knowledge frameworks (such as Section 3(p) of the Indian Patents Act), and documenting prior art disclosures via the TKDL.",
        "findings": [
            "Traditional formulations documented in classical texts are considered prior art.",
            "Novel non-obvious synergistic effects must be proven with empirical data.",
            "Compliance with the National Biodiversity Act (NBA) is mandatory in India."
        ],
        "source": {
            "title": "Ayurveda IP & Patentability Guidelines 2026",
            "section": "Section 3(p) Considerations",
            "page": "Page 12",
            "relevance": "94%",
            "text": "Under Section 3(p) of the Indian Patent Act, an invention which in effect is traditional knowledge is not patentable. Applicants must prove synergistic data."
        }
    },
    "hi": {
        "answer": "आयुर्वेद-आधारित हर्बल फॉर्मूलेशन के लिए, मुख्य बौद्धिक संपदा (IP) विचार पारंपरिक ज्ञान ढांचे (जैसे भारतीय पेटेंट अधिनियम की धारा 3(p)) के तहत अस्वीकृति से बचने और TKDL द्वारा पूर्व कला (Prior Art) का सत्यापन करने पर केंद्रित हैं।",
        "findings": [
            "शास्त्रीय ग्रंथों में प्रलेखित पारंपरिक ज्ञान सार्वजनिक संपत्ति माना जाता है।",
            "पेटेंट के लिए अप्रत्याशित सहक्रियात्मक प्रभाव के प्रायोगिक आंकड़े प्रस्तुत करने होंगे।",
            "भारतीय जैविक संसाधनों के उपयोग हेतु अनुमति लेना अनिवार्य है।"
        ],
        "source": {
            "title": "आयुर्वेद आईपी मार्गदर्शन 2026",
            "section": "धारा 3(p) विचार",
            "page": "पृष्ठ 12",
            "relevance": "94%",
            "text": "भारतीय पेटेंट अधिनियम की धारा 3(p) के तहत, जो आविष्कार पारंपरिक ज्ञान है वह पेटेंट योग्य नहीं है।"
        }
    }
}

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "en"

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌿 IP-SAKTI Sahayak")
    st.caption("SIH AI Research Prototype")
    
    if st.button("➕ New Research Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### 🌟 Platform USPs")
    st.markdown("✅ **Ayurveda IP Workflow**")
    st.markdown("✅ **Evidence-Cited Answers**")
    st.markdown("✅ **Evidence Traceability**")
    st.markdown("✅ **Transparent Audit Trail**")

# --- HEADER CONTROLS ---
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown("### 🌿 Ayurvedic IP & Regulatory Copilot")
with col2:
    mode = st.selectbox("Mode", ["IP Research", "Regulatory", "Patent", "General"])
with col3:
    market = st.selectbox("Market", ["🇮🇳 India", "🇺🇸 USA", "🇪🇺 Europe", "🌎 Global"])
with col4:
    lang_sel = st.selectbox("Language", ["English", "हिंदी"])
    st.session_state.language = "hi" if lang_sel == "हिंदी" else "en"

st.divider()

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            # AI Response Format
            st.markdown(f"**Answer Summary:**\n\n{msg['content']['answer']}")
            
            st.markdown("**Key Findings:**")
            for f in msg['content']['findings']:
                st.markdown(f"<div class='finding-box'>{f}</div>", unsafe_allow_html=True)
            
            # Evidence Source
            st.markdown("### 📚 Supporting Evidence")
            src = msg['content']['source']
            st.markdown(f"""
            <div class='source-box'>
                <strong>📄 Document:</strong> {src['title']} <br>
                <strong>📌 Section:</strong> {src['section']} | <strong>Page:</strong> {src['page']} <br>
                <span style='color: green; font-weight: bold;'>Relevance: {src['relevance']} Match</span>
                <hr style='margin: 10px 0;'>
                <em>"{src['text']}"</em>
            </div>
            """, unsafe_allow_html=True)

            # Traceability & Audit Trail
            with st.expander("🔗 View Evidence Traceability & Audit Trail"):
                st.markdown("""
                <div class='trace-box'>
                    <strong>Traceability Workflow:</strong><br>
                    Query ➔ Document Match (TKDL) ➔ Excerpt Citation (Section 3(p)) ➔ Final Verified Answer
                </div>
                """, unsafe_allow_html=True)
                st.markdown("### ⏱️ Audit Log")
                st.code("10:42 AM - User Query Received & Sanitized\n10:42 AM - Vector Search in Ayurveda IP DB\n10:43 AM - Retrieved Top 3 Matches\n10:43 AM - Context Synthesis Complete\n10:43 AM - Result Displayed to User")

# --- SUGGESTED PROMPTS ---
if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Suggested Prompts")
    prompts = SUGGESTED_PROMPTS[st.session_state.language]
    for prompt in prompts:
        if st.button(prompt):
            st.session_state.prompt_clicked = prompt
            st.rerun()

# --- INPUT HANDLING ---
user_input = st.chat_input("Ask about Ayurveda IP considerations...")
prompt_to_process = user_input

if "prompt_clicked" in st.session_state:
    prompt_to_process = st.session_state.prompt_clicked
    del st.session_state.prompt_clicked

if prompt_to_process:
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    with st.chat_message("user"):
        st.markdown(prompt_to_process)

    with st.chat_message("assistant"):
        with st.spinner("Synthesizing Ayurveda IP Citations & Evidence..."):
            time.sleep(1.2)
            lang = st.session_state.language
            response_data = MOCK_RESPONSE[lang]
            st.session_state.messages.append({"role": "assistant", "content": response_data})
            st.rerun()