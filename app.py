from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, uuid
from mcq.pipeline import extract_text, generate_mcqs

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
app.secret_key = "dev"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def ok_ext(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    f = request.files.get("document")
    if not f or f.filename == "":
        flash("Select a .txt, .pdf, or .docx file."); return redirect(url_for("index"))
    if not ok_ext(f.filename):
        flash("Unsupported file type."); return redirect(url_for("index"))

    num_qs = int(request.form.get("num_questions", 8))
    use_summary = request.form.get("use_summary") == "on"

    name = secure_filename(f.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], f"{uuid.uuid4().hex}_{name}")
    f.save(path)

    try:
        text = extract_text(path)
        mcqs = generate_mcqs(text, n=num_qs, use_summary=use_summary)
    except Exception as e:
        flash(f"Error: {e}")
        mcqs = []

    try: os.remove(path)
    except Exception: pass

    return render_template("results.html", mcqs=mcqs)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
