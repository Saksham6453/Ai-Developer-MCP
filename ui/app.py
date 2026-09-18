import sys
from pathlib import Path

# ---------------------------------------------------------
# Project Path Setup
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
import asyncio
import streamlit as st
from client.agent import run_agent

# ---------------------------------------------------------
# Helper: Safe Async Runner for Streamlit
# ---------------------------------------------------------
def run_async(coro):
    """Execute an async coroutine from the Streamlit app."""
    return asyncio.run(coro)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DevMCP — AI Developer Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Header */
    .app-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }

    .header-badge {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: #ffffff;
        padding: 4px 10px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-radius: 9999px;
        text-transform: uppercase;
    }

    /* Welcome Hero Card */
    .welcome-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem auto 2rem auto;
        max-width: 680px;
    }

    /* Tool Call Badges */
    .tool-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.12);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px 0 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **DevMCP Control**")
    st.caption("Contextual codebase intelligence via Model Context Protocol.")
    st.markdown("---")

    st.markdown("**Active Environment**")
    st.success("🟢 DevMCP Ready", icon="✅")

    st.markdown("**Capabilities**")
    st.markdown("""
    - 🔍 AST & Semantic Search
    - 📄 Codebase File Reading
    - 🧩 Function & Class Discovery
    - 🌿 Git Status / Diff / Log
    """)
    st.markdown("---")

    if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------
# Header Bar
# ---------------------------------------------------------
st.markdown("""
<div class="app-header">
    <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.5px;">🛠️ DevMCP</h2>
    <span class="header-badge">MCP + Gemini</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tool Activity Renderer
# ---------------------------------------------------------
def render_tools(tools):
    if not tools:
        return
    with st.expander(f"⚙️ Tool Invocations ({len(tools)})", expanded=False):
        for tool in tools:
            st.markdown(
                f"<span class='tool-badge'>⚡ {tool.get('tool', 'Unknown Tool')}</span>",
                unsafe_allow_html=True
            )
            st.json(tool.get("arguments", {}))

# ---------------------------------------------------------
# Message Feed Rendering
# ---------------------------------------------------------
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("tools"):
            render_tools(message["tools"])

# ---------------------------------------------------------
# Empty State Quick Prompts
# ---------------------------------------------------------
pending_prompt = None

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h3 style="margin-bottom: 8px;">How can I assist your engineering flow?</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 0;">
            Ask questions about directory architecture, code references, functions, classes, or Git history.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Explain project structure", use_container_width=True):
            pending_prompt = "Can you analyze and explain the top-level structure of this repository?"
    with col2:
        if st.button("🧩 Trace login flow", use_container_width=True):
            pending_prompt = "Trace the login flow across the project and explain which files and functions are involved."
    with col3:
        if st.button("🌿 Check recent changes", use_container_width=True):
            pending_prompt = "Check the Git status, recent commits, and changes in this project and summarize them."

# ---------------------------------------------------------
# Input and Orchestration
# ---------------------------------------------------------
user_query = st.chat_input("Ask something about your codebase...") or pending_prompt

if user_query:
    # 1. Record & render user query
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)

    # 2. Agent Execution
    with st.chat_message("assistant", avatar="⚡"):
        with st.status("Analyzing codebase & running tools...", expanded=True) as status:
            st.write("Resolving context from MCP server...")
            try:
                answer, tool_activity = run_async(run_agent(user_query))
                status.update(label="Analysis complete!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Execution error", state="error", expanded=True)
                st.error(f"Agent failed to complete the request: {e}")
                answer = "I encountered an error while communicating with the agent backend."
                tool_activity = []

        st.markdown(answer)
        if tool_activity:
            render_tools(tool_activity)

    # 3. Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tools": tool_activity
    })