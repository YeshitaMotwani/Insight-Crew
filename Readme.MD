# 🚀 InsightCrew — Multi-Agent Research & Content Engine

> A  Agentic AI app that replaces hours of research with 3 autonomous AI agents working in sequence. Built 100% free and deployed publicly.

![InsightCrew Demo](https://img.shields.io/badge/Built%20With-CrewAI%20%7C%20Gemini%202.0%20%7C%20Tavily-blueviolet?style=for-the-badge)
![Free Forever](https://img.shields.io/badge/Deployment-Streamlit%20Cloud%20(Free)-brightgreen?style=for-the-badge)

---

## 🧠 How It Works

Three agents collaborate in a **sequential pipeline**:

| Agent | Role | Tool |
|---|---|---|
| 🔍 Senior Research Analyst | Searches the web, finds trends & expert views | Tavily Search |
| ✍️ Strategic Content Planner | Writes reports & LinkedIn posts | Gemini 2.0 Flash |
| 🧐 Proofreader / Editor | Fact-checks, removes hallucinations, polishes | Gemini 2.0 Flash |

---

## ✅ Completely Free Stack

| Component | Service | Free Tier |
|---|---|---|
| Orchestration | [CrewAI](https://crewai.com) | Open-source |
| LLM | [Google Gemini 2.0 Flash](https://aistudio.google.com) | 15 req/min, 1M tokens/day |
| Search | [Tavily AI](https://tavily.com) | 1,000 credits/month |
| UI | [Streamlit](https://streamlit.io) | Open-source |
| Hosting | [Streamlit Cloud](https://share.streamlit.io) | Free forever |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/insight-crew
cd insight-crew

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open `http://localhost:8501` and enter your API keys in the sidebar.

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub (make sure it's **public**)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New App**
3. Select your repo and set `app.py` as the main file
4. Under **Advanced Settings → Secrets**, add:

```toml
GOOGLE_API_KEY = "your-gemini-api-key"
TAVILY_API_KEY = "your-tavily-api-key"
```

5. Click **Deploy** — you get a live public URL instantly! 🎉

---

## 🔑 Get Your Free API Keys

- **Google Gemini:** [aistudio.google.com](https://aistudio.google.com) → Create API Key (free)
- **Tavily Search:** [tavily.com](https://tavily.com) → Sign up → 1,000 free searches/month

---

## 📈 LinkedIn Posting Strategy

Use this structure for maximum reach:

**Hook:** *"I replaced my 4-hour research workflow with 3 autonomous AI agents."*

**Why it matters:** Traditional RAG just retrieves. Agentic workflows **reason, delegate, and self-correct.**

**Proof:** Share a GIF/screenshot of the app running + your live URL.

**CTA:** Link to this GitHub repo and your Streamlit app.

---

## 🛠️ Built With

- [CrewAI](https://crewai.com) — multi-agent orchestration
- [LangChain Google GenAI](https://python.langchain.com) — Gemini integration
- [Tavily](https://tavily.com) — real-time web search
- [Streamlit](https://streamlit.io) — UI & deployment

---

*Made with ❤️ — Star ⭐ this repo if it helped you!*