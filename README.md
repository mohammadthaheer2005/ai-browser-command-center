# 🤖 AI Browser Command Center

**The ultimate desktop workspace for browser automation and AI-driven productivity.**

AI Browser Command Center is a sophisticated desktop application that transforms how you interact with the web. By combining a modern Python GUI with powerful Agentic workflows, this tool can perform complex browser tasks—from automated research and product analysis to hands-on WhatsApp management—all through simple text or voice commands.

---

## 🚀 Vision
Standard AI assistants are often trapped in a chat box. **AI Browser Command Center** breaks those walls by giving the AI "hands" to navigate the web just like a human, but with the speed and precision of a machine.

## ✨ Core Capabilities
- **⚡ Fast Mode Results**: Prioritizes Google AI Overviews and Featured Snippets for near-instant responses to queries.
- **🎙️ Voice Intelligence**: Integrated speech-to-text allowing for a completely hands-free "Command Center" experience.
- **💬 WhatsApp Automation**: Context-aware auto-reply system that reads, understands, and responds to messages in your style (supports Hinglish/Tanglish).
- **🛒 Research & Logistics**: Automated comparison of products across multiple e-commerce platforms (Amazon, Flipkart) with pros/cons summarization.
- **▶️ Seamless Media**: Instant navigation and playback of YouTube content with ad-skipping logic.

## 🛠️ The Technology Stack
A lot of engineering went into making this experience smooth and reliable:
- **Python / Tkinter**: A sleek, dark-themed custom GUI designed for low latency.
- **Agentic AI**: Powered by `browser-use` and `LangChain`, utilizing Gemini 1.5 Pro and GPT-4o.
- **Automation Core**: Built on **Playwright** for robust browser session management.
- **Security Watchdog Bypass**: Custom-engineered monkey patches to allow safe, deep navigation without triggering standard library security freezes.

## 📦 Getting Started

### 1. Download & Launch
If you have the executable version:
1. Download the `AI_Agent_Pro.zip` from the Latest Release.
2. Extract and run `AI_Agent_Pro.exe`.
3. Enter your Gemini API Key when prompted (stored locally & encrypted in `.env_agent`).

### 2. Developer Setup
For those who want to run from source:
```bash
git clone https://github.com/mohammadthaheer2005/ai-browser-command-center.git
pip install -r requirements.txt
playwright install chromium
python AgentApp.py
```

## 🔒 Security & Privacy
We believe your data is yours. 
- **Local Storage**: Your API keys never touch our servers. They are stored right on your machine.
- **Visibility**: The browser session is visible, so you can see exactly what the AI is doing at every second.

---
**Crafted with precision by [Mohammad Thaheer](https://github.com/mohammadthaheer2005)**  
*Innovating the intersection of Browser Automation and Large Language Models.*
