import sys
import json
import pyperclip

from Controllers.Utilities.mock_gpt import simulate_gpt
from Controllers.Utilities.gpt_call import generate_json
from Controllers.Utilities.get_linkedin import scrape_job_description
from Controllers.Utilities.utility import load_file, save_text
from Controllers.generate_docx_cv import generate_docx_cv


# ------------------------
# MAIN
# ------------------------
def main():
    #IF SOME PARAMETER NOT PASSED
    if len(sys.argv) < 8:
        print("""
        Usage:
        python automatecv.py <URL> <TEMPLATE.docx> <PROMPT.txt> <profile.txt> <scrap.txt> <data.json> <output.docx>

        Example:
        python automatecv.py "https://linkedin.com/job/..." "TEMPLATE_CV.docx" "PROMPT_CV.txt" "profile.txt" "scrap.txt" "data.json" "CVOUTPUT.docx"
        """)
        return

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

[INSTRUCTION]
{prompt}

----------------------

OUTPUT STRICTLY IN JSON:
{{
  "summary": [],
  "experience": [
    {{
      "title": "",
      "company": "",
      "location": "",
      "time": "MONTH YEAR – MONTH YEAR",
      "bullets": [],
      "projects": [] /*optional for project NDA under this company*/
    }}
  ],
  "projects": [],
  "tech": [
    {{
        "title": "",
        "value": ""
    }}
  ],
  "skills": [
    {{
        "title": "",
        "value": ""
    }}
  ],
  "awards": [],
  "education": {{
    "focus": "",
    "thesis": ""
  }}
}}

Note:
"projects" inside "experience" is optional and only used if there is NDA projects done under that company.

----------------------

[JOB DESCRIPTION]
{job_desc}

----------------------

[PROFILE]
{profile}

"""
    
    pyperclip.copy(full_prompt) #Save prompt to clipboard
    print("GPT Prompt generated")

    # 4. CALL GPT
    # data = generate_json(full_prompt)
    data = simulate_gpt()

    # 5. SAVE JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 6. GENERATE DOCX
    generate_docx_cv(template_path, json_path, output_docx)

    print("✅ CV generated successfully!")


if __name__ == "__main__":
    main()