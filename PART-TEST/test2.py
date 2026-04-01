import os
import sys
import json
import pyperclip

from Controllers.Utilities.schema import (
    validate_json,
    CV_SCHEMA,
    COVERLETTER_SCHEMA,
    CHECK_SCHEMA
)
from Controllers.Utilities.gpt_call import generate_json
from Controllers.Utilities.get_linkedin import scrape_job_description
from Controllers.Utilities.utility import load_file, save_text
from Controllers.fix_cv_schema import fix_cv_schema
from Controllers.generate_docx_cv import generate_docx_cv
from Controllers.generate_docx_coverletter import generate_docx_coverletter
from Controllers.Utilities.mock_gpt import (
    simulate_check,
    simulate_cv,
    simulate_cover_letter,
    manual_gpt
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
    save_text(scrap_path, url + "\n\n" + job_desc)


    
    # 3B. LOAD INFORMATION TO BUILT PROMPT
    profile = load_file(profile_path) #LOAD FILES
    prompt = load_file(prompt_cv_path) #TAKE FROM PROMPT FILES

    suitability_note = ""

    # 3C. BUILD GPT PROMPT
    cv_prompt = f"""

[INSTRUCTION]
{prompt}

----------------------

{suitability_note}

----------------------

OUTPUT STRICTLY IN JSON:
{CV_SCHEMA}

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
    #cv_data = simulate_cv() #TEMP
    cv_data = manual_gpt(cv_prompt) #TEMP
    cv_data = fix_cv_schema(cv_data)
    #validate_json(data, "CV")

    # 3E. SAVE JSON
    with open(data_cv_path, "w", encoding="utf-8") as f:
        json.dump(cv_data, f, indent=2, ensure_ascii=False)

    # 3F. GENERATE DOCX
    generate_docx_cv(template_cv_path, data_cv_path, output_cv_docx)
  




        



if __name__ == "__main__":
    main()