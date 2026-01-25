import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
import threading
import sys
import os
import asyncio
import queue
import logging
import speech_recognition as sr

# --- ROBUST ENGINE LOADER ---
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from master_human_ai_agent_v3 import run_browser_use_task
    print("✅ DEBUG: Backend agent loaded.")
except Exception as e:
    run_browser_use_task = None
    print(f"❌ ERROR: {e}")

logging.basicConfig(level=logging.INFO)

class DarkDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.result = None
        self.title(title)
        self.geometry("450x220")
        self.configure(bg="#212121")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
        self.geometry(f"+{x}+{y}")

        tk.Label(self, text=prompt, bg="#212121", fg="white", font=("Segoe UI", 12)).pack(pady=(30, 15))
        self.entry = tk.Entry(self, bg="#333", fg="white", font=("Segoe UI", 12), relief="flat", insertbackground="white")
        self.entry.pack(pady=5, padx=30, fill="x", ipady=8)
        self.entry.focus_set()

        btn_frame = tk.Frame(self, bg="#212121")
        btn_frame.pack(pady=25)
        tk.Button(btn_frame, text="Ok", bg="#1976D2", fg="white", font=("Segoe UI", 11, "bold"), width=15, relief="flat", command=self.on_ok).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", bg="#1976D2", fg="white", font=("Segoe UI", 11, "bold"), width=15, relief="flat", command=self.destroy).pack(side="left", padx=10)

        self.bind("<Return>", lambda e: self.on_ok())
        self.wait_window(self)

    def on_ok(self):
        self.result = self.entry.get().strip()
        self.destroy()

class AgentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Agent Pro - Ultimate Command Center")
        self.geometry("1100x750")
        self.configure(bg="#121212")

        self.colors = {
            "bg": "#121212", "sidebar": "#1E1E1E", "card": "#2D2D2D",
            "accent_blue": "#3B8ED0", "accent_purple": "#BB86FC",
            "accent_green": "#03DAC6", "danger": "#CF6679", "text": "#FFFFFF",
            "text_dim": "#AAAAAA"
        }
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(self, width=300, bg=self.colors["sidebar"], padx=15, pady=15)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        tk.Label(self.sidebar, text="🤖 Quick Actions", bg=self.colors["sidebar"], fg=self.colors["accent_green"], font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        self.btn_stop = tk.Button(self.sidebar, text="⛔ STOP AGENT", bg=self.colors["danger"], fg="black", 
                                  font=("Segoe UI", 12, "bold"), relief="flat", command=self.stop_agent)
        self.btn_stop.pack(fill="x", pady=(0, 5))

        tk.Button(self.sidebar, text="🗑  Clear Logs & Memory", bg="#616161", fg="white", 
                  font=("Segoe UI", 11), relief="flat", command=self.clear_logs).pack(fill="x", pady=(0, 5))

        tk.Button(self.sidebar, text="🚪 Exit Application", bg="#424242", fg="white", 
                  font=("Segoe UI", 11), relief="flat", command=self.close_app).pack(fill="x", pady=(0, 20))

        self.create_sidebar_btn("▶  Play Video", self.action_play_video)
        self.create_sidebar_btn("🛒  Compare Products", self.action_compare_products)
        self.create_sidebar_btn("💬  WhatsApp Auto", self.action_whatsapp_reply)
        self.create_sidebar_btn("🎓  Education Mode", self.action_education_task, bg_color="#4A148C")
        self.create_sidebar_btn("❓  Ask Question", self.action_quick_ask)

        # Main Area
        self.main_area = tk.Frame(self, bg=self.colors["bg"], padx=30, pady=30)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(3, weight=1) 
        self.main_area.grid_columnconfigure(0, weight=1)

        tk.Label(self.main_area, text="🧠 Main Task Center", bg=self.colors["bg"], fg="white", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")
        
        input_container = tk.Frame(self.main_area, bg=self.colors["bg"])
        input_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        input_container.grid_columnconfigure(0, weight=1)

        self.input_main = tk.Entry(input_container, bg=self.colors["card"], fg="white", font=("Segoe UI", 14), relief="flat", insertbackground="white")
        self.input_main.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 10))

        self.btn_voice = tk.Button(input_container, text="🎙", bg="#333", fg="white", font=("Segoe UI", 16), width=4, command=self.start_voice_listening)
        self.btn_voice.grid(row=0, column=1, padx=(0, 10))

        self.btn_main_run = tk.Button(input_container, text="EXECUTE TASK", bg=self.colors["accent_green"], font=("Segoe UI", 11, "bold"), padx=20, command=self.run_main_task)
        self.btn_main_run.grid(row=0, column=2)

        self.console = scrolledtext.ScrolledText(self.main_area, bg="#0F0F0F", fg="#E0E0E0", font=("Consolas", 11), padx=15, pady=15)
        self.console.grid(row=3, column=0, sticky="nsew")

        self.stdout_queue = queue.Queue()
        sys.stdout = OutputRedirector(self.stdout_queue)
        self.current_loop = None
        self.conversation_history = []
        self.is_running_continuous = False
        self.update_console()
        self.after(500, self.ensure_api_key)

    def create_sidebar_btn(self, text, cmd, bg_color="#333"):
        btn = tk.Button(self.sidebar, text=text, bg=bg_color, fg="white", font=("Segoe UI", 11), anchor="w", padx=20, command=cmd)
        btn.pack(pady=2, fill="x", ipady=8)

    def show_custom_input(self, title, prompt):
        d = DarkDialog(self, title, prompt)
        return d.result

    def ensure_api_key(self):
        if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            key = self.show_custom_input("API Key", "Enter Your Gemeni API Key:")
            if key: os.environ["GOOGLE_API_KEY"] = key

    def run_main_task(self):
        t = self.input_main.get().strip()
        if t: self.run_task_engine(f"[MAIN_CENTER TARGET] {t}")

    def action_play_video(self):
        self.log_to_console("▶️ Opening YouTube player...")
        q = self.show_custom_input("Play Video", "Enter song or video name:")
        if q: 
            self.log_to_console(f"🎵 Searching for: {q}")
            self.run_task_engine(f"[PLAY TARGET] {q}")

    def action_compare_products(self):
        self.log_to_console("🛒 Opening product comparison...")
        q = self.show_custom_input("Compare", "Enter products:")
        if q: 
            self.log_to_console(f"🔍 Comparing: {q}")
            self.run_task_engine(f"[COMPARE TARGET] {q}")

    def action_education_task(self):
        self.log_to_console("🎓 Opening Education Mode...")
        q = self.show_custom_input("Education Mode", "Enter problem:")
        if q: 
            self.log_to_console(f"📚 Solving: {q}")
            self.run_task_engine(f"[EDU TARGET] {q}")

    def action_whatsapp_reply(self):
        self.log_to_console("💬 Starting WhatsApp Auto-Reply Mode...")
        self.log_to_console("⚡ Continuous monitoring activated. Click STOP AGENT to end.")
        self.is_running_continuous = True
        self.run_task_engine("[WHATSAPP AUTO TARGET] Start continuous monitoring.")

    def action_quick_ask(self):
        self.log_to_console("❓ Opening Quick Ask...")
        q = self.show_custom_input("Ask", "Enter your question:")
        if q: 
            self.log_to_console(f"🔎 Searching for: {q}")
            self.run_task_engine(f"[ASK TARGET] {q}")

    def run_task_engine(self, task_prompt):
        context = ""
        if self.conversation_history:
            context = "--- PAST MEMORY ---"
            for entry in self.conversation_history[-2:]:
                context += f"\nResult: {entry['result'][:1000]}"
            context += "\n--------------------\n"
        
        full_p = context + task_prompt
        self.log_to_console(f"\n🚀 Launching: {task_prompt}")
        self.btn_main_run.config(state="disabled", text="Running...")
        threading.Thread(target=self._backend_thread, args=(full_p, task_prompt), daemon=True).start()

    def _backend_thread(self, full_p, orig_t):
        try:
            if run_browser_use_task:
                self.current_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.current_loop)
                while True:
                    self.main_task = self.current_loop.create_task(run_browser_use_task(full_p))
                    res = self.current_loop.run_until_complete(self.main_task)
                    self.log_to_console(f"\n✨ Result:\n{res}\n")
                    self.conversation_history.append({"task": orig_t, "result": str(res)})
                    if not self.is_running_continuous: break
            else:
                self.log_to_console("❌ Engine missing.")
        except Exception as e:
            self.log_to_console(f"❌ Error: {e}")
        finally:
            self.is_running_continuous = False
            self.after(0, lambda: self.btn_main_run.config(state="normal", text="EXECUTE TASK"))

    def stop_agent(self):
        self.log_to_console("\n⏸️ STOPPING AGENT...")
        self.log_to_console("⛔ All continuous tasks will be terminated.\n")
        self.is_running_continuous = False
        if self.current_loop: self.current_loop.call_soon_threadsafe(self.main_task.cancel)

    def close_app(self):
        # This deletes your session data (WhatsApp login) when you close the software
        import shutil
        try:
            if os.path.exists("agent_browser_data"):
                shutil.rmtree("agent_browser_data")
                print("🔒 Session data cleared. Logged out successfully.")
        except Exception as e:
            print(f"⚠️ Could not clear session data: {e}")
            
        self.destroy()
        sys.exit()

    def clear_logs(self):
        self.console.delete("1.0", "end")
        self.conversation_history = []
        self.log_to_console("🗑 Logs and Memory cleared.")

    def start_voice_listening(self):
        threading.Thread(target=self._voice_thread, daemon=True).start()

    def _voice_thread(self):
        r = sr.Recognizer()
        r.pause_threshold = 1.0
        self.log_to_console("🎙 Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio)
            self.log_to_console(f"🗣 You said: '{text}'")
            self.input_main.delete(0, "end"); self.input_main.insert(0, text)
            # VOICE IS PART OF MAIN CENTER
            self.after(0, lambda: self.run_task_engine(f"[MAIN_CENTER TARGET] {text}"))
        except Exception as e:
            self.log_to_console(f"❌ Mic Error: {e}")

    def update_console(self):
        while not self.stdout_queue.empty():
            msg = self.stdout_queue.get_nowait()
            if msg: self._ui_log(msg)
        self.after(100, self.update_console)

    def _ui_log(self, msg):
        cleaned_msg = str(msg).replace("\\n", "\n").replace("**", "").replace("`", "")
        self.console.insert("end", cleaned_msg); self.console.see("end")

    def log_to_console(self, msg): print(msg)

class OutputRedirector(object):
    def __init__(self, queue): self.queue = queue
    def write(self, s):
        if s: self.queue.put(s)
    def flush(self): pass

if __name__ == "__main__":
    app = AgentGUI()
    app.mainloop()
