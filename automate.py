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
from Controllers.Utilities.get_linkedin import scrape_job_description, scrape_job_description_manual
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
    if len(sys.argv) == 13:
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

        from_linkedin = sys.argv[12]
        from_linkedin_bool = from_linkedin.lower().strip() in ("y", "yes", "true", "t", "1")

    elif len(sys.argv) == 1:
        url = input("URL: ") or ""
        if (url == ""):
           return
        
        job_desc = input("Job Title without space or special character: ") or ""

        scrap_path = input("Linkedin Scrap Txt Path: ") or "scrapLinkedin_" + job_desc + ".txt"
        profile_path = input("Profile Path: ") or ".\PROMPT\PROFILE.txt"

        prompt_check_path = input("Prompt Check Path: ") or ".\PROMPT\PROMPT_CHECK.txt"

        template_cv_path = input("Prompt Template CV Path: ") or ".\TEMPLATE\TEMPLATE_CV.docx"
        prompt_cv_path = input("Prompt CV: ") or ".\PROMPT\PROMPT_CV.txt" 
        data_cv_path = input("Prompt CV JSON Output Path: ") or "data_cv.json"

        template_cl_path = input("Prompt Template COVER LETTER Path: ") or ".\TEMPLATE\TEMPLATE_COVERLETTER.docx"
        prompt_cl_path = input("Prompt COVER LETTER: ") or ".\PROMPT\PROMPT_COVERLETTER.txt" 
        data_cl_path = input("Prompt COVER LETTER JSON Output Path: ") or "data_cl.json"

        output_docx = job_desc + ".docx"

        from_linkedin = input("From Linkedin (y/n): ").lower().strip()
        from_linkedin_bool = from_linkedin in ("y", "yes", "true", "t", "1")
    
    else:
        print("""ERROR REQUIRED ARGUMENTS WERE NOT GIVEN!!
Usage:
python automate.py <URL> <scrap.txt> <profile.txt> <PROMPTCHECK.txt> <TEMPLATECV.docx> <PROMPTCV.txt> <data_cv.json> <TEMPLATECOVERLETTER.docx> <PROMPTCOVERLETTER.txt> <data_coverletter.json> <output.docx> <FROM LINKEDIN (y/n)>

Example:
python automate.py "https://www.linkedin.com/jobs/view/1234567890/" "scrapLinkedin.txt" ".\PROMPT\PROFILE.txt" ".\PROMPT\PROMPT_CHECK.txt" ".\TEMPLATE\TEMPLATE_CV.docx" ".\PROMPT\PROMPT_CV.txt" "data_cv.json" ".\TEMPLATE\TEMPLATE_COVERLETTER.docx" ".\PROMPT\PROMPT_COVERLETTER.txt" "data_cl.json" "output.docx" "y"
        """)
        return
    
    #SPLIT THE output into output_cv and output_coverletter
    base, ext = os.path.splitext(output_docx)
    if ext == "":
      ext = ".docx" #EXTENSION OUTPUT ALWAYS DOCX
    output_cv_docx = f"{base}_cv{ext}"
    output_cl_docx = f"{base}_coverletter{ext}"

    run_automation(url, scrap_path, profile_path, prompt_check_path, 
                   template_cv_path, prompt_cv_path, data_cv_path,
                   template_cl_path, prompt_cl_path, data_cl_path, 
                   output_cv_docx, output_cl_docx, from_linkedin_bool)


def run_automation (url, scrap_path, profile_path, prompt_check_path, 
                   template_cv_path, prompt_cv_path, data_cv_path,
                   template_cl_path, prompt_cl_path, data_cl_path, 
                   output_cv_docx, output_cl_docx, from_linkedin_bool = True):
        # 1. SCRAPE LINKEDIN
    if (from_linkedin_bool):
       job_desc = scrape_job_description(url)
    else:
       job_desc = scrape_job_description_manual()

    # save raw scrape
    save_text(scrap_path, url + "\n\n" + job_desc)



    # 2. CHECK SUITABILITY
    print("1. 🔍 Checking job suitability...")

    #2A. LOAD INFORMATION TO BUILD PROMPT
    profile = load_file(profile_path) #LOAD FILES
    prompt = load_file(prompt_check_path) #LOAD FILES
    print("\nOptional: Add your own suitability note (press ENTER to skip)")
    suitability_note = input("👉 Your note: ")
    if suitability_note:
      suitability_note = "[SUITABILITY NOTE]\n\n" + suitability_note
    
    #2B. BUILT GPT PROMPT
    check_prompt = f"""
Evaluate job suitability.

[INSTRUCTION]
{prompt}

----------------------

{suitability_note}

----------------------

OUTPUT STRICTLY IN JSON:
{CHECK_SCHEMA}

------

[JOB DESCRIPTION]
{job_desc}

------

[PROFILE]
{profile}
    """

    #2C. CALL GPT
    # check_data = generate_json(check_prompt)
    # check_data = simulate_check() #TEMP
    check_data = manual_gpt(check_prompt) #TEMP
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
    
    # 3B. LOAD INFORMATION TO BUILT PROMPT
    prompt = load_file(prompt_cv_path) #TAKE FROM PROMPT FILES

    print("\nOptional: Add your own suitability note (press ENTER to skip)")
    suitability_note = input("👉 Your note: ")
    if suitability_note:
      suitability_note = "[SUITABILITY NOTE]\n\n" + suitability_note


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
  



    # 3. GENERATE COVER LETTER
    # 3A. ASK WHETHER WANT TO GENERATE COVER LETTER?
    print("\n\n====================================\n")
    if check_data.get("cover_letter_required"):
      print("⚠️ Cover letter is MANDATORY")

    cont = input("Do you want to generate cover letter? (y/n): ")

    if cont.lower() == "y":
        # 4B. LOAD INFORMATION TO BUILD PROMPT
        prompt = load_file(prompt_cl_path) #LOAD FILES
        print("\nOptional: Add your own suitability note (press ENTER to skip)")
        suitability_note = input("👉 Your note: ")
        if suitability_note:
          suitability_note = "[SUITABILITY NOTE]\n\n" + suitability_note


        # 4C. BUILD GPT PROMPT
        cover_prompt = f"""
[INSTRUCTION]
{prompt}

----------------------

{suitability_note}

----------------------

OUTPUT STRICTLY IN JSON:
{COVERLETTER_SCHEMA}

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
        #cover_data = simulate_cover_letter() #TEMP
        cover_data = manual_gpt(cover_prompt) #TEMP
        #validate_json(cover_data, "COVERLETTER")

        # 3E. SAVE JSON
        with open(data_cl_path, "w", encoding="utf-8") as f:
          json.dump(cover_data, f, indent=2, ensure_ascii=False)

        # 3F. GENERATE DOCX
        generate_docx_coverletter(template_cl_path, data_cl_path, output_cl_docx)
        
        



if __name__ == "__main__":
    main()