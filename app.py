from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import docx
import spacy

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Role keywords (you can add more)
ROLE_KEYWORDS = {
    "Data Scientist": [
        "python", "machine learning", "data analysis", "statistics", "pandas", "numpy",
        "regression", "classification", "data visualization", "matplotlib", "scikit-learn"
    ],

    "Software Developer": [
        "java", "c++", "c#", "javascript", "typescript", "software engineering", "react", 
        "angular", "node.js", "spring boot", "git", "object oriented programming", "oop"
    ],

    "Machine Learning Engineer": [
        "deep learning", "tensorflow", "pytorch", "neural networks", "computer vision", 
        "nlp", "keras", "model deployment", "mlops", "cloud"
    ],

    "Business Analyst": [
        "business analysis", "requirements gathering", "sql", "excel", "power bi", 
        "data visualization", "agile", "stakeholder management", "tableau", "gap analysis"
    ],

    "Frontend Developer": [
        "html", "css", "javascript", "react", "redux", "typescript", "vue.js", "next.js", 
        "responsive design", "tailwind", "bootstrap"
    ],

    "Backend Developer": [
        "node.js", "express", "django", "flask", "spring", "api development", "graphql",
        "microservices", "rest api", "database", "sql", "nosql"
    ],

    "DevOps Engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", 
        "linux", "ansible", "monitoring", "scripting"
    ],

    "Cybersecurity Analyst": [
        "network security", "penetration testing", "vulnerability assessment", 
        "firewalls", "siem", "iso 27001", "risk assessment", "incident response", 
        "cryptography", "ethical hacking"
    ],

    "Cloud Engineer": [
        "cloud computing", "aws", "azure", "gcp", "devops", "containers", "serverless", 
        "cloudformation", "terraform", "cloud security", "virtual machines"
    ],

    "Product Manager": [
        "product management", "agile", "scrum", "roadmap", "stakeholder management", 
        "user stories", "jira", "market research", "kpi", "ux", "mvp"
    ],

    "UI/UX Designer": [
        "ui design", "ux design", "figma", "adobe xd", "wireframes", "prototyping", 
        "user research", "interaction design", "visual design", "accessibility"
    ],

    "AI Engineer": [
        "artificial intelligence", "computer vision", "natural language processing", 
        "reinforcement learning", "gpt", "transformers", "deep learning", "opencv"
    ],
}

def extract_text(file):
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def analyze_resume_text(text):
    doc = nlp(text.lower())
    words = set([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

    role_scores = {}
    total_matches = 0
    total_keywords = 0

    for role, keywords in ROLE_KEYWORDS.items():
        match_count = sum(1 for kw in keywords if kw.lower() in words)
        role_scores[role] = round((match_count / len(keywords)) * 100) if keywords else 0
        total_matches += match_count
        total_keywords += len(keywords)

    ats_score = round((total_matches / total_keywords) * 100) if total_keywords else 0

    return role_scores, ats_score

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    text = extract_text(file)

    if not text.strip():
        return jsonify({"error": "No text extracted"}), 400

    predictions, ats_score = analyze_resume_text(text)

    return jsonify({
        "predictions": predictions,
        "ats": ats_score
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)