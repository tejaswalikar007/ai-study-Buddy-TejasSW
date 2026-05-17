from flask import Flask, render_template, request, jsonify
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer, AutoModelForQuestionAnswering, AutoTokenizer
import google.generativeai as genai
import textwrap
import json
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables (force override to ensure new keys in .env are always respected)
load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print(f"🔑 API Key detected (Length: {len(GEMINI_API_KEY)})")
    print(f"🔎 Security Check: Key starts with '{GEMINI_API_KEY[:3]}...' and ends with '...{GEMINI_API_KEY[-3:]}'")
else:
    print("❌ ERROR: No API Key found in .env file!")

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ WARNING: Gemini API calls will fail due to missing API Key.")

_working_gemini_model_name = None

def get_gemini_model():
    """
    Dynamically resolve and return a working Gemini model instance.
    Probes preferred models to ensure compatibility with the installed SDK version and API key.
    """
    global _working_gemini_model_name
    
    if _working_gemini_model_name is not None:
        return genai.GenerativeModel(_working_gemini_model_name)
        
    preferred_models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-flash-latest",
        "gemini-3.1-flash-lite",
        "gemini-2.5-pro",
        "models/gemini-2.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-flash-latest",
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.5-pro",
        "gemini-1.5-flash",
        "models/gemini-1.5-flash"
    ]
    
    for model_name in preferred_models:
        try:
            print(f"🔍 Probing Gemini model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            # Perform a lightweight ping to verify generate_content is supported
            response = model.generate_content("ping", generation_config={"max_output_tokens": 5})
            if response:
                _working_gemini_model_name = model_name
                print(f"🎉 Successfully selected working Gemini model: {model_name}")
                return model
        except Exception as e:
            print(f"⚠️ Model {model_name} failed verification: {e}")
            continue
            
    # Fallback to gemini-2.5-flash if verification probe failed but we still want to try it
    print("⚠️ All Gemini model probes failed. Defaulting to 'gemini-2.5-flash'...")
    _working_gemini_model_name = "gemini-2.5-flash"
    return genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

# --- Lazy Loading for Hugging Face Models ---
_question_generator = None
_summarizer = None
_qa_pipeline = None

def get_question_generator():
    global _question_generator
    if _question_generator is None:
        print("⏳ Loading local Question Generator pipeline (this may take a moment)...")
        qg_tokenizer = T5Tokenizer.from_pretrained("valhalla/t5-base-qg-hl")
        qg_model = T5ForConditionalGeneration.from_pretrained("valhalla/t5-base-qg-hl")
        _question_generator = pipeline("text2text-generation", model=qg_model, tokenizer=qg_tokenizer)
        print("✅ Question Generator pipeline loaded successfully.")
    return _question_generator

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        print("⏳ Loading local Summarizer pipeline (this may take a moment)...")
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("✅ Summarizer pipeline loaded successfully.")
    return _summarizer

def get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        print("⏳ Loading local QA pipeline (this may take a moment)...")
        qa_model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
        qa_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
        _qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=qa_tokenizer)
        print("✅ QA pipeline loaded successfully.")
    return _qa_pipeline

# --- Routes ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debug-models")
def debug_models():
    try:
        import google.generativeai as genai
        models = []
        for m in genai.list_models():
            models.append({
                "name": m.name,
                "supported_generation_methods": m.supported_generation_methods,
                "description": m.description
            })
        return jsonify({
            "status": "success",
            "active_key": GEMINI_API_KEY[:6] + "..." + GEMINI_API_KEY[-4:] if GEMINI_API_KEY else None,
            "models": models
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "active_key": GEMINI_API_KEY[:6] + "..." + GEMINI_API_KEY[-4:] if GEMINI_API_KEY else None,
            "error_type": str(type(e)),
            "error_message": str(e)
        })



# 1. Question Generator
@app.route("/question-generator", methods=["GET", "POST"])
def generate_questions():
    if request.method == "GET":
        return render_template("question_generator.html")
    paragraph = request.form.get("paragraph", "").strip()
    if not paragraph:
        return render_template("question_generator.html", error="Please enter a paragraph.")
    
    # Primary: Use Gemini API for superior speed and quality
    try:
        prompt = f"Generate 5 high-quality, relevant educational questions based strictly on the following text. Return them as a clean list with one question per line:\n\n{paragraph}"
        model = get_gemini_model()
        response = model.generate_content(prompt)
        # Parse questions, removing any leading list numbering
        questions = [line.strip().lstrip('0123456789.-* ') for line in response.text.split('\n') if line.strip()]
        return render_template("question_generator_result.html", questions=questions, input_paragraph=paragraph)
    except Exception as gemini_err:
        print(f"Gemini Question Gen failed: {gemini_err}. Trying local model fallback...")
        try:
            qg = get_question_generator()
            chunks = textwrap.wrap(paragraph, width=300)
            all_questions = []
            for chunk in chunks:
                input_text = f"generate questions: {chunk}"
                questions = qg(input_text, max_length=50, num_return_sequences=3, num_beams=5, batch_size=1)
                all_questions.extend(q["generated_text"] for q in questions)
            return render_template("question_generator_result.html", questions=list(set(all_questions)), input_paragraph=paragraph)
        except Exception as e:
            return render_template("question_generator.html", error=f"AI Error: {gemini_err} (Fallback error: {e}). Please check your API key in .env.")

# 2. Summarizer (Enhanced for Text & Links)
def extract_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        # Break into lines and remove leading/trailing whitespace
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        return "\n".join(chunk for chunk in chunks if chunk)
    except Exception as e:
        return f"Error fetching URL: {e}"

@app.route("/summarizer", methods=["GET", "POST"])
def summarize_text():
    if request.method == "GET":
        return render_template("summarizer.html")
    
    user_text = request.form.get("user_text", "").strip()
    url = request.form.get("url", "").strip()
    
    content_to_summarize = ""
    
    if url:
        content_to_summarize = extract_text_from_url(url)
        if content_to_summarize.startswith("Error"):
            return render_template("summarizer.html", error=content_to_summarize)
    else:
        content_to_summarize = user_text
        
    if not content_to_summarize:
        return render_template("summarizer.html", error="Please provide text or a valid URL.")

    # Use Gemini for superior summarization, but handle errors
    try:
        prompt = f"Summarize the following content in a few clear, concise sentences. Use bullet points if helpful:\n\n{content_to_summarize[:10000]}"
        model = get_gemini_model()
        response = model.generate_content(prompt)
        summary_text = response.text
    except Exception as e:
        # Fallback to BART if Gemini fails
        try:
            sb = get_summarizer()
            summary_text = sb(content_to_summarize[:1000], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            summary_text = "(Fallback Summary) " + summary_text
        except Exception as fallback_err:
            return render_template("summarizer.html", error=f"AI Error: {e} (Fallback error: {fallback_err}). Please check your API key in .env.")
    
    return render_template("summarizer_result.html", summary=summary_text, input_text=content_to_summarize[:500] + "...")

# 3. Question Answering
@app.route("/answer-question", methods=["GET", "POST"])
def answer_question():
    if request.method == "GET":
        return render_template("qa.html")
    context = request.form.get("context", "").strip()
    question = request.form.get("question", "").strip()
    if not context or not question:
        return render_template("qa.html", error="Please provide both context and question.")
    
    # Primary: Use Gemini API for superior speed and accuracy
    try:
        prompt = f"Using the following context, answer the question accurately and concisely:\n\nContext:\n{context}\n\nQuestion:\n{question}"
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return render_template("qa_result.html", answer=response.text, question=question, context=context)
    except Exception as gemini_err:
        print(f"Gemini QA failed: {gemini_err}. Trying local model fallback...")
        try:
            qa = get_qa_pipeline()
            result = qa(question=question, context=context)
            return render_template("qa_result.html", answer=result["answer"], question=question, context=context)
        except Exception as e:
            return render_template("qa.html", error=f"AI Error: {gemini_err} (Fallback error: {e}). Please check your API key in .env.")

# 4. Study Plan Generator
@app.route("/study-plan", methods=["GET", "POST"])
def study_plan():
    if request.method == "GET":
        return render_template("study_plan.html")
    syllabus = request.form.get("syllabus", "")
    topics = request.form.get("topics", "")
    start_date = request.form.get("start_date", "")
    deadline = request.form.get("deadline", "")
    
    prompt = f"Create a detailed study plan for: {syllabus}. Topics: {topics}. From {start_date} to {deadline}. Format in Markdown."
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return render_template("study_plan_result.html", study_plan=response.text)
    except Exception as e:
        return render_template("study_plan.html", error=f"AI Error: {e}. Please check your API key in .env.")

# 5. Topic Researcher
@app.route("/research", methods=["GET", "POST"])
def research():
    if request.method == "GET":
        return render_template("research.html")
    topic = request.form.get("topic", "").strip()
    if not topic:
        return render_template("research.html", error="Please enter a topic.")
    prompt = f"Provide a comprehensive educational guide on: {topic}. Use Markdown."
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return render_template("research_result.html", topic=topic, info=response.text)
    except Exception as e:
        return render_template("research.html", error=f"AI Error: {e}. Please check your API key in .env.")

# 6. Web-Search QA
@app.route("/web-search", methods=["GET", "POST"])
def web_search():
    if request.method == "GET":
        return render_template("web_search.html")
    question = request.form.get("question", "").strip()
    if not question:
        return render_template("web_search.html", error="Please enter a question.")
    prompt = f"Search and answer: {question}. Provide a detailed response."
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return render_template("web_search_result.html", question=question, answer=response.text)
    except Exception as e:
        return render_template("web_search.html", error=f"AI Error: {e}. Please check your API key in .env.")

# 7. Flashcards
@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    if request.method == "GET":
        return render_template("flashcards.html")
    topic = request.form.get("topic", "").strip()
    if not topic:
        return render_template("flashcards.html", error="Please enter a topic.")
    prompt = f"Generate 5 educational flashcards for: {topic}. Return JSON: [{{'question': '...', 'answer': '...'}}]"
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        try:
            cards = json.loads(text)
        except json.JSONDecodeError:
            # Attempt to fix common JSON issues or just report error
            return render_template("flashcards.html", error="AI returned invalid JSON. Please try again.")
        return render_template("flashcards_result.html", topic=topic, cards=cards)
    except Exception as e:
        return render_template("flashcards.html", error=f"AI Error: {e}. Please check your API key in .env.")

if __name__ == "__main__":
    # Binding to 0.0.0.0 is robust for both IPv4 and IPv6 connections on local networks/machines
    app.run(host="0.0.0.0", port=5000, debug=True)
