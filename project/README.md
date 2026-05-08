# 🎓 StudyMind AI — Question Answering System

NLP + Flask + Claude AI se bana hua intelligent study assistant.

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: API Key Set Karo
```bash
# Windows:
set ANTHROPIC_API_KEY=your-api-key-here

# Mac/Linux:
export ANTHROPIC_API_KEY=your-api-key-here
```

> 🔑 API Key milegi: https://console.anthropic.com

### Step 3: Run Karo
```bash
python app.py
```

### Step 4: Browser Mein Kholein
```
http://localhost:5000
```

---

## 📁 Project Structure

```
study_qa/
├── app.py                  ← Flask backend (API routes)
├── requirements.txt        ← Python packages
├── README.md
├── templates/
│   └── index.html          ← Main HTML page
└── static/
    ├── css/
    │   └── style.css       ← All styling
    └── js/
        └── main.js         ← Frontend logic
```

---

## ✨ Features

- 🤖 **Claude AI** powered answers
- 📚 **10 Subjects**: Math, Physics, Chemistry, Biology, CS, History, English, Urdu, Islamiat
- 💬 **Chat History**: Multi-turn conversation memory
- 🎨 **Dark Academic UI**: Animated particles, glassmorphism
- 📱 **Responsive**: Mobile + Desktop
- ⚡ **Quick Suggestions**: Per-subject question prompts

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Main page |
| POST | `/ask` | Send question, get AI answer |
| GET | `/subjects` | List of available subjects |

### POST `/ask` Example:
```json
{
  "question": "What is Newton's second law?",
  "subject": "Physics",
  "history": []
}
```

### Response:
```json
{
  "answer": "Newton's Second Law states...",
  "subject": "Physics",
  "timestamp": "14:32",
  "tokens_used": 187
}
```
