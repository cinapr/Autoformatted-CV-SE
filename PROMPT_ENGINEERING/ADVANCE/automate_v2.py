# just run this script. It reads your prompts, hits the API, remembers the context, and spits out the exact JSON files your original Word document generators need to build the final .docx files.
 
import os
import json
import google.generativeai as genai

# Helper to load and inject variables into markdown
def load_prompt(filepath, **kwargs):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for key, val in kwargs.items():
        content = content.replace(f"{{{{{key}}}}}", val)
    return content

def main():
    # 1. Get the Job Description from the user
    job_desc = input("Paste the Job Description here (press Enter to submit): ")
    if not job_desc:
        print("No job description provided. Exiting.")
        return

    # 2. Setup Gemini and Context
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    profile_text = load_prompt("context/cindy_profile.txt")
    system_instruction = load_prompt("context/system_instruction.md", PROFILE_DATA=profile_text)

    # Initialize the model with the system persona
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction,
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Start the persistent chat session
    chat = model.start_chat(history=[])

    # -----------------------------------------
    # PHASE 1: JOB CHECK
    # -----------------------------------------
    print("\n🔍 Analyzing job suitability...")
    prompt_check = load_prompt("prompts/1_check.md", JOB_DESCRIPTION=job_desc)
    res_check = chat.send_message(prompt_check)
    check_data = json.loads(res_check.text)
    
    print(f"Match Score: {check_data.get('match_score')}%")
    if not check_data.get('is_suitable'):
        print("🚨 Job is not suitable based on blockers. Stopping pipeline.")
        return

    # -----------------------------------------
    # PHASE 2: GENERATE CV
    # -----------------------------------------
    print("\n📄 Generating tailored CV data...")
    prompt_cv = load_prompt("prompts/2_resume.md")
    res_cv = chat.send_message(prompt_cv)
    cv_data = json.loads(res_cv.text)
    
    with open("data_cv.json", "w", encoding="utf-8") as f:
        json.dump(cv_data, f, indent=2)
    print("✅ Saved data_cv.json")

    # -----------------------------------------
    # PHASE 3: GENERATE COVER LETTER
    # -----------------------------------------
    if check_data.get("cover_letter_required"):
        print("\n✉️ Generating tailored Cover Letter...")
        prompt_cl = load_prompt("prompts/3_coverletter.md")
        res_cl = chat.send_message(prompt_cl)
        cl_data = json.loads(res_cl.text)
        
        with open("data_cl.json", "w", encoding="utf-8") as f:
            json.dump(cl_data, f, indent=2)
        print("✅ Saved data_cl.json")
    else:
        print("\n⏭️ Cover letter not mandatory. Skipping.")

    print("\n🎉 Pipeline complete. You can now pass the JSON files to your docx generators.")

if __name__ == "__main__":
    main()