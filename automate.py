import os
import sys
import json
import pyperclip

from Controllers.Utilities.gpt_call import generate_json
from Controllers.Utilities.get_linkedin import scrape_job_description
from Controllers.Utilities.utility import load_file, save_text
from Controllers.generate_docx_cv import generate_docx_cv
from Controllers.generate_docx_coverletter import generate_docx_coverletter
from Controllers.Utilities.mock_gpt import (
    simulate_check,
    simulate_cv,
    simulate_cover_letter
)


# ------------------------
# MAIN
# ------------------------
def main():
    #IF SOME PARAMETER NOT PASSED
    if len(sys.argv) < 12:
        print("""
Usage:
python automate.py <URL> <scrap.txt> <profile.txt> <PROMPTCHECK.txt> <TEMPLATECV.docx> <PROMPTCV.txt> <data_cv.json> <TEMPLATECOVERLETTER.docx> <PROMPTCOVERLETTER.txt> <data_coverletter.json> <output.docx>

Example:
python automate.py "https://www.linkedin.com/jobs/view/1234567890/" "scrapLinkedin.txt" ".\PROMPT\PROFILE.txt" ".\PROMPT\PROMPT_CHECK.txt" ".\TEMPLATE\TEMPLATE_CV.docx" ".\PROMPT\PROMPT_CV.txt" "data_cv.json" ".\TEMPLATE\TEMPLATE_COVERLETTER.docx" ".\PROMPT\PROMPT_COVERLETTER.txt" "data_cl.json" "output.docx"
        """)
        return

    # CLI arguments
    url = sys.argv[1]
    scrap_path = sys.argv[2]
    profile_path = sys.argv[3]

    prompt_check_path = sys.argv[4]

    template_cv_path = sys.argv[5]
    prompt_cv_path = sys.argv[6]
    data_cv_path = sys.argv[7]

    template_cl_path = sys.argv[8]
    prompt_cl_path = sys.argv[9]
    data_cl_path = sys.argv[10]

    output_docx = sys.argv[11]
    #SPLIT THE output into output_cv and output_coverletter
    base, ext = os.path.splitext(output_docx)
    if ext == "":
      ext = ".docx" #EXTENSION OUTPUT ALWAYS DOCX
    output_cv_docx = f"{base}_cv{ext}"
    output_cl_docx = f"{base}_coverletter{ext}"

    # 1. SCRAPE LINKEDIN
    job_desc = scrape_job_description(url)

    # save raw scrape
    save_text(scrap_path, job_desc)



    # 2. CHECK SUITABILITY
    print("1. 🔍 Checking job suitability...")

    #2A. LOAD FILES
    profile = load_file(profile_path)
    prompt = load_file(prompt_check_path)

    #2B. BUILT GPT PROMPT
    check_prompt = f"""
Evaluate job suitability.

[INSTRUCTION]
{prompt}

----------------------

OUTPUT STRICTLY IN JSON:
{{
  "match_score": 0-100,
  "is_suitable": true/false,
  "visa_sponsorship": "Yes/No/Not mentioned",
  "language_fit": "OK/Not OK",
  "notes": [],
  "missing_requirements": [],
  "mandatory_documents": [],
  "cover_letter_required": true/false
}}

------

[JOB DESCRIPTION]
{job_desc}

------

[PROFILE]
{profile}
    """

    #2C. CALL GPT
    # check_data = generate_json(check_prompt)
    check_data = simulate_check() #TEMP
    #validate_json(check_data, "CHECK")

    #2D. PRINT REVIEW
    print("\n===== JOB CHECK RESULT =====")
    print(f"Match Score        : {check_data['match_score']}%")
    print(f"Suitable           : {check_data['is_suitable']}")
    print(f"Visa               : {check_data['visa_sponsorship']}")
    print(f"Language Fit       : {check_data['language_fit']}")

    print("\nMissing Requirements:")
    for m in check_data.get("missing_requirements", []):
        print(f"- {m}")

    print("\nMandatory Documents:")
    for d in check_data.get("mandatory_documents", []):
        print(f"- {d}")

    print("\n============================\n")



    # 3. GENERATE CV
    # 3A. ASK WHETHER WANT TO GENERATE CV?
    cont = input("Do you want to generate CV? (y/n): ")

    if cont.lower() != "y":
        print("❌ Stopped.")
        return
    
    # 3B. LOAD FILES
    prompt = load_file(prompt_cv_path)

    # 3C. BUILD GPT PROMPT
    cv_prompt = f"""

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
    
    pyperclip.copy(cv_prompt) #Save prompt to clipboard
    print("GPT Prompt generated")

    # 3D. CALL GPT
    # data = generate_json(cv_prompt)
    cv_data = simulate_cv() #TEMP
    #validate_json(data, "CV")

    # 3E. SAVE JSON
    with open(data_cv_path, "w", encoding="utf-8") as f:
        json.dump(cv_data, f, indent=2, ensure_ascii=False)

    # 3F. GENERATE DOCX
    generate_docx_cv(template_cv_path, data_cv_path, output_cv_docx)
  



    # 3. GENERATE COVER LETTER
    # 3A. ASK WHETHER WANT TO GENERATE COVER LETTER?
    if check_data.get("cover_letter_required"):
      print("\n\n====================================\n")
      print("⚠️ Cover letter is MANDATORY")

    cont = input("Do you want to generate cover letter? (y/n): ")

    if cont.lower() == "y":
        # 4B. LOAD FILES
        prompt = load_file(prompt_cl_path)

        # 4C. BUILD GPT PROMPT
        cover_prompt = f"""
[INSTRUCTION]
{prompt}

----------------------

OUTPUT STRICTLY IN JSON:
{{
  "job_title": "",
  "company_name": "",
  "company_location": "",
  "hiring_manager_name": "",
  "company_address": "",
  "letter_date": "",
  "body": []
}}

----------------------

[JOB DESCRIPTION]
{job_desc}

----------------------

[PROFILE]
{profile}
        """

        pyperclip.copy(cover_prompt) #Save prompt to clipboard
        print("GPT Prompt generated")

        # 3D. CALL GPT
        # cover_data = generate_json(cover_prompt)
        cover_data = simulate_cover_letter() #TEMP
        #validate_json(cover_data, "COVERLETTER")

        # 3E. SAVE JSON
        with open(data_cl_path, "w", encoding="utf-8") as f:
          json.dump(cover_data, f, indent=2, ensure_ascii=False)

        # 3F. GENERATE DOCX
        generate_docx_coverletter(template_cl_path, data_cl_path, output_cl_docx)
        
        



if __name__ == "__main__":
    main()