import sys
import json

from docx import Document
from copy import deepcopy

from Controllers.Utilities.schema import validate_json
from Controllers.Utilities.get_linkedin import scrape_job_description
from Controllers.Utilities.generate_docx import (
    replace_single_value, 
    insert_experience, 
    insert_projects, 
    remove_section
)

from Controllers.Utilities.utility import (
    set_text,
    insert_simple_bullets,
    insert_labeled_bullets
)

def generate_docx_cv(template_path, json_path, output_path):
    doc = Document(template_path)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if not validate_json(data, "CV"):
        print("❌ Fix JSON before generating CV")
        return

    # EDUCATION
    replace_single_value(doc, "{{FOCUS_REPLACE}}", data["education"]["focus"])
    replace_single_value(doc, "{{THESIS_REPLACE}}", data["education"]["thesis"])

    # OTHER SECTIONS
    insert_simple_bullets(doc, "{{SUMMARY_ITEM}}", data["summary"])
    insert_labeled_bullets(doc, "{{TECH_TITLE}}", data["tech"])
    insert_labeled_bullets(doc, "{{SKILL_TITLE}}", data["skills"])
        
    insert_experience(doc, data["experience"])
    
    # NOT MANDATORY
    if "awards" not in data or not data["awards"]:
        remove_section(doc, "AWARDS & CERTIFICATIONS")
    else:
        insert_simple_bullets(doc, "{{AWARDS_BULLET}}", data["awards"])
    #if "awards" in data and data["awards"]:
    #    insert_simple_bullets(doc, "{{AWARDS_BULLET}}", data["awards"])
    #else:
    #    remove_section(doc, "{{AWARDS_BULLET}}", "AWARDS & CERTIFICATIONS")

    #if data.get("projects"):
    #    insert_projects(doc, data["projects"])
    #else:
    if "projects" not in data or not data["projects"]:
        remove_section(doc, "OPEN-SOURCE PROJECTS")
    else:
        insert_projects(doc, data["projects"])

    doc.save(output_path)
    print(f"✅ CV generated: {output_path}")

