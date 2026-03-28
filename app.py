import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightCrew · Agentic Research Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@300;400&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0a0f; }
.hero-title {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -1px;
    background: linear-gradient(135deg, #e0ff4f 0%, #00e5ff 60%, #ff6bff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.1; margin-bottom: 0.3rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace; font-size: 0.85rem;
    color: #666; letter-spacing: 0.08em; text-transform: uppercase;
}
.agent-card {
    background: #12121a; border: 1px solid #222; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 0.7rem;
}
.agent-card h4 { color: #e0ff4f; font-size: 0.9rem; margin: 0 0 0.3rem; }
.agent-card p  { color: #888; font-size: 0.82rem; margin: 0; font-family: 'DM Mono', monospace; }
.result-box {
    background: #0e0e18; border: 1px solid #2a2a40;
    border-radius: 16px; padding: 2rem; color: #d0d0e8;
    font-family: 'DM Mono', monospace; font-size: 0.88rem;
    line-height: 1.7; white-space: pre-wrap; word-break: break-word;
}
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.72rem; font-family: 'DM Mono', monospace;
    background: #1a1a2e; border: 1px solid #2a2a50; color: #888;
    margin-right: 6px; margin-bottom: 4px;
}
.stButton > button {
    background: linear-gradient(135deg, #e0ff4f, #00e5ff) !important;
    color: #000 !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    padding: 0.65rem 2rem !important; font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important; transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }
.stTextInput input, .stTextArea textarea {
    background: #12121a !important; border: 1px solid #333 !important;
    color: #eee !important; border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
}
section[data-testid="stSidebar"] { background: #090910 !important; border-right: 1px solid #1a1a2a; }
.divider { border: none; border-top: 1px solid #1e1e2e; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">InsightCrew</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Multi-Agent Research Engine</div>', unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("**🔑 API Keys**")
    google_api_key = st.text_input(
        "Google Gemini API Key", type="password",
        value=os.environ.get("GOOGLE_API_KEY", ""),
        help="Get free key at aistudio.google.com"
    )
    tavily_api_key = st.text_input(
        "Tavily Search API Key", type="password",
        value=os.environ.get("TAVILY_API_KEY", ""),
        help="Get 1000 free credits/month at tavily.com"
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("**🤖 Agent Crew**")
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Senior Research Analyst</h4>
        <p>Scours the web for deep technical data, trends & expert opinions</p>
    </div>
    <div class="agent-card">
        <h4>✍️ Strategic Content Planner</h4>
        <p>Transforms raw research into LinkedIn-ready hooks & summaries</p>
    </div>
    <div class="agent-card">
        <h4>🧐 Proofreader / Editor</h4>
        <p>Eliminates hallucinations, ensures accuracy & professional tone</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.75rem; color:#555; font-family:'DM Mono',monospace;">
    <span class="badge">CrewAI</span>
    <span class="badge">Gemini 2.0 Flash</span>
    <span class="badge">Tavily Search</span>
    <span class="badge">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">InsightCrew 🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multi-Agent · Research · Content Generation · Always Free</div>', unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input(
        "**Research Topic**",
        placeholder="e.g.  Agentic AI frameworks in 2025, LLM fine-tuning trends, ...",
        help="Enter any topic you want to research deeply"
    )
with col2:
    output_style = st.selectbox(
        "**Output Style**",
        ["Report + LinkedIn Post", "Technical Deep-Dive", "Executive Summary"],
        help="Choose how the final output should be structured"
    )

run_btn = st.button("⚡ Launch Agent Crew", use_container_width=True)


# ── Agent Logic ───────────────────────────────────────────────────────────────
def build_crew(topic: str, style: str, g_key: str, t_key: str):
    os.environ["GOOGLE_API_KEY"] = g_key
    os.environ["TAVILY_API_KEY"] = t_key

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=g_key,
        temperature=0.4,
    )

    search_tool = TavilySearchResults(max_results=5)

    # ── Agents ──
    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Uncover the latest, most credible developments, trends, and diverse expert perspectives on: {topic}",
        backstory=(
            "You are a seasoned research analyst with 15 years of experience tracking "
            "technology trends. You excel at finding non-obvious insights from niche blogs, "
            "academic papers, and technical documentation. You always cite sources."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Strategic Content Planner",
        goal="Transform complex research into compelling, value-driven content tailored for LinkedIn professionals",
        backstory=(
            "You are a former tech journalist turned content strategist. You know how to "
            "distill complex technical ideas into crisp hooks and narratives that get engagement. "
            "You write for senior professionals, not beginners."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    editor = Agent(
        role="Proofreader and Editor",
        goal="Ensure factual accuracy, eliminate hallucinations, and polish for professional tone",
        backstory=(
            "You are a meticulous editor from a top-tier publication. You fact-check every "
            "claim, remove vague buzzwords, and make sure every sentence earns its place. "
            "You verify that information aligns with cited sources."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # ── Tasks ──
    if style == "Report + LinkedIn Post":
        expected_output = (
            "A structured report with:\n"
            "1. EXECUTIVE SUMMARY (3 bullet points)\n"
            "2. KEY FINDINGS (5 deep insights with sources)\n"
            "3. THREE EXPERT PERSPECTIVES (different viewpoints)\n"
            "4. LINKEDIN POST (150 words, punchy hook, 5 hashtags)"
        )
    elif style == "Technical Deep-Dive":
        expected_output = (
            "A technical report with:\n"
            "1. TECHNICAL OVERVIEW\n"
            "2. CURRENT STATE OF THE ART (with concrete examples)\n"
            "3. LIMITATIONS & OPEN PROBLEMS\n"
            "4. FUTURE DIRECTIONS"
        )
    else:
        expected_output = (
            "An executive summary with:\n"
            "1. ONE-PARAGRAPH OVERVIEW\n"
            "2. TOP 3 STRATEGIC IMPLICATIONS\n"
            "3. RECOMMENDED ACTIONS\n"
            "4. BOTTOM LINE"
        )

    task_research = Task(
        description=(
            f"Research the topic: **{topic}**\n\n"
            "Your deliverables:\n"
            "- Search the web for the latest developments (last 6 months prioritized)\n"
            "- Identify at least 3 distinct expert viewpoints or schools of thought\n"
            "- Collect 5+ concrete data points, statistics, or examples\n"
            "- Note any controversies or ongoing debates\n"
            "- List all sources used"
        ),
        expected_output="A comprehensive research brief with findings, viewpoints, data points, and sources",
        agent=researcher,
    )

    task_write = Task(
        description=(
            f"Using the research brief provided, create a **{style}** on: {topic}\n\n"
            "Requirements:\n"
            "- Follow the expected output format exactly\n"
            "- Use active voice, avoid jargon unless necessary\n"
            "- LinkedIn post must have a strong hook in the first line\n"
            "- Include relevant emojis sparingly for LinkedIn section only"
        ),
        expected_output=expected_output,
        agent=writer,
        context=[task_research],
    )

    task_edit = Task(
        description=(
            "Review the complete draft for:\n"
            "1. Factual accuracy — flag and remove any claims not supported by the research\n"
            "2. Professional tone — remove fluff, buzzwords, and vague statements\n"
            "3. Clarity — ensure every section is crisp and actionable\n"
            "4. Polish — fix grammar, flow, and formatting\n\n"
            "Output the FINAL polished version ready for publication."
        ),
        expected_output="Final polished, publication-ready content in the requested format",
        agent=editor,
        context=[task_research, task_write],
    )

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[task_research, task_write, task_edit],
        process=Process.sequential,
        verbose=True,
    )

    return crew


# ── Run ───────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")
    elif not google_api_key:
        st.error("❌ Google Gemini API Key is required. Add it in the sidebar.")
    elif not tavily_api_key:
        st.error("❌ Tavily API Key is required. Add it in the sidebar.")
    else:
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("**🔄 Agent Status**")

        status_placeholder = st.empty()
        result_placeholder = st.empty()

        with st.spinner("🤖 Agents are working... (this takes 1–3 minutes)"):
            try:
                status_placeholder.info(
                    "🔍 **Researcher** is scouring the web...\n\n"
                    "✍️ **Writer** is on standby...\n\n"
                    "🧐 **Editor** is on standby..."
                )
                crew = build_crew(topic, output_style, google_api_key, tavily_api_key)
                result = crew.kickoff(inputs={"topic": topic})
                final_text = str(result)

                status_placeholder.success("✅ All agents completed successfully!")
                st.markdown("### 📄 Final Output")
                st.markdown(f'<div class="result-box">{final_text}</div>', unsafe_allow_html=True)

                st.download_button(
                    label="⬇️ Download as .txt",
                    data=final_text,
                    file_name=f"insightcrew_{topic[:30].replace(' ','_')}.txt",
                    mime="text/plain",
                )

            except Exception as e:
                status_placeholder.error(f"❌ Error: {e}")
                st.markdown(
                    "**Troubleshooting:**\n"
                    "- Verify your API keys are correct\n"
                    "- Ensure you have free quota remaining\n"
                    "- Try a shorter/simpler topic"
                )