import streamlit as st
import requests
import time

st.set_page_config(page_title="Document Q&A Chat", layout="wide")

# -------------------------------
# INITIALIZE SESSION STATE
# -------------------------------
defaults = {
    "chat_history": [],
    "uploaded_file": None,
    "document_indexed": False,
    "user_name": "",
    "awaiting_name": True,
    "pending_question": None,
    "confirm_end": False
}

for key, value in defaults.items():
    st.session_state.setdefault(key, value)

# -------------------------------
# CHAT BUBBLES
# -------------------------------
def user_bubble(text):
    st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin:6px 0;">
            <div style="
                max-width:70%; background-color:#4CAF50; color:white; padding:14px;
                border-radius:18px 18px 0 18px; word-wrap:break-word; font-size:15px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
                {text}
            </div>
        </div>""", unsafe_allow_html=True)

def bot_bubble(text):
    st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; margin:6px 0;">
            <div style="
                max-width:70%; background-color:#F1F1F1; color:#000; padding:14px;
                border-radius:18px 18px 18px 0; word-wrap:break-word; font-size:15px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
                {text}
            </div>
        </div>""", unsafe_allow_html=True)

# -------------------------------
# RENDER CHAT
# -------------------------------
chat_container = st.container()
def render_chat():
    chat_container.empty()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                user_bubble(msg["content"])
            else:
                bot_bubble(msg["content"])

# -------------------------------
# END CHAT BUTTON WITH CONFIRMATION
# -------------------------------
if st.session_state.user_name:
    if not st.session_state.confirm_end:
        if st.button("End Chat"):
            st.session_state.confirm_end = True
            st.rerun()
    else:
        st.markdown("<b>Are you sure you want to end the chat?</b>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, End Chat"):
                for key, value in defaults.items():
                    st.session_state[key] = value
                st.session_state.confirm_end = False
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.confirm_end = False
                st.rerun()

# Apply button colors via CSS
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ff4b4b !important;
    color: white !important;
    font-weight: bold !important;
}
div.stButton > button:last-child {
    background-color: #4CAF50 !important;
    color: white !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("Document Q&A Chatbot")

# -------------------------------
# STEP 1: NAME INPUT
# -------------------------------
if st.session_state.awaiting_name:
    with st.form("name_form"):
        name_input = st.text_input("Hello! What's your name?")
        submit_name = st.form_submit_button("Submit Name")

    if submit_name:
        if not name_input.strip():
            st.warning("Please enter your name.")
        else:
            st.session_state.user_name = name_input.strip()
            st.session_state.awaiting_name = False
            st.session_state.chat_history.append({
                "role": "bot",
                "content": f"Hi {st.session_state.user_name}! Please upload your PDF to start."
            })
            st.rerun()

# -------------------------------
# STEP 2: PDF UPLOAD
# -------------------------------
if st.session_state.user_name and not st.session_state.uploaded_file:
    uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        placeholder = st.empty()
        placeholder.info("Uploading document...")

        try:
            resp = requests.post(
                "http://localhost:5678/webhook/upload_pdf",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )
            if resp.status_code == 200:
                st.session_state.document_indexed = True
                st.session_state.chat_history.append({
                    "role": "bot",
                    "content": "Document indexed successfully! Ask your questions."
                })
                placeholder.success("Document indexed successfully!")
            else:
                placeholder.error(f"Upload failed: {resp.text}")
                st.session_state.uploaded_file = None

        except Exception as e:
            placeholder.error(f"Error: {e}")
            st.session_state.uploaded_file = None

        time.sleep(1)
        st.rerun()

# -------------------------------
# RENDER CHAT AREA
# -------------------------------
render_chat()
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------
# INPUT BOX
# -------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Type your question here…")
    send = st.form_submit_button("Send")

# -------------------------------
# HANDLE USER MESSAGE
# -------------------------------
if send:
    if not st.session_state.document_indexed:
        st.warning("Please upload your PDF first.")
        st.stop()
    if not user_input.strip():
        st.warning("Please enter a question.")
        st.stop()

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "bot", "content": "_Bot is typing…_"})
    st.session_state.pending_question = user_input
    st.rerun()

# -------------------------------
# PROCESS PENDING QUESTION
# -------------------------------
if st.session_state.pending_question:
    time.sleep(1)
    try:
        resp = requests.post(
            "http://localhost:5678/webhook/ask_question",
            json={"question": st.session_state.pending_question}
        )
        if resp.status_code == 200:
            data = resp.json()
            answer = (
                data[0]["content"]["parts"][0]["text"]
                if isinstance(data, list)
                else data.get("answer", "No answer returned.")
            )
        else:
            answer = f"Error: {resp.text}"
    except Exception as e:
        answer = f"Exception: {e}"

    st.session_state.chat_history[-1] = {"role": "bot", "content": answer}
    st.session_state.pending_question = None
    st.rerun()
