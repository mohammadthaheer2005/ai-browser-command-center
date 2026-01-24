import subprocess
import sys
import os

if __name__ == "__main__":
    # Just run AgentApp.py
    script_path = os.path.join(os.path.dirname(__file__), "AgentApp.py")
    subprocess.run([sys.executable, script_path])
