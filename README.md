# 🎓 AI Study Buddy

A premium, state-of-the-art AI-powered study companion that helps you research topics, summarize articles, generate challenge questions, and create custom study plans. 

Built with an elegant Glassmorphism UI and powered by Google's latest Gemini AI models, this tool turns your browser into a full-fledged intelligent tutor.

![AI Study Buddy Banner](https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge) ![Gemini Integration](https://img.shields.io/badge/AI-Google_Gemini_2.5-blue?style=for-the-badge&logo=google) ![Flask Backend](https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge&logo=flask)

---

## ✨ Features

- 🧬 **Topic Researcher**: Deep-dive into any educational subject with structured, well-formatted markdown articles.
- 🌐 **Web-Search QA**: Get real-time, AI-synthesized answers to complex questions.
- 📇 **Interactive Flashcards**: Test your knowledge using beautiful, animated 3D flip-cards.
- 💡 **Smart Summarizer 2.0**: Instantly summarize giant blocks of text or directly summarize content from web URLs.
- 📅 **Study Planner**: Automatically generate organized, structured Markdown study schedules with clear milestones.
- ❓ **Question Generator**: Challenge yourself with high-quality AI-generated questions based on your study text.
- 🎓 **AI Tutor (Q&A)**: Extract direct answers from specific paragraphs seamlessly.
- 🎨 **Premium UI/UX**: Built with a sleek dark-mode Glassmorphism design system, smooth micro-animations, and responsive layouts.
- 📄 **Robust Markdown Rendering**: Fully custom client-side Markdown rendering engine that beautifully structures lists, paragraphs, quotes, and code blocks.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tejaswalikar007/ai-study-Buddy-TejasSW.git
   cd ai-study-Buddy-TejasSW
   ```

2. **Create and activate a virtual environment (Recommended)**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key (Security Best Practice)**:
   Create a file named `.env` in the root of the project.
   Add your Google Gemini API key to it:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```
   > ⚠️ **IMPORTANT**: Never hardcode your API key into `config.py` or commit the `.env` file to GitHub to prevent leaks!

---

## 🚀 Running the App

Start the Flask server:
```bash
python app.py
```

Open your browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚙️ How it Works under the Hood

- **Dynamic Model Resolution**: The application dynamically probes for the latest supported Gemini models (e.g., `gemini-2.5-flash`, `gemini-2.0-flash`) ensuring your application never crashes from deprecated endpoints.
- **Robust Client-Side Markdown**: AI outputs are securely funneled through hidden `<textarea>` decoders to preserve structural white space, which is then compiled into gorgeous structured HTML in real-time.
- **Local Fallbacks**: Hugging Face transformer models provide localized fallback capabilities if the cloud API goes down.

---

## 📦 Publishing Updates to GitHub

This repository includes a completely automated deployment script to make pushing your code to GitHub foolproof and secure.

Simply run:
```bash
python push_to_github.py
```
This script will automatically format the `.gitignore`, strip tracked `.env` variables to protect your API keys, commit the changes, and force push the updates directly to the `main` branch.

---
*Created and maintained by Tejas Walikar.*