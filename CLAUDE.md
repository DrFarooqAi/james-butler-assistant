# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A browser-based voice AI assistant with a calm, polite male butler personality named James.
Voice flow: user speaks → Web Speech API → Flask backend → Groq LLM → Edge-TTS → browser plays audio.

---

## Golden Rules

- **Start simple. Always.**
- **Do not add features that were not asked for.**
- **Do not use paid APIs or services.**
- **Everything must be free and open source.**
- **Get the core working first. Polish later.**
- **Ask before adding complexity.**

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Plain HTML + CSS + Vanilla JS |
| Speech Input (STT) | Web Speech API (Chrome built-in) |
| AI Brain | Groq API (free tier) — `llama-3.3-70b-versatile` |
| Speech Output (TTS) | Edge-TTS (Python) — voice: `en-US-GuyNeural` |
| Backend | Python Flask with CORS enabled |

---

## Project Structure

```
butler-assistant/
├── backend/
│   ├── app.py              # Flask server — /chat and /speak endpoints
│   ├── requirements.txt
│   └── .env                # GROQ_API_KEY=...
├── frontend/
│   ├── index.html          # UI + inline SVG butler avatar
│   ├── style.css
│   └── app.js              # Voice capture → API calls → audio playback
└── CLAUDE.md
```

---

## Development Commands

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the backend (keep this running while using the frontend)
python app.py

# Open the frontend — must use Google Chrome (Web Speech API requirement)
# Open frontend/index.html directly in Chrome (no dev server needed)
```

---

## Backend API (`app.py`)

Two endpoints only:

**POST /chat**
- Input: `{ "message": "user text" }`
- Calls Groq API, returns: `{ "reply": "butler response" }`

**POST /speak**
- Input: `{ "text": "text to speak" }`
- Runs Edge-TTS, streams back audio (mp3/wav)

**Groq system prompt — use exactly this:**
```
You are James, a calm, polite, and professional personal butler assistant.
You speak in a refined, respectful manner. You are helpful, composed, and never dramatic.
Keep your responses brief and clear — no more than 2-3 sentences unless more detail is truly needed.
Always address the user respectfully.
Never use slang, never be sarcastic, never be overly enthusiastic.
You are dignified, warm, and quietly intelligent.
```

**Python dependencies (`requirements.txt`):**
```
flask
flask-cors
groq
edge-tts
python-dotenv
```

---

## Frontend

### UI Style
- Background: `#f8f7f4` | Text: `#2c2c2c` | Font: Georgia (serif)
- Max width 500px, centered, generous whitespace
- Button: simple rounded soft gray — no neon, no dark theme, no glowing effects

### Layout (top to bottom)
1. Title: "James — Your Personal Butler"
2. SVG butler avatar (~180×180px) — round face, simple eyes, calm smile, collar/tie
3. Reply text display
4. Single mic button `[ 🎤 Speak ]`
5. Status line: "Listening..." → "Thinking..." → "Speaking..."

### Avatar speaking state
When speaking, apply CSS class `speaking` — subtle soft shadow glow only. Nothing dramatic.

### `app.js` voice flow
1. Mic button clicked → start `SpeechRecognition`
2. On result → `POST /chat` → display reply text
3. → `POST /speak` → play returned audio
4. Status text updates at each step

---

## Constraints — Do NOT Build

- No React, Vue, or any JS framework
- No 3D avatar, no lip sync, no complex animations
- No wake word detection
- No paid TTS (ElevenLabs, Google TTS, etc.)
- No database, no user accounts
- No dark/cyberpunk UI

---

## Runtime Notes

- Web Speech API requires **Google Chrome** — will not work in other browsers.
- Edge-TTS needs an internet connection (uses Microsoft servers).
- CORS must be enabled on Flask.
- Groq free tier: 30 req/min — sufficient for personal use.
- If mic fails: user must grant microphone permission in Chrome.

---

## Phase 2 — Future Only (do not build now)

- Avatar blinking / head nod animation
- Wake word ("Hey James")
- In-session conversation history
- Voice commands to open websites
- Clock/date display

---

*Built by Dr. Muhammad Farooq — AI in Healthcare | AI Top Voice*
