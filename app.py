from flask import Flask, request, render_template
import os

from main import load_resumes, load_job_description, rank_resumes, extract_skills

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        files = request.files.getlist("resumes")

        for f in os.listdir("resumes"):
            os.remove(os.path.join("resumes", f))

        for file in files:
            file.save(os.path.join("resumes", file.filename))

        resumes = load_resumes("resumes")
        job_desc = request.form["job_desc"]

        ranked = rank_resumes(job_desc, resumes)

        for i, (name, score) in enumerate(ranked, start=1):
            skills = extract_skills(resumes[name])
            results.append({
                "rank": i,
                "name": name,
                "score": round(score, 2),
                "skills": ", ".join(skills)
            })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)