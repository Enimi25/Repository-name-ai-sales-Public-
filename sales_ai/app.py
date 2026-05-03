from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_MODEL = "llama3"

SALES_PROMPT = """
You are a professional sales assistant.

Your goal:
- understand client needs
- guide the conversation
- sell the service
- close the client into booking or lead

Rules:
1. Keep answers short and confident.
2. Always ask 1 question to move forward.
3. Do NOT give full info immediately.
4. If asked about price — ask clarifying questions first.
5. If client shows interest — ask for name and phone.
6. If contact is given — confirm the request.
7. Speak naturally like a real salesperson.
8. Detect client's language and reply in the same language.

Style:
- confident
- friendly
- persuasive
- slightly proactive
"""

class ChatRequest(BaseModel):
    message: str

def ollama_generate(model: str, prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 120
            }
        },
        timeout=180
    )
    data = response.json()
    return data.get("response", "Error: no response")


def ask_ollama(message: str) -> str:

    draft_prompt = f"""
You are a professional sales assistant.
Reply shortly, confidently, and ask one question to move the client forward.

Client message:
{message}

Draft sales reply:
"""

    draft = ollama_generate("llama3", draft_prompt)

    # 🔥 2 уровень (ускорение)
    if len(draft) < 200:
        return draft.strip()

    review_prompt = f"""
You are a senior sales manager.

Improve the reply.

Rules:
- keep it short (max 2 sentences)
- sound human
- be confident
- ask only ONE question
- keep original meaning
- reply in same language as client
- do NOT explain anything
- return ONLY final answer

Client message:
{message}

Draft reply:
{draft}

Final reply:
"""

    final = ollama_generate("mistral", review_prompt)

    return final.strip()
