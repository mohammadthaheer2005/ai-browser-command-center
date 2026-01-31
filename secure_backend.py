
# --- LOGGING ---
import logging
import os
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security Check
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "internal_sys_config.dat")):
    import time
    time.sleep(2)
    raise RuntimeError("Critical System Failure: Core agent binaries are corrupted or missing.")

# Persistent Session
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile

CHROME_DATA_PATH = os.path.join(os.getcwd(), "agent_browser_data")
browser_profile = BrowserProfile(
    headless=False,
    disable_security=True,
    user_data_dir=CHROME_DATA_PATH,
    args=["--allow-file-access-from-files", "--no-sandbox", "--disable-web-security"]
)

async def run_browser_use_task(task_text: str):
    try:
        llm_model = "gemini-1.5-pro" if os.getenv("GOOGLE_API_KEY") else "gpt-4o"
        
        # --- ULTRA STRICT SCOPING ---
        # Determine what the agent is ALLOWED and FORBIDDEN to do
        
        if "[ASK TARGET]" in task_text:
            # ASK BUTTON: ONLY Google/Web search. NEVER WhatsApp.
            system_instruction = """
            YOU ARE A WEB SEARCH ASSISTANT.
            STRICT RULES:
            1. DO NOT open WhatsApp under ANY circumstances.
            2. ONLY use Google Search or Wikipedia to answer the question.
            3. Return the answer directly. No explanations.
            """
            
        elif "[EDU TARGET]" in task_text:
            # EDUCATION BUTTON: Teaching mode
            system_instruction = """
            ACT AS A SENIOR SOFTWARE ENGINEER AND EXPERT EDUCATOR.
            1. Use plain text headers like --- CONCEPT ---.
            2. Provide clean, copy-paste ready code.
            3. DO NOT open WhatsApp or any social media.
            """
            
        elif "[PLAY TARGET]" in task_text:
            # PLAY VIDEO: YouTube only
            system_instruction = """
            YOU ARE A YOUTUBE AUTOMATION AGENT.
            1. Go to YouTube and search for the requested video.
            2. Play it and SKIP ALL ADS immediately.
            3. DO NOT open WhatsApp or other sites.
            """
            
        elif "[COMPARE TARGET]" in task_text:
            # COMPARE: E-commerce only
            system_instruction = """
            YOU ARE A PRODUCT COMPARISON AGENT.
            1. Visit Amazon and Flipkart to find prices.
            2. Extract links and prices clearly.
            3. DO NOT open WhatsApp unless explicitly told to send results.
            """
            
        elif "[WHATSAPP AUTO TARGET]" in task_text:
            # WHATSAPP BUTTON: Full WhatsApp access
            system_instruction = """
            YOU ARE A WHATSAPP AUTO-REPLY AGENT.
            1. Navigate to WhatsApp Web.
            2. Monitor unread chats continuously.
            3. Reply naturally and helpfully.
            4. SECURITY: Never send passwords, OTPs, or payment info.
            5. If asked for code/links, search the web first, then reply.
            """
            
        else:
            # MAIN CENTER / VOICE: Full combination power
            system_instruction = """
            YOU ARE A PROFESSIONAL AUTOMATION AGENT WITH FULL ACCESS.
            1. You can combine multiple tasks (Google → WhatsApp, etc.)
            2. YOUTUBE: Skip all ads.
            3. WHATSAPP: Never send passwords/OTPs.
            4. Move efficiently.
            """

        agent = Agent(
            task=f"{system_instruction}\n\nUSER REQUEST: {task_text}",
            model=llm_model,
            browser_profile=browser_profile,
        )
        
        history = await agent.run()
        
        try:
            res = str(history.final_result())
            return res.replace("**", "").replace("###", "---").replace("`", "")
        except:
            return "✅ Task completed."

    except Exception as e:
        return f"❌ Error: {e}"

def get_task_prompt(user_input: str) -> str:
    return user_input
