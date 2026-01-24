import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys
import asyncio
import queue
import logging
import speech_recognition as sr

# Import the existing agent logic
try:
    from master_human_ai_agent_v3 import run_browser_use_task
    print("DEBUG: Imported backend agent.")
except ImportError as e:
    run_browser_use_task = None
    print(f"WARNING: Backend agent not found. Error: {e}")

import os

logging.basicConfig(level=logging.INFO)

class AgentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Agent - Ultimate Command Center")
        self.geometry("1100x750")
        self.configure(bg="#121212")

        # --- COLORS & FONTS ---
        self.colors = {
            "bg": "#121212",
            "sidebar": "#1E1E1E",
            "card": "#2D2D2D",
            "accent_blue": "#3B8ED0",
            "accent_purple": "#BB86FC",
            "accent_green": "#03DAC6",
            "danger": "#CF6679",
            "text": "#FFFFFF",
            "text_dim": "#AAAAAA"
        }
        self.fonts = {
            "header": ("Segoe UI", 16, "bold"),
            "sub": ("Segoe UI", 11),
            "input": ("Segoe UI", 12),
            "log": ("Consolas", 10)
        }

        # --- LAYOUT CONFIG ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR (Quick Actions with Inputs) =================
        self.sidebar = tk.Frame(self, width=300, bg=self.colors["sidebar"], padx=15, pady=15)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo / Header
        tk.Label(self.sidebar, text="🤖 Quick Actions", bg=self.colors["sidebar"], fg=self.colors["accent_green"], 
                 font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        # --- ACTIONS (Clean Dark Style) ---
        
        # 1. PLAY VIDEO
        self.create_sidebar_btn("▶  Play Video", self.action_play_video)

        # 2. COMPARE
        self.create_sidebar_btn("🛒  Compare Products", self.action_compare_products)

        # 3. WHATSAPP
        self.create_sidebar_btn("💬  WhatsApp Auto", self.action_whatsapp_reply)

        # 4. ASK
        self.create_sidebar_btn("❓  Ask Question", self.action_quick_ask)

        # CONTROLS (At the bottom)
        
        btn_exit = tk.Button(self.sidebar, text="Exit", bg="#212121", fg="#888", 
                             font=("Segoe UI", 10), relief="flat", cursor="hand2", command=self.close_app)
        btn_exit.pack(side="bottom", fill="x", pady=10)

        self.btn_stop = tk.Button(self.sidebar, text="⛔ STOP AGENT", bg=self.colors["danger"], fg="black", 
                                  font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2", command=self.stop_agent)
        self.btn_stop.pack(side="bottom", fill="x", pady=5)


        # ================= MAIN AREA (Deep Task) =================
        self.main_area = tk.Frame(self, bg=self.colors["bg"], padx=30, pady=30)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(3, weight=1) # Log expands
        self.main_area.grid_columnconfigure(0, weight=1)

        # Header
        tk.Label(self.main_area, text="🧠 Main Task Center", bg=self.colors["bg"], fg="white", font=self.fonts["header"]).grid(row=0, column=0, sticky="w")
        tk.Label(self.main_area, text="Use this for complex tasks (e.g. 'Add Nike shoes to cart')", bg=self.colors["bg"], fg=self.colors["text_dim"], font=self.fonts["sub"]).grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Main Input Row
        input_container = tk.Frame(self.main_area, bg=self.colors["bg"])
        input_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        input_container.grid_columnconfigure(0, weight=1)

        self.input_main = tk.Entry(input_container, bg=self.colors["card"], fg="white", font=("Segoe UI", 14), relief="flat", insertbackground="white")
        self.input_main.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 10))

        # Voice Button
        self.btn_voice = tk.Button(input_container, text="🎙", bg="#333333", fg="white", font=("Segoe UI", 16), 
                                   width=4, relief="flat", cursor="hand2", command=self.start_voice_listening)
        self.btn_voice.grid(row=0, column=1, padx=(0, 10))

        # Execute Button
        self.btn_main_run = tk.Button(input_container, text="EXECUTE TASK", bg=self.colors["accent_green"], fg="black", 
                                      font=("Segoe UI", 11, "bold"), padx=20, relief="flat", cursor="hand2", command=self.run_main_task)
        self.btn_main_run.grid(row=0, column=2)

        # Logs Header & Clear Button
        log_header_frame = tk.Frame(self.main_area, bg=self.colors["bg"])
        log_header_frame.grid(row=3, column=0, sticky="ew", pady=(25, 5))
        
        tk.Label(log_header_frame, text="Live Agent Feed", bg=self.colors["bg"], fg=self.colors["text_dim"], 
                 font=("Segoe UI", 12)).pack(side="left")
        
        tk.Button(log_header_frame, text="Clear Logs", bg="#333333", fg="white", font=("Segoe UI", 9), 
                  relief="flat", cursor="hand2", command=self.clear_logs).pack(side="right")

        self.console = scrolledtext.ScrolledText(self.main_area, bg="#0F0F0F", fg="#E0E0E0", font=("Consolas", 11), 
                                                 relief="flat", padx=15, pady=15, selectbackground="#3B8ED0")
        self.console.grid(row=4, column=0, sticky="nsew")

        # --- LOGIC INIT ---
        self.stdout_queue = queue.Queue()
        sys.stdout = OutputRedirector(self.stdout_queue)
        
        # Helper storage for dynamic entry inputs
        self.quick_inputs = {} 

        # Internal state
        self.current_loop = None
        self.update_console()
        
        # Check for API Key on startup
        self.after(500, self.ensure_api_key)

    # ================= UI HELPERS =================
    def create_sidebar_btn(self, text, cmd, bg_color=None, fg_color="white"):
        if not bg_color: bg_color = "#333333"
        btn = tk.Button(self.sidebar, text=text, bg=bg_color, fg=fg_color, 
                        font=("Segoe UI", 11), relief="flat", cursor="hand2", anchor="w", padx=20, command=cmd)
        btn.pack(pady=2, fill="x", ipady=8) # TIGHT SPACING (pady=2)
        return btn

    def show_input_dialog(self, title, prompt, is_password=False):
        """Shows a custom dark input dialog and returns the string"""
        d = DarkDialog(self, title, prompt, is_password)
        return d.result

    def ensure_api_key(self):
        """Checks if API key exists, if not, prompts user. Persists to .env_agent"""
        env_file = ".env_agent"
        
        # 1. Check current environment variables
        if os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY"):
            return

        # 2. Check local persistent file
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                key = f.read().strip()
                if key:
                    os.environ["GOOGLE_API_KEY"] = key
                    self.log_to_console("✅ API Key loaded from disk.")
                    return

        # 3. Prompt user if still missing
        key = self.show_input_dialog("API Key Required", "Please enter your Google Gemini API Key:", is_password=True)
        if key:
            os.environ["GOOGLE_API_KEY"] = key
            try:
                with open(env_file, "w") as f:
                    f.write(key)
                self.log_to_console("✅ API Key saved for future sessions.")
            except:
                self.log_to_console("✅ API Key set for this session (could not save to disk).")
        else:
            self.log_to_console("⚠ WARNING: No API Key provided. Agent will fail to start.")

    # ================= LOGIC & ACTIONS =================

    def action_play_video(self):
        query = self.show_input_dialog("Play Video", "Enter song or video name:")
        if query: 
            # optimized prompt for speed and accuracy
            self.run_task_engine(f"Go to youtube.com, search for '{query} official', and click the first video result immediately.")

    def action_compare_products(self):
        query = self.show_input_dialog("Compare Products", "Enter product names (e.g., iPhone 15 vs S24):")
        if query: 
            self.run_task_engine(f"Search google for '{query} comparison price specs'. Summarize the key differences and best price found.")

    def action_quick_ask(self):
        query = self.show_input_dialog("Ask Question", "Enter your question:")
        if query: 
            # Force fast google snippet answer
            self.run_task_engine(f"Go to google.com, search for '{query}', and return the precise answer found in the featured snippet or top result.")

    def action_whatsapp_reply(self):
        # Sophisticated Prompt for WhatsApp
        task_prompt = (
            "Navigate to https://web.whatsapp.com. "
            "1. Look for unread chats (green badges). "
            "2. For each unread message: Read the last few messages to understand context. "
            "3. GENERATE A REPLY YOURSELF based on the context. Be helpful and polite. "
            "4. SECURITY: If asked for money/passwords, reply 'I cannot share that'. "
            "5. Send the reply."
        )
        self.run_task_engine(task_prompt)

    def run_main_task(self):
        text = self.input_main.get().strip()
        if text: self.run_task_engine(text)
        else: self.log_to_console("⚠ Please type a task.")

    def start_voice_listening(self):
        self.btn_voice.config(bg="orange")
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        r = sr.Recognizer()
        r.pause_threshold = 0.8
        self.log_to_console("🎙 Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            
            self.log_to_console("⏳ Thinking...")
            text = r.recognize_google(audio)
            self.log_to_console(f"🗣 You said: '{text}'")
            
            self.input_main.delete(0, "end")
            self.input_main.insert(0, text)
            self.after(0, lambda: self.run_task_engine(text))

        except Exception as e:
            self.log_to_console(f"❌ Voice Error: {e}")
        finally:
            self.btn_voice.config(bg="#333333")

    # ================= CORE ENGINE =================
    def run_task_engine(self, task_prompt):
        self.log_to_console(f"\n🚀 Starting task: {task_prompt}...\n")
        self.btn_main_run.config(state="disabled", text="Running...")
        self.btn_stop.config(state="normal") 
        threading.Thread(target=self._backend_thread, args=(task_prompt,), daemon=True).start()

    def _backend_thread(self, task):
        try:
            if run_browser_use_task:
                self.current_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.current_loop)
                self.main_task = self.current_loop.create_task(run_browser_use_task(task))
                result = self.current_loop.run_until_complete(self.main_task)
                
                self.log_to_console("\n✨ --- AGENT RESULT --- ✨")
                self.log_to_console(str(result).strip())
                self.log_to_console("--------------------------\n")
            else:
                self.log_to_console("❌ Engine missing.")
        except asyncio.CancelledError:
            self.log_to_console("⛔ STOPPED by User.")
        except Exception as e:
            self.log_to_console(f"❌ Error: {e}")
        finally:
            if self.current_loop: 
                try: self.current_loop.close()
                except: pass
            self.current_loop = None
            self.after(0, self._reset_ui)

    def _reset_ui(self):
        self.btn_main_run.config(state="normal", text="EXECUTE TASK")

    def stop_agent(self):
        self.log_to_console("⚠ STOPPING...")
        if self.current_loop:
            self.current_loop.call_soon_threadsafe(self.main_task.cancel)
        else:
            self._reset_ui()

    def clear_logs(self):
        self.console.delete("1.0", "end")

    def log_to_console(self, msg):
        print(msg) 
        self.after(0, lambda: self._ui_log(msg))

    def _ui_log(self, msg):
        self.console.insert("end", str(msg) + "\n")
        self.console.see("end")

    def close_app(self):
        self.destroy()
        sys.exit()

    def update_console(self):
        while not self.stdout_queue.empty():
            try:
                msg = self.stdout_queue.get_nowait()
                if msg:
                    self._ui_log(msg)
            except: pass
        self.after(100, self.update_console)

class OutputRedirector(object):
    def __init__(self, queue): self.queue = queue
    def write(self, string):
        if string:
            self.queue.put(string)
    def flush(self): pass

class DarkDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, is_password=False):
        super().__init__(parent)
        self.result = None
        self.title(title)
        self.geometry("400x180")
        self.configure(bg="#2D2D2D")
        self.resizable(False, False)
        
        # Center relative to parent
        self.transient(parent)
        self.grab_set()
        
        tk.Label(self, text=prompt, bg="#2D2D2D", fg="white", font=("Segoe UI", 11)).pack(pady=(20, 10))
        
        show_char = "*" if is_password else ""
        self.entry = tk.Entry(self, bg="#404040", fg="white", font=("Segoe UI", 12), insertbackground="white", show=show_char)
        self.entry.pack(pady=5, padx=20, fill="x")
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self.on_ok())
        
        btn_frame = tk.Frame(self, bg="#2D2D2D")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="OK", bg="#3B8ED0", fg="white", font=("Segoe UI", 10, "bold"), 
                  width=10, relief="flat", command=self.on_ok).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Cancel", bg="#CF6679", fg="black", font=("Segoe UI", 10, "bold"), 
                  width=10, relief="flat", command=self.destroy).pack(side="left", padx=10)
        
        self.wait_window(self)

    def on_ok(self):
        self.result = self.entry.get().strip()
        self.destroy()

if __name__ == "__main__":
    app = AgentGUI()
    app.mainloop()
