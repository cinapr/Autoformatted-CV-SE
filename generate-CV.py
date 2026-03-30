import sys
import json
from openai import OpenAI

from get_linkedin import scrape_job_description
from generate_docx import generate_docx


# ------------------------
# Load file
# ------------------------
def load_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ------------------------
# Save text
# ------------------------
def save_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# ------------------------
# GPT CALL
# ------------------------
def generate_json(prompt):
    client = OpenAI(api_key="YOUR_API_KEY")

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an ATS CV generator. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return json.loads(response.choices[0].message.content)


# ------------------------
# MAIN
# ------------------------
def main():
    # CLI arguments
    url = sys.argv[1]
    template_path = sys.argv[2]
    prompt_path = sys.argv[3]
    profile_path = sys.argv[4]
    scrap_path = sys.argv[5]
    json_path = sys.argv[6]
    output_docx = sys.argv[7]

    # 1. SCRAPE LINKEDIN
    job_desc = scrape_job_description(url)

    # save raw scrape
    save_text(scrap_path, job_desc)

    # 2. LOAD FILES
    profile = load_file(profile_path)
    prompt = load_file(prompt_path)

    # 3. BUILD GPT PROMPT
    full_prompt = f"""
[JOB DESCRIPTION]
{job_desc}

----------------------

[PROFILE]
{profile}

----------------------

[INSTRUCTION]
{prompt}

----------------------

OUTPUT STRICTLY IN JSON:
{{
  "summary": [],
  "experience": [],
  "projects": [],
  "tech": [],
  "skills": [],
  "awards": [],
  "education": {{
    "focus": "",
    "thesis": ""
  }}
}}
"""

    # 4. CALL GPT
    data = generate_json(full_prompt)

    # 5. SAVE JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 6. GENERATE DOCX
    generate_docx(template_path, json_path, output_docx)

    print("✅ CV generated successfully!")


if __name__ == "__main__":
    main()