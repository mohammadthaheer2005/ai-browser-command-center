# 🤖 AI Agent Pro - Ultimate Browser Command Center

**AI Agent Pro** is a next-generation autonomous AI assistant that goes beyond simple chatbots. It's a fully intelligent agent capable of controlling your web browser like a human, performing complex multi-step tasks, and maintaining memory across sessions.

---

## 🌟 Unique & Standout Features

### 1. 🧠 **Intelligent Task Memory & Chaining**
Unlike standard bots, AI Agent Pro **remembers** your previous tasks and can chain them together:
- **Example:** "Find the best iPhone prices on Amazon and Flipkart" → "Now send those links to my WhatsApp contact"
- The agent automatically uses the results from Task 1 to complete Task 2 without you repeating anything!

### 2. 💬 **WhatsApp Auto-Reply with AI Intelligence**
A dedicated continuous monitoring system that:
- Automatically detects unread messages in real-time
- Replies naturally in the sender's language (English, Hindi, Tamil, etc.)
- **Smart Security:** Refuses to share passwords, OTPs, or payment information
- **Live Research:** If a friend asks for code or product links, the agent searches the web and sends accurate answers
- **One-Time Login:** Scan QR code once, stay logged in across sessions

### 3. 🎓 **Education Mode - Your Personal Coding Tutor**
Get instant, high-quality educational content:
- **Clean Code Blocks:** Perfectly formatted, copy-paste ready code in Python, Java, C++, etc.
- **Step-by-Step Explanations:** Detailed breakdowns of concepts
- **Math Solver:** Solves probability, calculus, and algebra problems with clear logic
- **No Markdown Mess:** Output is clean and readable, not cluttered with symbols

### 4. 🎙️ **Voice-Activated Execution**
Speak your commands naturally:
- "Hey Agent, play the latest movie trailer on YouTube"
- "Find laptop prices under 80k and compare them"
- Hands-free operation with high-accuracy speech recognition

### 5. 🎬 **YouTube Ad-Skipper**
Automatically detects and clicks "Skip Ad" buttons instantly - no more waiting!

### 6. 🛒 **Multi-Platform Shopping Brain**
Visits Amazon, Flipkart, and other e-commerce sites simultaneously to:
- Extract product links
- Compare prices
- Find the best ratings
- Deliver results in seconds

### 7. 🔒 **Smart Security & Privacy**
- **Session Logout:** WhatsApp login data is automatically deleted when you exit the app
- **No Hardcoded Keys:** Each user must provide their own API key (your credentials are never shared)
- **Anti-Scam Protection:** Blocks requests for sensitive information on WhatsApp

### 8. 🎯 **Strict Task Scoping**
Each button has a specific purpose and won't interfere with others:
- **Ask Question** → Only searches the web (Google, Wikipedia)
- **Education Mode** → Only provides learning content
- **WhatsApp Auto** → Only handles messaging
- **Main Task Bar** → Full combination power for complex workflows

---

## 🛠️ Technology Stack

- **AI Brain:** Google Gemini 1.5 Pro / OpenAI GPT-4o
- **Automation Engine:** `browser-use` + Playwright
- **Interface:** Python Tkinter (Premium Dark Theme with Glassmorphism)
- **Voice Recognition:** Google Speech API
- **Packaging:** PyInstaller (Single-Folder Distribution)

---

## 🌎 Real-World Use Cases

### Use Case 1: Smart Shopping Assistant
**Command:** "Find the cheapest Samsung S24 Ultra on Amazon and Flipkart, then send the links to my WhatsApp group"

**What happens:**
1. Agent opens Amazon and Flipkart in separate tabs
2. Searches for the product
3. Extracts the best prices and direct links
4. Navigates to WhatsApp Web
5. Sends the comparison to your specified contact

---

### Use Case 2: Automated Customer Support (WhatsApp)
**Scenario:** You're away from your phone, but need to handle customer queries

**What happens:**
1. Click "WhatsApp Auto"
2. Agent monitors all incoming messages
3. Replies professionally to common questions
4. If asked for product details or code examples, it searches the web and provides accurate answers
5. Refuses to share any sensitive information

---

### Use Case 3: Homework Helper
**Command:** "Solve this probability problem: A bag has 5 red and 3 blue marbles. What's the probability of drawing red?"

**What happens:**
1. Agent provides a step-by-step mathematical solution
2. Shows the formula and calculation
3. Delivers the final answer clearly

---

### Use Case 4: Entertainment on Demand
**Voice Command:** "Play 90s Bollywood hits on YouTube"

**What happens:**
1. Opens YouTube
2. Searches for the playlist
3. Starts playback
4. Automatically skips all ads

---

## 📋 System Requirements

- **OS:** Windows 10 or 11 (64-bit)
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 1GB free space
- **Internet:** Active connection required
- **API Key:** Google Gemini API (free from https://aistudio.google.com/app/apikey)

---

## 🚀 Installation & Setup

### For End Users (Executable)

1. **Download** the `AI_Agent_Pro_App` folder
2. **Extract** the folder to your desired location
3. **Install Playwright** (one-time setup):
   ```bash
   pip install playwright
   playwright install chromium
   ```
4. **Run** `AI_Agent_Pro.exe`
5. **Enter your API Key** when prompted (first run only)

### For Developers (Source Code)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI_Agent_Pro.git
   cd AI_Agent_Pro
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Set your API Key:**
   ```bash
   set GOOGLE_API_KEY=your_api_key_here
   ```

4. **Run the application:**
   ```bash
   python AgentApp.py
   ```

---

## 🎨 User Interface

The application features a **premium dark-mode interface** with:
- Sidebar with quick-action buttons
- Main task center with voice input
- Real-time console for monitoring agent actions
- Visual feedback for all operations

---

## 🔧 Advanced Features

### Task Memory System
The agent maintains a conversation history buffer that stores:
- Previous task descriptions
- Results (up to 2000 characters per task)
- Context for intelligent task chaining

### Persistent Browser Sessions
WhatsApp login is saved in a local `agent_browser_data` folder:
- Scan QR code once
- Stay logged in across all tasks
- Automatically cleared on app exit for security

### Multi-Threading Architecture
- GUI runs on the main thread
- Browser automation runs on background threads
- Async event loops for efficient task execution

---

## 📝 Example Commands

| Command | What It Does |
|---------|--------------|
| "Compare iPhone 15 vs Samsung S24" | Opens Amazon/Flipkart, extracts prices and specs |
| "Play Interstellar trailer" | Opens YouTube, plays video, skips ads |
| "Give me Python code for binary search" | Provides clean, executable code with explanation |
| "What's the current time in New York?" | Searches Google and returns the answer |
| "Send the laptop links to 9876543210 on WhatsApp" | Uses memory from previous search and sends via WhatsApp |

---

## 🛡️ Security & Privacy

- **No Data Collection:** All processing happens locally on your machine
- **API Key Protection:** Your credentials are stored in environment variables only
- **Session Isolation:** Each user's WhatsApp login is separate and secure
- **Auto-Logout:** Browser data is wiped on application exit

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Mohammad Thaheer**

This project was developed to bridge the gap between AI conversation and real-world web automation. It transforms the browser from a static tool into an intelligent, autonomous partner.

---

## 🙏 Acknowledgments

- **browser-use** - For the powerful browser automation framework
- **LangChain** - For LLM integration
- **Google Gemini** - For the AI brain
- **Playwright** - For reliable browser control

---

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the example commands above

---

## 🔮 Future Roadmap

- [ ] Support for more languages (Spanish, French, German)
- [ ] Integration with Telegram and Discord
- [ ] Custom automation workflows (user-defined scripts)
- [ ] Cloud sync for task history
- [ ] Mobile companion app

---

**⭐ If you find this project useful, please give it a star on GitHub!**

---

*Built with ❤️ using Python, AI, and lots of coffee ☕*
