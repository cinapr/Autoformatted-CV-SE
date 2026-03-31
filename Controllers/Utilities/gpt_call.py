import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# ---- pricing (update if OpenAI changes pricing later)
PRICE_INPUT_PER_1K = 0.01   # example: $0.01 / 1K input tokens
PRICE_OUTPUT_PER_1K = 0.03  # example: $0.03 / 1K output tokens

# LOAD ENV FILE
load_dotenv(dotenv_path=".env")

def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Missing OPENAI_API_KEY")
    return key



# FIX WHEN GPT RETURN { ... } That breaks `json.loads()`
def clean_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]  # remove ```json
        if text.startswith("json"):
            text = text[4:]
    
    return text.strip()



def calculate_gpt_cost(response):
    # ------------------------
    # TOKEN USAGE
    # ------------------------
    usage = response.usage

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    # ------------------------
    # COST CALCULATION
    # ------------------------
    cost_input = (prompt_tokens / 1000) * PRICE_INPUT_PER_1K
    cost_output = (completion_tokens / 1000) * PRICE_OUTPUT_PER_1K
    total_cost = cost_input + cost_output

    # ------------------------
    # LOGGING
    # ------------------------
    print("\n===== GPT USAGE =====")
    print(f"Prompt tokens     : {prompt_tokens}")
    print(f"Completion tokens : {completion_tokens}")
    print(f"Total tokens      : {total_tokens}")
    print(f"Cost (input)      : ${cost_input:.5f}")
    print(f"Cost (output)     : ${cost_output:.5f}")
    print(f"TOTAL COST        : ${total_cost:.5f}")
    print("=====================\n")

    return total_cost



def log_cost(job_title, total_cost):
    with open("cost_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{job_title} | ${total_cost:.5f}\n")



def generate_json(prompt, job_title=""):
    client = OpenAI(api_key=get_api_key())

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an ATS CV generator. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    # SAVE TOKEN COST TO LOG
    total_cost = calculate_gpt_cost
    log_cost(job_title, total_cost)

    content = clean_json(response.choices[0].message.content)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ GPT did not return valid JSON")
        print(content)
        raise



