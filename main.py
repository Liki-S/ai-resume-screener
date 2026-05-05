import pdfplumber
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Load resumes
def load_resumes(folder):
    resumes = {}
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            resumes[file] = extract_text_from_pdf(path)
    return resumes


# Load job description
def load_job_description(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Rank resumes
def rank_resumes(job_desc, resumes):
    job_embedding = model.encode(job_desc, convert_to_tensor=True)

    results = []
    for name, text in resumes.items():
        resume_embedding = model.encode(text, convert_to_tensor=True)

        score = util.cos_sim(job_embedding, resume_embedding).item()
        results.append((name, score))

    return sorted(results, key=lambda x: x[1], reverse=True)

def extract_skills(text):
    skills_list = [
        "python", "java", "sql", "machine learning",
        "data analysis", "deep learning", "excel",
        "c++", "javascript"
    ]

    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills

# Main function
def main():
    resumes = load_resumes("resumes")
    job_desc = load_job_description("job.txt")

    ranked = rank_resumes(job_desc, resumes)

    # Save to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Resume", "Score", "Skills"])

        for name, score in ranked:
            skills = extract_skills(resumes[name])
            writer.writerow([name, score, ";".join(skills)])

    # Print output
    print("\n📊 Resume Rankings:\n")

    for name, score in ranked:
        skills = extract_skills(resumes[name])

        print(f"{name} → Score: {score:.2f}")
        print(f"Skills: {', '.join(skills)}\n")
        

if __name__ == "__main__":
    main()