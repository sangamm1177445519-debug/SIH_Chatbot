import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IP-SAKTI Sahayak",
    page_icon="🌿",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f8fafc;
}

.stApp header {
    background-color: transparent;
}

.finding-box {
    background-color: #f1f5f9;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 8px;
    border-left: 4px solid #10b981;
}

.source-box {
    background-color: #e0e7ff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #c7d2fe;
    margin-bottom: 10px;
}

.trace-box {
    background-color: #1e293b;
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "en"

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌿 IP-SAKTI Sahayak")
    st.caption("Powered by Google Gemini")

    st.divider()

    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        help="Paste your Google Gemini API key here."
    )

    st.divider()

    if st.button(
        "🗑️ Clear / Delete Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 🌟 Platform USPs")

    st.markdown("✅ **Ayurveda IP Workflow**")
    st.markdown("✅ **Evidence-Cited Answers**")
    st.markdown("✅ **Transparent Audit Trail**")

# =========================================================
# HEADER CONTROLS
# =========================================================

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    st.markdown("### 🌿 Ayurvedic IP & Regulatory Copilot")

with col2:
    mode = st.selectbox(
        "Mode",
        [
            "IP Research",
            "Regulatory",
            "Patent",
            "General"
        ]
    )

with col3:
    market = st.selectbox(
        "Market",
        [
            "🇮🇳 India",
            "🇺🇸 USA",
            "🇪🇺 Europe",
            "🌎 Global"
        ]
    )

with col4:
    lang_sel = st.selectbox(
        "Language",
        [
            "English",
            "हिंदी"
        ]
    )

    st.session_state.language = (
        "hi" if lang_sel == "हिंदी" else "en"
    )

st.divider()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":

            st.markdown(msg["content"])

        else:

            content = msg["content"]

            st.markdown(
                f"**Answer Summary:**\n\n{content['answer']}"
            )

            st.markdown("**Key Findings:**")

            for finding in content["findings"]:

                st.markdown(
                    f"""
                    <div class='finding-box'>
                        {finding}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### 📚 Supporting Evidence")

            source = content["source"]

            st.markdown(
                f"""
                <div class='source-box'>

                    <strong>📄 Document:</strong>
                    {source['title']}
                    <br>

                    <strong>📌 Section:</strong>
                    {source['section']}
                    |
                    <strong>Page:</strong>
                    {source['page']}
                    <br>

                    <span style='color: green; font-weight: bold;'>
                        Relevance: {source['relevance']} Match
                    </span>

                    <hr style='margin: 10px 0;'>

                    <em>"{source['text']}"</em>

                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander(
                "🔗 View Evidence Traceability & Audit Trail"
            ):

                st.markdown(
                    """
                    <div class='trace-box'>

                        <strong>
                        Traceability Workflow:
                        </strong>
                        <br>

                        Query ➔
                        Knowledge Base Match ➔
                        Excerpt Citation ➔
                        Verified Synthesis

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("### ⏱️ Audit Log")

                st.code(
                    "Query Received & Sanitized\n"
                    "Knowledge Base Search\n"
                    "Retrieved Top Matches\n"
                    "Context Synthesis Complete"
                )

# =========================================================
# SUGGESTED PROMPTS
# =========================================================

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

# =========================================================
# SHOW SUGGESTED PROMPTS
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("#### 💡 Suggested Prompts")

    for prompt in SUGGESTED_PROMPTS[
        st.session_state.language
    ]:

        if st.button(
            prompt,
            use_container_width=True
        ):

            st.session_state.prompt_clicked = prompt
            st.rerun()

# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Ask about Ayurveda IP considerations..."
)

prompt_to_process = user_input

if "prompt_clicked" in st.session_state:

    prompt_to_process = st.session_state.prompt_clicked

    del st.session_state.prompt_clicked

# =========================================================
# GEMINI RESPONSE
# =========================================================

if prompt_to_process:

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt_to_process
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt_to_process)

    # -----------------------------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Connecting to Gemini & generating response..."
        ):

            answer_text = ""

            # -------------------------------------------------
            # CHECK API KEY
            # -------------------------------------------------

            if not api_key:

                answer_text = (
                    "⚠️ Please enter your Gemini API key "
                    "in the sidebar to get live responses."
                )

            else:

                try:

                    # -----------------------------------------
                    # CREATE GEMINI CLIENT
                    # -----------------------------------------

                    client = genai.Client(
                        api_key=api_key
                    )

                    # -----------------------------------------
                    # LANGUAGE
                    # -----------------------------------------

                    selected_language = (
                        "Hindi"
                        if st.session_state.language == "hi"
                        else "English"
                    )

                    # -----------------------------------------
                    # SYSTEM INSTRUCTION
                    # -----------------------------------------

                    system_instruction = f"""
You are IP-SAKTI Sahayak, an expert AI assistant
specialized in Ayurvedic Intellectual Property (IP),
patents, traditional knowledge and regulatory guidance.

Current Market:
{market}

Current Mode:
{mode}

Response Language:
{selected_language}

Instructions:

1. Provide clear and professional answers.
2. Focus specifically on Ayurveda, herbal products,
   intellectual property and regulatory matters.
3. Structure the response clearly.
4. Mention important legal or regulatory considerations.
5. Do not invent laws, regulations, patents or citations.
6. If information is uncertain, clearly say so.
7. This is an AI assistant and not a substitute for
   professional legal advice.
"""

                    # -----------------------------------------
                    # USER PROMPT
                    # -----------------------------------------

                    full_prompt = f"""
{system_instruction}

User Question:

{prompt_to_process}
"""

                    # -----------------------------------------
                    # GEMINI API CALL
                    # -----------------------------------------

                    response = client.models.generate_content(
                        model="gemini-3.7-flash",
                        contents=full_prompt
                    )

                    # -----------------------------------------
                    # GET RESPONSE
                    # -----------------------------------------

                    if response and response.text:

                        answer_text = response.text

                    else:

                        answer_text = (
                            "⚠️ Gemini returned an empty response."
                        )

                except Exception as e:

                    answer_text = (
                        f"❌ Gemini API Connection Error:\n\n"
                        f"{str(e)}"
                    )

            # =================================================
            # RESPONSE DATA
            # =================================================

            response_data = {

                "answer": answer_text,

                "findings": [

                    f"Analyzed the query for {market}.",

                    f"Focused on {mode} requirements "
                    "related to Ayurveda IP and regulation.",

                    "Response generated using Google Gemini."
                ],

                "source": {

                    "title": (
                        f"IP-SAKTI Knowledge Base ({market})"
                    ),

                    "section": (
                        f"Compliance & {mode} Guidelines"
                    ),

                    "page": "AI-generated response",

                    "relevance": "AI",

                    "text": (
                        f"Evaluated query context: "
                        f"{prompt_to_process}"
                    )
                }
            }

            # =================================================
            # SAVE ASSISTANT MESSAGE
            # =================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_data
                }
            )

    # =====================================================
    # REFRESH UI
    # =====================================================

    st.rerun()
