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

## Local Setup

### 1. Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) — no credit card required.

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Add your API key
Create `backend/.env`:
```
GROQ_API_KEY=your_key_here
```

### 4. Obsidian vault (optional)
To enable voice note-taking and vault search, add to `backend/.env`:
```
OBSIDIAN_VAULT=C:\Users\YourName\Documents
```
If omitted, James works as a voice assistant without the notes features.

### 5. Run
```bash
python backend/app.py
```

Then open **Google Chrome** and go to `http://127.0.0.1:5000`

> **Chrome is required** — Web Speech API does not work in other browsers.

---

## Quick Launch (Windows)

Double-click **`Start James.bat`** — starts the server and opens your browser automatically.

---

## Deploy to Cloud (share with others)

James can be deployed to [Render](https://render.com) for free — no credit card required.

1. Fork this repo
2. Sign up at [render.com](https://render.com) and create a new **Web Service** from your fork
3. Render auto-detects `render.yaml` — click **Deploy**
4. Add environment variable: `GROQ_API_KEY=your_key_here`
5. Share the generated URL with anyone — they just need Chrome

> Free tier spins down after 15 min of inactivity. First load after a pause takes ~30 seconds.

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
├── render.yaml             # Render cloud deployment config
└── Start James.bat         # One-click launcher (Windows)
```

---

*Built by [Dr. Muhammad Farooq](https://github.com/DrFarooqAi) — AI in Healthcare | AI Top Voice*
