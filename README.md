# Autoformatted CV Generator (GPT + DOCX)
Replace DOCX placeholder with JSON value
A modular pipeline that generates ATS-optimized CVs from:
- LinkedIn job postings
- Personal profile (text)
- Custom prompt instructions

The system:
1. Scrapes job description
2. Sends job + profile + prompt to GPT
3. Receives structured JSON
4. Injects content into a DOCX template (preserving formatting)

---

## 🧱 Project Structure

```
project/
│
├── generate_cv.py # MAIN ENTRY (pipeline controller)
├── generate_docx.py # CV structure logic (DOCX manipulation)
├── utility.py # Low-level formatting helpers
├── get_linkedin.py # Job scraping
│
├── TEMPLATE.docx # Word template with placeholders
├── PROMPT.txt # Instruction prompt for GPT
├── profile.txt # Your master profile
│
├── scrap.txt # (output) scraped job content
├── data.json # (output) structured CV data from GPT
├── CVOUTPUT.docx # (output) final CV
```

---


## ▶️ How to Run

### Standard CLI

```
python generate_cv.py "URL" "TEMPLATE.docx" "PROMPT.txt" "profile.txt" "scrap.txt" "data.json" "CVOUTPUT.docx"
```

### Example

```
python generate_cv.py "https://www.linkedin.com/jobs/view/xxxx
" TEMPLATE.docx PROMPT.txt profile.txt scrap.txt data.json CVOUTPUT.docx
```


---

## 🔄 Pipeline Flow

```
LinkedIn URL
↓
get_linkedin.py → scrap.txt
↓
generate_cv.py → GPT API
↓
data.json
↓
generate_docx.py
↓
CVOUTPUT.docx
```

---

## 🧠 JSON Structure (IMPORTANT)

GPT **must return this exact structure**:

```
{
  "summary": ["bullet", "bullet"],

  "experience": [
    {
      "title": "Role",
      "company": "Company",
      "location": "Location",
      "time": "Date range",
      "bullets": ["bullet", "bullet"],
      "projects": ["optional bullet", "optional bullet"]
    }
  ],

  "projects": [
    {
      "title": "Project name",
      "bullets": ["bullet", "bullet"]
    }
  ],

  "tech": [
    {"title": "Category", "value": "Skill list"}
  ],

  "skills": [
    {"title": "Category", "value": "Skill list"}
  ],

  "awards": ["bullet", "bullet"],

  "education": {
    "focus": "text",
    "thesis": "text"
  }
}
```

---

## DOCX Template Rules

Your TEMPLATE.docx must contain placeholders:

```
Simple bullets
• {{SUMMARY_ITEM}}
• {{AWARDS_BULLET}}

Labeled bullets
• {{TECH_TITLE}}: {{TECH_STACK_ITEM}}
• {{SKILL_TITLE}}: {{SKILL_ITEM}}

Experience block
{{EXPERIENCE_BLOCK}}
{{EXPERIENCE_TITLE_ITEM}} | {{EXPERIENCE_COMPANY_ITEM}} | {{EXPERIENCE_LOCATION_ITEM}} | {{EXPERIENCE_TIME_ITEM}}
• {{EXP_ITEM}}
• Projects:
− {{EXP_PROJECT_ITEM}}

Project block
{{PROJECT_BLOCK}}
{{PROJECT_TITLE_ITEM}}
• {{PROJECT_BULLET_ITEM}}

Single values
Focus: {{FOCUS_REPLACE}}
Thesis: {{THESIS_REPLACE}}
```

---

## ⚙️ File Responsibilities

1. generate_cv.py (Main Controller)

    Handles:
    - CLI arguments
    - scraping job description
    - building GPT prompt
    - calling GPT API
    - saving JSON
    - triggering DOCX generation

    Key functions:
    - main()
    - generate_json(prompt)
    - load_file(path)
    - save_text(path)

2. get_linkedin.py

    Handles:
    - scraping job description from LinkedIn

    Key function:
    - scrape_job_description(url)

    Returns:
    - string (job description)

3. generate_docx.py

    Handles:
    - CV structure logic
    - mapping JSON → Word template

    Key functions:
    - generate_docx(template, json, output)
    - insert_experience()
    - insert_projects()
    - replace_single_value()
    - remove_section()

4. utility.py

    Handles:
    - low-level formatting (Word manipulation)
    - reusable helpers

    Key functions:
    - set_text()
    - insert_simple_bullets()
    - insert_labeled_bullets()

---

## ⚠️ Important Notes

### Encoding Issue

- Always load JSON with UTF-8: `open("data.json", encoding="utf-8")`

- Word Formatting Rule: Formatting comes from TEMPLATE.

- Python only preserves, not redesigns.