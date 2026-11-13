import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRMPT_PATH = PROJECT_ROOT / "htb-mentor-prompt.md"

client = OpenAI()

MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")
SYSTEM_PROMPT = PRMPT_PATH.read_text(encoding="utf-8")

def ask_ai(prompt, history=None):
    if history is None:
        history = []
        
    messages = history + [
        {
            "role": "user",
            "content": prompt
            }
    ]    
    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=messages
    )
    
    answer = response.output_text.strip()
    
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": answer})
    
    return answer