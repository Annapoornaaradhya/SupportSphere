# app.py

import json
import html
import time

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pandas.errors import EmptyDataError

from config import APP_TITLE, APP_TAGLINE, ESCALATION_LOG, FAQS_FILE
from rag_pipeline import SupportRAGPipeline, log_escalation


# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💬",
    layout="wide"
)

# ----------------- LOAD RAG PIPELINE (ONE INSTANCE) -----------------
@st.cache_resource
def load_pipeline():
    return SupportRAGPipeline()

pipeline = load_pipeline()

# ----------------- CUSTOM CSS -----------------
custom_css = """
<style>
/* Global dark styling tweaks */
.main {
    background: radial-gradient(circle at top left, #111827, #020617);
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    border-right: 1px solid #1f2937;
}

/* Chat layout */
.chat-container {
    padding: 0.5rem 0.25rem;
}

/* Base row */
.chat-row {
    display: flex;
    margin-bottom: 0.6rem;
    align-items: flex-end;
}

/* Avatar circle */
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #e5e7eb;
    flex-shrink: 0;
}

/* Assistant row: avatar left, bubble right */
.chat-row-bot {
    justify-content: flex-start;
    gap: 0.4rem;
}

.chat-avatar-bot {
    background: linear-gradient(135deg, #22c55e, #06b6d4);
    border: 1px solid #0f766e;
}

/* User row: avatar right, bubble left but aligned to right side */
.chat-row-user {
    justify-content: flex-end;
    gap: 0.4rem;
}

.chat-avatar-user {
    background: linear-gradient(135deg, #4f46e5, #db2777);
    border: 1px solid #312e81;
}

/* Bubble wrappers */
.chat-bubble-wrapper {
    max-width: 75%;
}

/* User bubble: right side */
.chat-bubble-user {
    background: linear-gradient(135deg, #1d4ed8, #22c55e);
    padding: 0.75rem 1rem;
    border-radius: 14px;
    border: 1px solid #1d4ed8;
    color: #e5e7eb;
    font-size: 0.92rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.7);
}

/* Assistant bubble: left side */
.chat-bubble-bot {
    background: #020617;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    border: 1px solid #1f2937;
    color: #e5e7eb;
    font-size: 0.92rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.7);
}

/* Meta labels */
.chat-meta {
    font-size: 0.70rem;
    color: #9ca3af;
    margin-bottom: 0.15rem;
}

/* Hide Streamlit default menu & footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: visible;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------- HERO SECTION WITH JS EFFECTS -----------------
hero_html = """
<div id="particles-js" style="position:fixed; width:100%; height:100%; top:0; left:0; z-index:-1;"></div>

<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<div style="padding-top: 0.5rem; padding-bottom: 0.75rem;">
  <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.25rem;
             background: linear-gradient(90deg,#38bdf8,#a855f7,#22c55e);
             -webkit-background-clip: text; color: transparent;">
    SupportSphere
  </h1>
  <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.2rem;">
    <i class="fa-solid fa-headset"></i>
    <span id="typed-tagline" style="font-size: 1rem; color: #9ca3af;"></span>
  </div>
  <p style="font-size: 0.9rem; color:#6b7280;">
    Resolve FAQs instantly with a RAG-powered AI support assistant. Escalate only the complex queries to humans.
  </p>
</div>

<!-- Typed.js -->
<script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
  new Typed("#typed-tagline", {
    strings: [
      "AI that understands your FAQs.",
      "Reduce ticket load, not customer happiness.",
      "Smart support. Human when it matters."
    ],
    typeSpeed: 40,
    backSpeed: 20,
    backDelay: 1800,
    loop: true
  });
});
</script>

<!-- Particles.js -->
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 60},
    "color": {"value": "#38bdf8"},
    "shape": {"type": "circle"},
    "opacity": {"value": 0.3},
    "size": {"value": 3},
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#64748b",
      "opacity": 0.4,
      "width": 1
    },
    "move": {"enable": true, "speed": 2}
  },
  "interactivity": {
    "events": {
      "onhover": {"enable": true, "mode": "repulse"}
    }
  },
  "retina_detect": true
});
</script>
"""
components.html(hero_html, height=230)


# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.subheader("⚙️ Assistant Settings")

    tone = st.radio(
        "Reply Style",
        ["Formal", "Friendly"],
        index=0,
        help="Choose the tone of the support assistant's replies."
    )

    st.markdown("---")
    st.subheader("📚 FAQ Categories")

    with open(FAQS_FILE, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    categories = sorted(list({row["category"] for row in faq_data}))
    selected_category = st.selectbox(
        "Browse FAQs by Category",
        options=["All"] + categories
    )

    if selected_category == "All":
        filtered_faqs = faq_data
    else:
        filtered_faqs = [x for x in faq_data if x["category"] == selected_category]

    with st.expander("View Sample FAQs"):
        for row in filtered_faqs:
            st.markdown(f"**Q:** {row['question']}")
            st.markdown(f"**A:** {row['answer']}")
            st.caption(f"Category: {row['category']} | Tags: {', '.join(row.get('tags', []))}")
            st.markdown("---")

    st.markdown("---")
    st.caption("🔁 This demo uses local models + Pinecone vector store (free tier).")


# ----------------- SESSION STATE -----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of dicts with role, content

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

st.markdown("### 🗨️ Conversation")

# ----------------- HELPERS -----------------
def render_message(role: str, content: str) -> str:
    """Return HTML for a single message bubble."""
    safe = html.escape(content)
    if role == "user":
        return f"""
        <div class="chat-row chat-row-user">
            <div class="chat-bubble-wrapper">
                <div class="chat-bubble-user">
                    <div class="chat-meta">You</div>
                    <div>{safe}</div>
                </div>
            </div>
            <div class="chat-avatar chat-avatar-user">
                U
            </div>
        </div>
        """
    else:
        return f"""
        <div class="chat-row chat-row-bot">
            <div class="chat-avatar chat-avatar-bot">
                SS
            </div>
            <div class="chat-bubble-wrapper">
                <div class="chat-bubble-bot">
                    <div class="chat-meta">SupportSphere</div>
                    <div>{safe}</div>
                </div>
            </div>
        </div>
        """


def render_chat_static(container):
    """Render the full static chat history."""
    with container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.caption("Start the conversation by asking a support question below 👇")
        else:
            for msg in st.session_state.chat_history:
                st.markdown(
                    render_message(msg["role"], msg["content"]),
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)


# ----------------- CHAT AREA -----------------
chat_container = st.container()

# Clear chat button
clear_col, _ = st.columns([1, 3])
with clear_col:
    if st.button("🧹 Clear chat"):
        st.session_state.chat_history = []
        st.session_state.last_answer = None
        st.rerun()

# Initial render of existing history
render_chat_static(chat_container)

st.markdown("---")

# ----------------- INPUT AREA (BOTTOM) -----------------
# Use a form so the input clears automatically on submit
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])

    with col1:
        user_query = st.text_area(
            "💬 Ask a support question",
            placeholder="e.g. I forgot my password. How do I reset it?",
            height=100,
        )

    with col2:
        user_email = st.text_input(
            "Customer Email (optional)",
            placeholder="user@example.com"
        )

    submitted = st.form_submit_button("🚀 Get Answer", type="primary")

# Escalate button (outside form)
escalate_btn = st.button("⚠️ Escalate to Human", help="Use after you see the AI's answer.")

# ----------------- BUTTON LOGIC -----------------
if submitted and user_query.strip():
    question = user_query.strip()

    # 1️⃣ Re-render chat including previous history + NEW user message
    chat_container.empty()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

        # Old history
        for msg in st.session_state.chat_history:
            st.markdown(
                render_message(msg["role"], msg["content"]),
                unsafe_allow_html=True,
            )

        # New user message (appears immediately)
        st.markdown(
            render_message("user", question),
            unsafe_allow_html=True,
        )

        # Placeholder for assistant message (we'll "type" into this)
        assistant_placeholder = st.empty()

        st.markdown("</div>", unsafe_allow_html=True)

        # 2️⃣ Show spinner while RAG pipeline runs
        with st.spinner("SupportSphere is thinking with RAG..."):
            answer, docs = pipeline.answer_question(question, tone=tone)

        # 3️⃣ Typing effect for assistant reply (character by character)
        typed_text = ""
        for ch in answer:
            typed_text += ch
            assistant_placeholder.markdown(
                render_message("assistant", typed_text),
                unsafe_allow_html=True,
            )
            time.sleep(0.01)  # typing speed

    # 4️⃣ Update history AFTER full answer is typed
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # 5️⃣ Save last interaction for escalation
    st.session_state.last_answer = {
        "question": question,
        "answer": answer,
        "docs": docs,
        "user_email": user_email
    }

    # 6️⃣ Rerun so the whole chat is now static
    st.rerun()


# ----------------- ESCALATE TO HUMAN -----------------
if escalate_btn:
    if not st.session_state.last_answer:
        st.warning("Ask a question first before escalating.")
    else:
        last = st.session_state.last_answer
        log_escalation(
            user_question=last["question"],
            model_answer=last["answer"],
            reason="User clicked escalate button.",
            top_docs=last["docs"],
            user_email=last.get("user_email", "")
        )
        st.success("✅ Query logged for human support. They will review the conversation and follow up.")

        with st.expander("View what was logged"):
            st.write("**Question:**", last["question"])
            st.write("**AI Answer:**", last["answer"])
            st.write("**Top Retrieved FAQ entries:**")
            for d in last["docs"]:
                st.markdown(f"- **{d['question']}** (Category: {d.get('category', 'FAQ')})")


# ----------------- ESCALATION LOG VIEW -----------------
if ESCALATION_LOG.exists():
    with st.expander("📂 View Escalation Log (for supervisors)", expanded=False):
        try:
            if ESCALATION_LOG.stat().st_size > 0:
                df = pd.read_csv(ESCALATION_LOG)
                if not df.empty:
                    st.dataframe(df.tail(10))
                else:
                    st.info("No escalations logged yet.")
            else:
                st.info("No escalations logged yet.")
        except EmptyDataError:
            st.info("No escalations logged yet.")
        except Exception as e:
            st.error(f"Could not load escalation log: {e}")
