from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load AI text detector model
ai_detector = pipeline("text-classification", model="roberta-base-openai-detector")

@app.route("/", methods=["GET", "POST"])
def check_plagiarism():
    question = "Question"  # Example subjective question

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            return render_template("plqaga.html", error="Please enter an answer.")

        try:
            # Detect AI probability
            result = ai_detector(text)
            ai_probability = round(result[0]["score"] * 100, 2)

            return render_template("plqaga.html", result=f"AI Probability: {ai_probability}%", question=question, answer=text)
        
        except Exception as e:
            return render_template("plqaga.html", error=f"Error: {str(e)}", question=question)

    return render_template("plqaga.html", question=question)

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 10000))  # Get the port from the environment or default to 10000
     app.run(debug=True, host="0.0.0.0", port=port)

