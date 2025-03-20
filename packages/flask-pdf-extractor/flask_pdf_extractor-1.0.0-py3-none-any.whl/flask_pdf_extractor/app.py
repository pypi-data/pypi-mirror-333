from flask import Flask, render_template, request
import PyPDF2
import ollama
import os

app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def upload_page():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files or "prompt" not in request.form:
        return "Missing file or prompt", 400

    file = request.files["file"]
    user_prompt = request.form["prompt"]

    if file.filename == "":
        return "No selected file", 400

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        response = process_with_ollama(text, user_prompt)

        return render_template("result.html", response=response)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    return text.strip()

def process_with_ollama(text, user_prompt):
    prompt = f"""
        {user_prompt}
        Context: {text}
        Answer:
    """
    response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def main():
    app.run(debug=True, host='0.0.0.0', port=3000)

if __name__ == "__main__":
    main()
