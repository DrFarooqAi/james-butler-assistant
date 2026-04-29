import asyncio
import os
import tempfile
from datetime import datetime

import edge_tts
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from groq import Groq

load_dotenv()

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
OBSIDIAN_VAULT = r"C:\Users\ac\Documents"
DAILY_NOTES_DIR = os.path.join(OBSIDIAN_VAULT, "James Notes")

app = Flask(__name__, static_folder=None)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are James, a calm, polite, and professional personal butler assistant. "
    "You speak in a refined, respectful manner. You are helpful, composed, and never dramatic. "
    "Keep your responses brief and clear — no more than 2-3 sentences unless more detail is truly needed. "
    "Always address the user respectfully. "
    "Never use slang, never be sarcastic, never be overly enthusiastic. "
    "You are dignified, warm, and quietly intelligent."
)

conversation_history = []
MAX_HISTORY = 20  # keep last 20 exchanges (~40 messages)

NOTE_TRIGGERS = [
    "take a note", "note this", "save a note", "add a note",
    "remember this", "write this down", "make a note", "note down",
    "jot this down", "record this",
]

SEARCH_TRIGGERS = [
    "in my notes", "from my notes", "my notes", "what do i have",
    "do i have anything", "search my notes", "look in my notes",
    "check my notes", "find in my notes", "search for",
]


def is_note_command(text):
    t = text.lower()
    return any(trigger in t for trigger in NOTE_TRIGGERS)


def is_search_command(text):
    t = text.lower()
    return any(trigger in t for trigger in SEARCH_TRIGGERS)


def extract_note_content(text):
    t = text.lower()
    for trigger in sorted(NOTE_TRIGGERS, key=len, reverse=True):
        if trigger in t:
            idx = t.index(trigger) + len(trigger)
            return text[idx:].lstrip(" :,")
    return text


def save_note(content):
    os.makedirs(DAILY_NOTES_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    note_file = os.path.join(DAILY_NOTES_DIR, f"{today}.md")
    timestamp = datetime.now().strftime("%H:%M")
    write_header = not os.path.exists(note_file)
    with open(note_file, "a", encoding="utf-8") as f:
        if write_header:
            f.write(f"# {today}\n\n")
        f.write(f"- {timestamp} — {content}\n")
    return today


def search_vault(query):
    keywords = [w for w in query.lower().split() if len(w) > 3]
    if not keywords:
        return []
    results = []
    for root, dirs, files in os.walk(OBSIDIAN_VAULT):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for filename in files:
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                score = sum(content.lower().count(kw) for kw in keywords)
                if score > 0:
                    results.append((score, filename, content[:800]))
            except Exception:
                pass
    results.sort(reverse=True)
    return results[:3]


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Note-taking
    if is_note_command(message):
        content = extract_note_content(message)
        if content:
            date = save_note(content)
            reply = f"Noted, sir. I've saved that to your daily note for {date}."
        else:
            reply = "Of course. What would you like me to note down?"
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    # Build system prompt — inject vault context if searching
    system = SYSTEM_PROMPT
    if is_search_command(message):
        results = search_vault(message)
        if results:
            context = "\n\n".join(f"[From '{r[1]}']:\n{r[2]}" for r in results)
            system += (
                "\n\nThe user is asking about their Obsidian notes. "
                "Here are the most relevant excerpts from their vault:\n\n"
                + context
                + "\n\nAnswer based on these notes. Be concise."
            )
        else:
            system += "\n\nThe user asked about their notes but no matching notes were found in the vault."

    conversation_history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": system}] + conversation_history[-MAX_HISTORY:]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    reply = completion.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})


@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()

    async def synthesize():
        communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
        await communicate.save(tmp.name)

    asyncio.run(synthesize())

    return send_file(tmp.name, mimetype="audio/mpeg", as_attachment=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
