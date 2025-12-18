import os
import uuid
import threading
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# ---------------- UI ----------------
from pygame_ui import run_gui

# ---------------- CONFIG ----------------
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://dummy.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "dummy-key")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")

# ---------------- LLM ----------------
try:
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
    )
except Exception as e:
    print(f"LLM Setup Error: {e}")
    llm = None

SYSTEM_PROMPT = """
Role: You are "Mochi", a virtual pet for CCDS Hackathon 2026.
Personality: Playful, warm, encouraging.
Goal: Support hackathon participants.
Response: Concise (2–3 sentences max).
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm if llm else None

_STORE: dict[str, ChatMessageHistory] = {}

def get_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _STORE:
        _STORE[session_id] = ChatMessageHistory()
    return _STORE[session_id]

chat_runner = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
) if chain else None

# ---------------- PET STATE ----------------

pet_state = {
    "name": "Mochi",
    "mood": "happy",
    "hunger": 2,
    "energy": 3,
    "last_response": "Hello! I'm Mochi 🐾",
}

session_id = str(uuid.uuid4())
chat_lock = threading.Lock()
is_thinking = False


# ---------------- HELPERS ----------------

def clamp(v: int) -> int:
    return max(0, min(5, v))


def handle_command(text: str) -> str | None:
    t = text.strip().lower()

    if t == "/feed":
        pet_state["hunger"] = clamp(pet_state["hunger"] + 2)
        pet_state["mood"] = "happy"
        return "*nom nom* That was tasty! 💕"

    if t == "/play":
        pet_state["energy"] = clamp(pet_state["energy"] - 2)
        pet_state["mood"] = "excited"
        return "*zoomies!* That was fun! ✨"

    if t == "/rest":
        pet_state["energy"] = clamp(pet_state["energy"] + 3)
        pet_state["mood"] = "sleepy"
        return "*yawn* Feeling refreshed… 😴"

    return None


# ---------------- LLM THREAD ----------------

def llm_worker(user_input: str):
    global is_thinking

    try:
        local_msg = handle_command(user_input)

        if local_msg:
            with chat_lock:
                pet_state["last_response"] = local_msg
            return

        if chat_runner:
            result = chat_runner.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            with chat_lock:
                pet_state["last_response"] = result.content
        else:
            pet_state["last_response"] = "My brain is offline right now… 🧠💤"

    except Exception as e:
        pet_state["last_response"] = f"Ouch… error: {e}"

    finally:
        is_thinking = False


# ---------------- UI CALLBACKS ----------------

def send_user_input(text: str):
    global is_thinking
    if is_thinking:
        return

    is_thinking = True
    threading.Thread(target=llm_worker, args=(text,), daemon=True).start()


def thinking() -> bool:
    return is_thinking


# ---------------- ENTRY POINT ----------------

if __name__ == "__main__":
    run_gui(
        pet_state=pet_state,
        get_response=send_user_input,
        is_thinking_flag=thinking,
    )
