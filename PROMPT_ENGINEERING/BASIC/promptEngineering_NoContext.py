# pip install python-docx google-generativeai

'''
Python script using the Gemini API. It implements the three-phase pipeline we outlined. 
It uses the google-generativeai library to manage the system instructions and force the JSON outputs.

You will need to install the SDK first by running pip install google-generativeai.

Make sure you set your API key as an environment variable (export GEMINI_API_KEY="your_key_here") before running it.

The script manages state implicitly because the system_instruction is attached to the model object. 
Every call you make against model.generate_content is automatically grounded in your master profile.

---

As written, each model.generate_content() call is completely stateless. 
While the model remembers your system_instruction (your Master Profile) because it is tied to the model object, it completely forgets the job description by the time it reaches Phase 3. 
Phase 3 would likely hallucinate or fail because the job description was only sent in Phase 1.

'''

import os
import json
import google.generativeai as genai
from docx import Document

# Setup your API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)

MASTER_PROFILE = """
John Doe
Email: john.doe@email.com | Phone: 555-0100
Software Engineer with 5 years of experience building scalable backend systems.
Skills: Python, React, PostgreSQL, Docker, AWS, CI/CD.
Experience:
- Backend Engineer at TechCorp (2021-Present): Reduced API latency by 40% using Redis. Built microservices in Python.
- Junior Developer at WebSolutions (2019-2021): Managed database migrations and wrote unit tests.
"""

JOB_DESCRIPTION = """
We are looking for a Senior Python Developer to join our core infrastructure team.
Requirements:
- 4+ years of Python experience.
- Deep knowledge of AWS services (EC2, S3, RDS).
- Experience transitioning monolithic architectures to microservices.
- Must be located in North America or willing to relocate.
"""

# This takes the JSON dictionary from Phase 2 and writes it into a cleanly formatted Word file. 
def create_word_document(resume_data, filename="Tailored_Resume.docx"):
    doc = Document()
    
    # Header
    doc.add_heading(resume_data.get("name", "Name Missing"), 0) #Include name and contact info so the final document has a proper header.
    doc.add_paragraph(resume_data.get("contact_info", ""))
    
    # Summary
    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(resume_data.get("summary", ""))
    
    # Experience
    doc.add_heading("Experience", level=1)
    for job in resume_data.get("experience", []):
        job_heading = f"{job.get('title', '')} at {job.get('company', '')}"
        doc.add_heading(job_heading, level=2)
        
        for bullet in job.get("bullets", []):
            doc.add_paragraph(bullet, style='List Bullet')
            
    # Skills
    doc.add_heading("Technical Skills", level=1)
    skills_text = ", ".join(resume_data.get("skills", []))
    doc.add_paragraph(skills_text)
    
    doc.save(filename)
    print(f"Saved resume to {filename}")

def run_job_pipeline():
    system_instruction = f"""
    You are an expert career strategist and technical resume writer. 
    You process job descriptions and tailor applicant profiles to match. 
    Do not invent experience. Rely strictly on the provided Master Profile.
    
    Master Profile:
    {MASTER_PROFILE}
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction
    )

    print("Phase 1: Analyzing job suitability...")
    
    suitability_prompt = f"""
    Evaluate this job description against the Master Profile. 
    Return a strict JSON object with these keys: 
    - "match_score" (integer 0-100)
    - "apply_recommendation" (boolean)
    - "missing_skills" (list of strings)
    - "visa_location_blockers" (string)
    - "targeted_keywords" (list of strings)
    
    Job Description:
    {JOB_DESCRIPTION}
    """
    
    response_1 = model.generate_content(
        suitability_prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    suitability_data = json.loads(response_1.text)
    print(f"Match Score: {suitability_data.get('match_score')}%")
    
    if not suitability_data.get("apply_recommendation"):
        print("\nPipeline stopped. The AI does not recommend applying for this role.")
        return

    print("\nPhase 2: Generating tailored resume data...")
    
    keywords = suitability_data.get("targeted_keywords", [])
    resume_prompt = f"""
    Rewrite the Master Profile to target the job description. 
    Focus heavily on these keywords: {keywords}. 
    Return a strict JSON object matching this exact schema:
    {{
        "name": "string",
        "contact_info": "string",
        "summary": "string",
        "experience": [
            {{
                "company": "string",
                "title": "string",
                "bullets": ["string", "string"]
            }}
        ],
        "skills": ["string"]
    }}
    Keep all bullets concise and action-oriented.
    """
    
    response_2 = model.generate_content(
        resume_prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    resume_data = json.loads(response_2.text)
    create_word_document(resume_data)
    
    print("\nPhase 3: Drafting the cover letter...")
    
    cover_letter_prompt = """
    Write a 3-paragraph cover letter for this role. 
    Address the specific goals of the company mentioned in the job description. 
    Highlight past achievements from the Master Profile that solve those specific problems. 
    Do not use generic opening hooks. Output plain text.
    """
    
    response_3 = model.generate_content(cover_letter_prompt)
    
    # The script now saves both the resume and the cover letter automatically to your current folder.
    with open("Cover_Letter.txt", "w") as f:
        f.write(response_3.text)
    print("Saved cover letter to Cover_Letter.txt")

if __name__ == "__main__":
    run_job_pipeline()