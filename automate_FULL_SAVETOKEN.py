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
from Controllers.Utilities.get_linkedin import scrape_job_description, scrape_job_description_manual, appendLinkedinResult
from Controllers.Utilities.utility import load_file, save_text, multi_line_input_INPUTFINISH_skipENTER, clean_xml_text, clean_dict
from Controllers.fix_cv_schema import fix_cv_schema
from Controllers.generate_docx_cv import generate_docx_cv
from Controllers.generate_docx_coverletter import generate_docx_coverletter
from Controllers.merge_docx import merge_documents
from Controllers.Utilities.mock_gpt import (
    simulate_check,
    simulate_cv,
    simulate_cover_letter,
    manual_gpt
)

# ------------------------
# CONSTANT VARIABLES
# ------------------------

# COLOR
RED = '\033[91m'
RESET = '\033[0m'



# ------------------------
# MAIN
# ------------------------
def main():
    #IF SOME PARAMETER NOT PASSED
    if len(sys.argv) == 14:
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

        mode_choice = sys.argv[13]

    elif len(sys.argv) == 1:
        url = input("URL: ") or ""
        if (url == ""):
           return
        
        job_desc = input("Job Title without space or special character: ") or ""

        scrap_path = input("Linkedin Scrap Txt Path: ") or "scrapLinkedin_" + job_desc + ".txt"
        profile_path = input("Profile Path: ") or ".\PROMPT\PROFILE.txt"

        #prompt_check_path = input("Prompt Check Path: ") or ".\PROMPT\PROMPT_CHECK.txt"
        prompt_check_path = input("Prompt Check Full Path: ") or ".\PROMPT\PROMPT_FULL.txt"

        template_cv_path = input("Prompt Template CV Path: ") or ".\TEMPLATE\TEMPLATE_CV.docx"
        prompt_cv_path = input("Prompt CV: ") or ".\PROMPT\PROMPT_CV.txt" 
        data_cv_path = input("Prompt CV JSON Output Path: ") or "data_cv.json"

        template_cl_path = input("Prompt Template COVER LETTER Path: ") or ".\TEMPLATE\TEMPLATE_COVERLETTER.docx"
        prompt_cl_path = input("Prompt COVER LETTER: ") or ".\PROMPT\PROMPT_COVERLETTER.txt" 
        data_cl_path = input("Prompt COVER LETTER JSON Output Path: ") or "data_cl.json"

        output_docx = job_desc + ".docx"

        from_linkedin = input("From Linkedin (y/n): ").lower().strip()
        from_linkedin_bool = from_linkedin.strip().lower() in ("", "y", "yes", "true", "t", "1")
    
        print("\n--- SELECT MODE ---")
        print("1. Check LinkedIn (Scrap + Analysis)")
        print("2. Generate CV")
        print("3. Generate Cover Letter")
        print("4. Generate CV + Cover Letter")
        print("5. CV + Cover Letter (Only if Mandatory)")
        mode_choice = input("\n👉 Select mode (1-5): ") or "1"

    else:
        print("""ERROR REQUIRED ARGUMENTS WERE NOT GIVEN!!
Usage:
python automate.py <URL> <scrap.txt> <profile.txt> <PROMPTCHECK.txt> <TEMPLATECV.docx> <PROMPTCV.txt> <data_cv.json> <TEMPLATECOVERLETTER.docx> <PROMPTCOVERLETTER.txt> <data_coverletter.json> <output.docx> <FROM LINKEDIN (y/n)> <mode>
              
Mode:
1. Check LinkedIn (Scrap + Analysis)
2. Generate CV
3. Generate Cover Letter
4. Generate CV + Cover Letter
5. Generate CV + Cover Letter (Only if Mandatory)

Example:
python automate.py "https://www.linkedin.com/jobs/view/1234567890/" "scrapLinkedin.txt" ".\PROMPT\PROFILE.txt" ".\PROMPT\PROMPT_CHECK.txt" ".\TEMPLATE\TEMPLATE_CV.docx" ".\PROMPT\PROMPT_CV.txt" "data_cv.json" ".\TEMPLATE\TEMPLATE_COVERLETTER.docx" ".\PROMPT\PROMPT_COVERLETTER.txt" "data_cl.json" "output.docx" "y" "4"
        """)
        return

    #SPLIT THE output into output_cv and output_coverletter
    base, ext = os.path.splitext(output_docx)
    if ext == "":
      ext = ".docx" #EXTENSION OUTPUT ALWAYS DOCX
    output_cv_docx = f"{base}_RESUME{ext}"
    output_cl_docx = f"{base}_COVERLETTER{ext}"

    run_automation(url, scrap_path, profile_path, prompt_check_path, 
                   template_cv_path, prompt_cv_path, data_cv_path,
                   template_cl_path, prompt_cl_path, data_cl_path, 
                   output_cv_docx, output_cl_docx, from_linkedin_bool,
                   mode=mode_choice)


def run_automation (url, scrap_path, profile_path, prompt_check_path, 
                   template_cv_path, prompt_cv_path, data_cv_path,
                   template_cl_path, prompt_cl_path, data_cl_path, 
                   output_cv_docx, output_cl_docx, from_linkedin_bool = True, mode = "4"):
        # 1. SCRAPE LINKEDIN
    if (from_linkedin_bool):
       job_desc = scrape_job_description(url)
    else:
       job_desc = scrape_job_description_manual()

    # save raw scrape
    job_desc = clean_xml_text(job_desc)
    save_text(scrap_path, url + "\n\n" + job_desc)



    # 2. CHECK SUITABILITY (Always runs to determine logic)
    print("1. 🔍 Checking job suitability...")

    #2A. LOAD INFORMATION TO BUILD PROMPT
    profile = load_file(profile_path) #LOAD FILES
    prompt = load_file(prompt_check_path) #LOAD FILES
    print("\nOptional: Add your own suitability note (press ENTER to skip)")
    suitability_note = ""
    suitability_note = multi_line_input_INPUTFINISH_skipENTER("👉 Your note: ")
    if suitability_note:
      suitability_note = "[SUITABILITY NOTE]\n\n" + suitability_note
    
    print("\nOptional: Add extra questions (press ENTER to skip)")
    extra_questions = multi_line_input_INPUTFINISH_skipENTER("👉 Your questions: ")
    
    extra_section = ""
    if extra_questions:
        extra_section = f"""

----------------------

[ADDITIONAL QUESTIONS]
{extra_questions}

Answer them and include results in JSON under "additional_answers".

        """
    
    
    #2B. BUILT GPT PROMPT
    check_prompt = f"""
Evaluate job suitability and provide a structured analysis.

[INSTRUCTION]

{prompt}

----------------------

{suitability_note}

----------------------

[OUTPUT RULES]
1. OUTPUT STRICTLY IN JSON.
    * Keep notes concise but insightful
    * Do not hallucinate requirements or my background or suitability
2. Use this schema: {json.dumps(CHECK_SCHEMA)}
3. Do not include any markdown formatting tags or prose.

----------------------

OUTPUT STRICTLY IN JSON:
{CHECK_SCHEMA}

{extra_section}

------------------------

[JOB DESCRIPTION]
{job_desc}

------

[PROFILE]
{profile}

    """

    check_prompt_new = load_file(prompt_check_path).replace("[JOB_ADS_HERE]", job_desc).replace("[SUITABILITY_NOTE_HERE]", suitability_note).replace("[ADDITIONAL_QUESTIONS_HERE]", extra_section)

    #2C. CALL GPT
    # check_data = generate_json(check_prompt)
    # check_data = simulate_check() #TEMP
    check_data = manual_gpt(check_prompt_new) #TEMP
    #validate_json(check_data, "CHECK")

    
    #2D. PRINT REVIEW
    result_text = "\n===== JOB CHECK RESULT =====\n"
    result_text += f"Match Score        : {check_data['match_score']}%" + "\n"
    result_text += f"Suitable           : {check_data['is_suitable']}" + "\n"
    result_text += f"{RED}!! VISA STATUS: {check_data.get('visa_sponsorship', 'NO TALK ABOUT SPONSORSHIP').upper()}{RESET}" + "\n"
    #result_text += f"Visa               : {check_data['visa_sponsorship']}" + "\n"
    result_text += f"Language Fit       : {check_data['language_fit']}" + "\n"
    
    # --- LANGUAGE STATUS ALERTS ---
    known_langs = ["malay", "bahasa", "indonesia", "english", "hokkien"]
    req_langs_str = check_data.get('language_fit', "")
    # Parse comma separated list from GPT
    req_langs = [l.strip().lower() for l in req_langs_str.split(',') if l.strip()]
    language_unfulfilled = [l.upper() for l in req_langs if l not in known_langs]
    if language_unfulfilled:
        result_text += f"{RED}!! LANGUAGE WARNING: {', '.join(language_unfulfilled)} REQUIRED (NOT FULFILLED){RESET}" + "\n"

    result_text += "\nMissing Requirements: \n"
    for m in check_data.get("missing_requirements", []):
        result_text += f"- {m}" + "\n"

    result_text += "\nMandatory Documents:\n"
    for d in check_data.get("mandatory_documents", []):
        result_text += f"- {d}" + "\n"

    if check_data.get("additional_answers"):
        result_text += "\nAdditional Answers:\n"
        for qa in check_data["additional_answers"]:
            result_text += f"Q: {qa['question']}\n"
            result_text += f"A: {qa['answer']}\n\n"

    result_text += "\n============================\n"

    print(result_text)
    appendLinkedinResult(scrap_path, check_data, result_text)

    if mode == "1":
        print("\n✅ Analysis complete. Exiting Mode 1.")
        return
    

    # 2E. If big blocker than stop process
    is_no_sponsorship = check_data.get('visa_sponsorship', '').upper() == "NO SPONSORSHIP EXPLICITLY"
    
    if is_no_sponsorship or language_unfulfilled:
        print(f"\n{RED}🚨 CRITICAL BLOCKERS DETECTED!{RESET}" + "\n")
        if is_no_sponsorship:
            print(f"- Job explicitly denies sponsorship.\n")
        if language_unfulfilled:
            print(f"- Missing mandatory languages: {', '.join(language_unfulfilled)}\n")
        
        confirm = input(f"\n{RED}Do you still want to proceed with document generation? (y/n): {RESET}").lower().strip()
        if confirm != 'y':
            print("❌ Operation aborted based on blockers.\n\n")
            return


    # 3. GENERATE CV
    # 3A. ASK WHETHER WANT TO GENERATE CV?
    should_gen_cv = mode in ["2", "4", "5"]

    if (should_gen_cv == False):
        cont = input("Do you want to generate CV? (y/n): ")

        if cont.lower() != "y":
            print("❌ Stopped.")
            return
        else:
           should_gen_cv = True
    
    if (should_gen_cv == True):
        print("\n========= CV GENERATION ==========\n")
        # 3B. LOAD INFORMATION TO BUILT PROMPT
        prompt = load_file(prompt_cv_path) #TAKE FROM PROMPT FILES

        print("\nOptional: Add your own suitability note (press ENTER to skip)")
        suitability_note = ""
        suitability_note = multi_line_input_INPUTFINISH_skipENTER("👉 Your note: ")
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
        cv_data = clean_dict(cv_data)
        #validate_json(data, "CV")

        # 3E. SAVE JSON
        with open(data_cv_path, "w", encoding="utf-8") as f:
            json.dump(cv_data, f, indent=2, ensure_ascii=False)

        # 3F. GENERATE DOCX
        generate_docx_cv(template_cv_path, data_cv_path, output_cv_docx)
  




    print("\n\n====================================\n")
    # 3. GENERATE COVER LETTER
    cl_mandatory = check_data.get("cover_letter_required", False)
    should_gen_cl = (mode == "3") or (mode == "4") or (mode == "5" and cl_mandatory)

    if (should_gen_cl == False):
        # 3A. ASK WHETHER WANT TO GENERATE COVER LETTER?
        if check_data.get("cover_letter_required"):
            print("⚠️ Cover letter is MANDATORY")
        else:
            print("Cover letter is NOT MANDATORY")

        cont = input("Do you want to generate cover letter? (y/n): ")

        if cont.lower() == "y":
            should_gen_cl = True

    if (should_gen_cl == True):
        print("\n========= COVER LETTER GENERATION ==========\n")
        # 4B. LOAD INFORMATION TO BUILD PROMPT
        prompt = load_file(prompt_cl_path) #LOAD FILES
        print("\nOptional: Add your own suitability note (press ENTER to skip)")
        suitability_note = ""
        suitability_note = multi_line_input_INPUTFINISH_skipENTER("👉 Your note: ")
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
        cover_data = clean_dict(cover_data)
        #validate_json(cover_data, "COVERLETTER")

        # 3E. SAVE JSON
        with open(data_cl_path, "w", encoding="utf-8") as f:
          json.dump(cover_data, f, indent=2, ensure_ascii=False)

        # 3F. GENERATE DOCX
        generate_docx_coverletter(template_cl_path, data_cl_path, output_cl_docx)

    
    # 4. FINAL MERGE
    if mode == "1":
        print("\n✅ Analysis complete. Exiting Mode 1.")
        return
    
    # Only merge if the files actually exist (prevents errors in Mode 1 or if skipped)
    if os.path.exists(output_cv_docx) or os.path.exists(output_cl_docx):
        print("\n4. 📄 Merging documents into final output...")
        final_docx_name = output_cv_docx.replace("_RESUME", "") 
        try:
            merge_documents(
                output_cv_docx if os.path.exists(output_cv_docx) else None, 
                output_cl_docx if os.path.exists(output_cl_docx) else None, 
                scrap_path, 
                final_docx_name
            )
        except Exception as e:
            print(f"❌ Failed to merge documents: {e}")
        
        



if __name__ == "__main__":
    main()