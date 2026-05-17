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

## 🏗️ System Architecture

The AI Study Buddy is built on a resilient, dual-layered architecture designed to prioritize speed, reliability, and user experience:

- **Frontend Layer (Client-Side)**: 
  - A responsive web interface built with vanilla HTML, CSS, and JS.
  - Features a custom Glassmorphism UI and dynamic DOM updates for smooth interactions.
  - Implements a robust client-side Markdown rendering engine that formats AI outputs beautifully into structured paragraphs, lists, and code blocks.
- **Backend Server (Flask)**: 
  - A lightweight, fast Python Flask application handling routing, API requests, and file processing (e.g., PDF text extraction).
  - Integrates **Flask-Limiter** for rate limiting to prevent API abuse and ensure server stability.
- **AI Integration Layer (Cloud & Local)**:
  - **Primary AI (Google Gemini)**: Connects dynamically to Google's latest generative AI models (e.g., `gemini-2.5-flash`) for lightning-fast text generation, summarization, and reasoning.
  - **Local Fallback Models (Hugging Face)**: If the primary API fails, the backend seamlessly falls back to pre-trained local NLP models (T5, BART, DistilBERT) ensuring the app remains functional.

---

## 💻 Tech Stack

### Frontend
- **HTML5 & CSS3**: Vanilla CSS with a custom Dark Mode Glassmorphism design system.
- **JavaScript (ES6+)**: Vanilla JS for DOM Manipulation and asynchronous requests.
- **Markdown Rendering**: Client-side parsing to display rich text formats safely.

### Backend
- **Python 3.x**: Core backend language.
- **Flask**: Web application framework.
- **Flask-Limiter**: Rate limiting.
- **BeautifulSoup4 & Requests**: Web scraping for URL content extraction.
- **PyMuPDF (fitz)**: Efficient PDF document parsing.

### AI & Machine Learning
- **Google Generative AI SDK** (`google-generativeai`): Interacting with Gemini models.
- **Hugging Face Transformers** (`transformers`, `torch`): Running local NLP fallback models (`valhalla/t5-base-qg-hl`, `facebook/bart-large-cnn`, `distilbert-base-uncased-distilled-squad`).

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