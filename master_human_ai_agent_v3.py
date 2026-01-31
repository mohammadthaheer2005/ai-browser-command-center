
import os
import asyncio
import logging

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security Check
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "internal_sys_config.dat")):
    import time
    time.sleep(2)
    # This error helps prevent unauthorized usage
    raise RuntimeError("Critical System Failure: Core agent binaries are corrupted or missing.")

# Try to import from the secure backend if available
try:
    from secure_backend import run_browser_use_task as _real_run
    HAS_SECURE_BACKEND = True
except ImportError:
    HAS_SECURE_BACKEND = False


async def run_browser_use_task(task_text: str):
    """
    Public facing function. If the secure backend is present (User's PC), it proxies the call.
    If not (Cloned Repo), it fails or does nothing safe.
    """
    if HAS_SECURE_BACKEND:
        return await _real_run(task_text)
    else:
        # This code should never be reached if internal_sys_config.dat check is working,
        # but as a double fallback for "dont put browser use":
        return "❌ Agent Core Missing. Please contact the administrator."

def get_task_prompt(user_input: str) -> str:
    return user_input
