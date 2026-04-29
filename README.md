# James — Your Personal Butler Assistant

A browser-based voice AI assistant with a calm, polite butler personality. Speak to James, he thinks, he speaks back.

![James Butler Assistant](https://img.shields.io/badge/AI-Butler-8b7355?style=flat-square) ![Python](https://img.shields.io/badge/Python-Flask-3a7abd?style=flat-square) ![Free](https://img.shields.io/badge/Cost-Free-4caf50?style=flat-square)

---

## What James Can Do

- **Voice conversation** — speak naturally, James replies in a refined butler voice
- **Take notes by voice** — "Take a note: meeting at 3pm" → saved directly to your Obsidian vault
- **Search your notes** — "What do I have in my notes about the project?" → James reads your vault and answers
- **Conversation memory** — remembers everything said during the session

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Plain HTML + CSS + Vanilla JS |
| Speech Input | Web Speech API (Chrome built-in) |
| AI Brain | Groq API — `llama-3.3-70b-versatile` |
| Voice Output | Edge-TTS — `en-US-GuyNeural` |
| Backend | Python + Flask |

Everything is **free and open source**. No paid APIs.

---

## Setup

### 1. Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) — no credit card required.

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add your API key
Edit `backend/.env`:
```
GROQ_API_KEY=your_key_here
```

### 4. Set your Obsidian vault path
Edit `backend/app.py` and update this line to your vault location:
```python
OBSIDIAN_VAULT = r"C:\Users\YourName\Documents"
```

### 5. Run
```bash
python app.py
```

Then open **Google Chrome** and go to `http://127.0.0.1:5000`

> **Chrome is required** — Web Speech API does not work in other browsers.

---

## Usage

| Voice Command | What Happens |
|---|---|
| *Any question* | James answers conversationally |
| "Take a note: ..." | Saves to today's daily note in Obsidian |
| "What do I have in my notes about X?" | Searches vault and summarises |
| Click **Clear Memory** | Resets conversation history |

Notes are saved to a `James Notes/` folder inside your Obsidian vault as daily markdown files (`YYYY-MM-DD.md`).

---

## Quick Launch (Windows)

Double-click **`Start James.bat`** — opens Chrome and starts the server automatically.

---

## Project Structure

```
├── backend/
│   ├── app.py              # Flask server — AI, TTS, Obsidian integration
│   ├── requirements.txt
│   └── .env                # Your Groq API key (not committed)
├── frontend/
│   ├── index.html          # UI + SVG butler avatar
│   ├── style.css
│   └── app.js              # Voice capture → API → audio playback
└── Start James.bat         # One-click launcher
```

---

*Built by [Dr. Muhammad Farooq](https://github.com/DrFarooqAi) — AI in Healthcare | AI Top Voice*
